import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import http from 'http';

const API_URL = 'http://localhost:11434/v1/chat/completions';
const MODEL = 'gemma4:26b';

const CONFIG = {
  it: {
    targetDir: 'it',
    name: 'Italiano',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Italian. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Lezione", "Übung" -> "Esercizio", "Abbildung" -> "Figura", "Schrift" -> "Scrittura". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  es: {
    targetDir: 'es',
    name: 'Español',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Spanish. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Lección", "Übung" -> "Ejercicio", "Abbildung" -> "Figura", "Schrift" -> "Escritura". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  nl: {
    targetDir: 'nl',
    name: 'Nederlands',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Dutch (Nederlands). PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Les", "Übung" -> "Oefening", "Abbildung" -> "Afbeelding", "Schrift" -> "Schrift". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  hi: {
    targetDir: 'hi',
    name: 'Hindi',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Hindi. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "पाठ", "Übung" -> "अभ्यास", "Abbildung" -> "चित्र", "Schrift" -> "लिपि". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  uk: {
    targetDir: 'uk',
    name: 'Українська',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Ukrainian. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Урок", "Übung" -> "Вправа", "Abbildung" -> "Малюнок", "Schrift" -> "Письмо". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  ru: {
    targetDir: 'ru',
    name: 'Русский',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Russian. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Урок", "Übung" -> "Упражнение", "Abbildung" -> "Рисунок", "Schrift" -> "Письмо". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  bg: {
    targetDir: 'bg',
    name: 'Български',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Bulgarian. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Урок", "Übung" -> "Упражнение", "Abbildung" -> "Фигура", "Schrift" -> "Писмо". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  ta: {
    targetDir: 'ta',
    name: 'தமிழ்',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Tamil. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "பாடம்", "Übung" -> "பயிற்சி", "Abbildung" -> "படம்", "Schrift" -> "எழுத்து". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  it2: {
    targetDir: 'it2',
    name: 'Italiano (GPT-120B)',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Italian. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Lezione", "Übung" -> "Esercizio", "Abbildung" -> "Figura", "Schrift" -> "Scrittura". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  },
  it3: {
    targetDir: 'it3',
    name: 'Italiano (Nyx Opti)',
    prompt: 'Translate the following German text of a Sanskrit grammar course into Italian. PRESERVE ALL SANSKRIT TEXT (IAST and Devanagari) EXACTLY AS IS. Do not translate terms like "Sandhi", "Dvandva", "IAST". Translate German prose, headers, and metadata labels. Keep Markdown syntax, image paths, and Vue components intact. "Lektion" -> "Lezione", "Übung" -> "Esercizio", "Abbildung" -> "Figura", "Schrift" -> "Scrittura". This is for a quality test using Gemini 3 Flash and Gemma 4.'
  }
};

function stripThoughts(text) {
  return text.replace(/<\|channel>thought[\s\S]*?<channel\|>/g, '').trim();
}

async function translateText(text, lang, activeModel, activeApi, retryCount = 50) {
  if (!text.trim()) return '';

  const body = JSON.stringify({
    model: activeModel,
    messages: [
      { role: 'system', content: CONFIG[lang].prompt },
      { role: 'user', content: text }
    ],
    options: {
      temperature: 1.0,
      top_p: 0.95,
      top_k: 64,
      num_ctx: 8192
    }
  });

  for (let i = 0; i < retryCount; i++) {
    try {
      const result = await new Promise((resolve, reject) => {
        const url = new URL(activeApi);
        const options = {
          hostname: url.hostname,
          port: url.port,
          path: url.pathname,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
          },
          timeout: 1800000 // 30 minutes
        };

        const req = http.request(options, (res) => {
          let data = '';
          res.on('data', (chunk) => data += chunk);
          res.on('end', () => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(JSON.parse(data));
            } else {
              reject(new Error(`API Status ${res.statusCode}: ${data}`));
            }
          });
        });

        req.on('error', (err) => reject(err));
        req.on('timeout', () => {
          req.destroy();
          reject(new Error('Request Timeout (15 min)'));
        });

        req.write(body);
        req.end();
      });

      let content = result.choices[0].message.content;
      return stripThoughts(content);
    } catch (err) {
      console.error(`Attempt ${i + 1} failed: ${err.message}`);
      if (i === retryCount - 1) throw err;
      await new Promise(resolve => setTimeout(resolve, 30000));
    }
  }
}

