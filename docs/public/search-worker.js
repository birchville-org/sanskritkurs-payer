// ============================================================
// Payer Sanskrit Semantic Search Web Worker
// Performs client-side vector embedding inference and cosine
// similarity matching 100% in-browser (GitHub Pages compatible).
// ============================================================

let pipeline = null;
let embedder = null;
let modelLoading = false;
let modelReady = false;

// Dot product between two L2-normalized vectors (= cosine similarity)
function dotProduct(vecA, vecB) {
  let sum = 0.0;
  const len = Math.min(vecA.length, vecB.length);
  for (let i = 0; i < len; i++) {
    sum += vecA[i] * vecB[i];
  }
  return sum;
}

// Fallback hybrid text-scoring when vector model is initializing or offline
function computeHybridScore(query, record) {
  const qTokens = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
  if (qTokens.length === 0) return 0;

  const heading = (record.heading || '').toLowerCase();
  const snippet = (record.snippet || '').toLowerCase();

  let matched = 0;
  let bonus = 0;

  for (const token of qTokens) {
    if (heading.includes(token)) {
      matched++;
      bonus += 0.25;
    } else if (snippet.includes(token)) {
      matched++;
    }
  }

  if (matched === 0) return 0;
  const ratio = matched / qTokens.length;
  return Math.min(0.92, 0.45 + (ratio * 0.35) + bonus);
}

// Asynchronously load the ONNX feature extraction pipeline
async function initModel() {
  if (embedder || modelLoading) return;
  modelLoading = true;
  self.postMessage({ type: 'STATUS', status: 'loading_model' });

  try {
    const { pipeline: hfPipeline, env } = await import('https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.3.3');
    env.allowLocalModels = false;
    env.useBrowserCache = true;

    // Load nomic-embed-text-v1.5 with q8 quantization (~35MB, cached in Cache API)
    embedder = await hfPipeline('feature-extraction', 'nomic-ai/nomic-embed-text-v1.5', {
      dtype: 'q8'
    });

    modelReady = true;
    modelLoading = false;
    self.postMessage({ type: 'STATUS', status: 'ready' });
  } catch (err) {
    console.warn('[search-worker] ONNX model could not be loaded, using hybrid fallback:', err);
    modelLoading = false;
    modelReady = false;
    self.postMessage({ type: 'STATUS', status: 'fallback', error: String(err) });
  }
}

self.onmessage = async (e) => {
  const { type, query, records, lang } = e.data || {};

  if (type === 'INIT') {
    initModel();
    return;
  }

  if (type === 'SEARCH') {
    if (!query || !records || records.length === 0) {
      self.postMessage({ type: 'RESULTS', query, results: [], method: 'none' });
      return;
    }

    // Try full vector semantic search if model is ready
    if (modelReady && embedder) {
      try {
        const output = await embedder(query, { pooling: 'mean', normalize: true });
        const qVec = Array.from(output.data);

        const scored = [];
        for (const record of records) {
          if (record.embedding && record.embedding.length > 0) {
            const sim = dotProduct(qVec, record.embedding);
            scored.push({ ...record, score: sim });
          } else {
            const hSim = computeHybridScore(query, record);
            if (hSim > 0) scored.push({ ...record, score: hSim });
          }
        }

        scored.sort((a, b) => b.score - a.score);
        self.postMessage({
          type: 'RESULTS',
          query,
          results: scored.slice(0, 5),
          method: 'vector'
        });
        return;
      } catch (err) {
        console.warn('[search-worker] Vector inference failed, falling back to hybrid:', err);
      }
    }

    // If model is loading or not ready, trigger model load and use instant hybrid search
    if (!modelReady && !modelLoading) {
      initModel();
    }

    const scored = [];
    for (const record of records) {
      const sim = computeHybridScore(query, record);
      if (sim > 0) {
        scored.push({ ...record, score: sim });
      }
    }

    scored.sort((a, b) => b.score - a.score);
    self.postMessage({
      type: 'RESULTS',
      query,
      results: scored.slice(0, 5),
      method: 'hybrid',
      modelReady
    });
  }
};