async function processFile(filePath, lang, activeModel, activeApi, force = false) {
  const relativePath = path.relative('docs', filePath);
  const targetPath = path.join('docs', CONFIG[lang].targetDir, relativePath);

  if (fs.existsSync(targetPath) && !force) {
    return;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  console.log(`Translating ${path.basename(filePath)} (${(content.length / 1024).toFixed(1)} KB) to ${CONFIG[lang].name} using ${activeModel}...`);

  try {
    let translated;
    try {
      // Try Cloud first (5 retries)
      translated = await translateText(content, lang, activeModel, activeApi, 5);
    } catch (err) {
      console.error(`Cloud failed for ${path.basename(filePath)}. Switching to nyx.local fallback...`);
      const localApi = 'http://nyx.local:11434/v1/chat/completions';
      const localModel = 'gemma4:26b-a4b-it-q4_K_M'; // Optimized model for nyx
      translated = await translateText(content, lang, localModel, localApi, 10);
    }
    
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    fs.writeFileSync(targetPath, translated);
    console.log(`Saved to ${targetPath}`);
  } catch (err) {
    console.error(`Final failure for ${filePath} even with local fallback: ${err.message}`);
  }
}

async function main() {
  const lang = process.argv[2];
  const force = process.argv.includes('--force');
  
  // Allow model override via --model <model_name>
  let currentModel = MODEL;
  const modelIdx = process.argv.indexOf('--model');
  if (modelIdx > -1 && process.argv[modelIdx + 1]) {
    currentModel = process.argv[modelIdx + 1];
  }

  // Allow API override via --api <url>
  let activeApi = API_URL;
  const apiIdx = process.argv.indexOf('--api');
  if (apiIdx > -1 && process.argv[apiIdx + 1]) {
    activeApi = process.argv[apiIdx + 1];
  }

  // Allow limit via --limit <number>
  let limit = Infinity;
  const limitIdx = process.argv.indexOf('--limit');
  if (limitIdx > -1 && process.argv[limitIdx + 1]) {
    limit = parseInt(process.argv[limitIdx + 1]);
  }

  if (!CONFIG[lang]) {
    console.error('Usage: node scripts/translate.mjs <it|es|nl|hi|uk|ru|bg|ta> [--force] [--model <model_name>] [--limit <number>]');
    process.exit(1);
  }

  // Update global-like model for this run
  const activeModel = currentModel;

  const specificFiles = process.argv.filter(arg => arg.endsWith('.md'));
  let files = [];

  if (specificFiles.length > 0) {
    console.log(`Translating specific files: ${specificFiles.join(', ')}`);
    files = specificFiles.map(f => path.join(f.startsWith('docs/') ? '' : 'docs', f));
  } else {
    const dirs = ['lektionen', 'uebungen', 'schrift'];
    for (const dir of dirs) {
      const dirPath = path.join('docs', dir);
      if (fs.existsSync(dirPath)) {
        const dirFiles = fs.readdirSync(dirPath)
          .filter(f => f.endsWith('.md'))
          .map(f => path.join(dirPath, f));
        files = files.concat(dirFiles);
      }
    }

    const rootFiles = fs.readdirSync('docs')
      .filter(f => f.endsWith('.md') && !['index.md'].includes(f))
      .map(f => path.join('docs', f));
    files = files.concat(rootFiles);

    files.sort((a, b) => fs.statSync(a).size - fs.statSync(b).size);
  }

  if (limit < Infinity && specificFiles.length === 0) {
    console.log(`Limiting to first ${limit} files.`);
    files = files.slice(0, limit);
  }

  const CONCURRENCY = 1;
  console.log(`Found ${files.length} files to translate. Using concurrency: ${CONCURRENCY}`);

  for (let i = 0; i < files.length; i += CONCURRENCY) {
    const chunk = files.slice(i, i + CONCURRENCY);
    await Promise.all(chunk.map(file => processFile(file, lang, activeModel, activeApi, force)));
  }

  console.log(`Finished translating ${CONFIG[lang].name}. Running link fixer...`);
  try {
    execSync(`node scripts/fix_links_locale.mjs ${lang}`, { stdio: 'inherit' });
  } catch (err) {
    console.error(`Failed to run link fixer: ${err.message}`);
  }
}

main();
