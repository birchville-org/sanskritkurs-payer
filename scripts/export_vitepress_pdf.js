const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const EXPORT_DIR = path.join(ROOT, 'dist_exports');

function getDistDir() {
  const distPublic = path.join(ROOT, 'docs', '.vitepress', 'dist-public');
  if (fs.existsSync(distPublic)) return distPublic;
  const distStandard = path.join(ROOT, 'docs', '.vitepress', 'dist');
  if (fs.existsSync(distStandard)) return distStandard;
  return null;
}

async function exportVitePressMedia(lang = 'de') {
  console.log(`📄 Generating pixel-perfect VitePress PDF & EPUB for [${lang}]...`);
  if (!fs.existsSync(EXPORT_DIR)) {
    fs.mkdirSync(EXPORT_DIR, { recursive: true });
  }

  const DIST_DIR = getDistDir();
  if (!DIST_DIR) {
    console.log(`⚠️ Dist directory not found. Run 'npm run docs:build' first.`);
    return;
  }

  console.log(`Using VitePress build output at: ${DIST_DIR}`);

  // Find all CSS asset files to include full VitePress styling
  const assetsDir = path.join(DIST_DIR, 'assets');
  let cssStyles = '';
  if (fs.existsSync(assetsDir)) {
    const cssFiles = fs.readdirSync(assetsDir).filter(f => f.endsWith('.css'));
    for (const cssFile of cssFiles) {
      const cssPath = path.join(assetsDir, cssFile);
      cssStyles += fs.readFileSync(cssPath, 'utf-8') + '\n';
    }
  }

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1200, height: 1600 }
  });

  const searchBase = lang === 'de' ? DIST_DIR : path.join(DIST_DIR, lang);
  const htmlFilePaths = [];

  function searchDir(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        searchDir(fullPath);
      } else if (entry.isFile() && entry.name.startsWith('lektion') && entry.name.endsWith('.html')) {
        htmlFilePaths.push(fullPath);
      }
    }
  }

  searchDir(searchBase);

  // Sort lesson files numerically (lektion01.html, lektion02.html, ...)
  htmlFilePaths.sort((a, b) => {
    const na = parseInt((path.basename(a).match(/\d+/) || [0])[0], 10);
    const nb = parseInt((path.basename(b).match(/\d+/) || [0])[0], 10);
    return na - nb;
  });

  console.log(`Injecting ${htmlFilePaths.length} rendered lesson pages with full CSS styling & images...`);

  let combinedHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Sanskritkurs Payer (${lang.toUpperCase()})</title>
  <style>
    ${cssStyles}
    @media print {
      .page-break { page-break-after: always; break-after: page; }
      nav, .VPNav, .VPSidebar, .VPFooter, .next-and-prev-link, .VPLocalNav { display: none !important; }
      body { background: #fcf9f2 !important; color: #03192e !important; font-family: "Newsreader", serif !important; }
    }
  </style>
</head>
<body class="vp-doc">
  <div style="padding: 60px 40px; page-break-after: always; text-align: center;">
    <h1 style="font-size: 38px; color: #03192e; margin-bottom: 10px;">Sanskritkurs Payer (${lang.toUpperCase()})</h1>
    <h2 style="font-size: 22px; color: #48626e; margin-bottom: 40px;">Ein vollständiger Lehrgang von Alois Payer</h2>
    <hr style="margin: 30px 0; border: 0; border-top: 1px solid #48626e;">
    <div style="text-align: left; max-width: 650px; margin: 40px auto; font-size: 16px; line-height: 1.8; border: 1px solid #48626e; padding: 30px; border-radius: 8px; background: #f1eee7;">
      <h3 style="font-size: 20px; color: #241500; margin-top: 0;">Impressum &amp; Urheberrechtshinweis / Copyright Notice</h3>
      <ul>
        <li><strong>Originalautor:</strong> Alois Payer (Tüpfli's Global Village Library)</li>
        <li><strong>Herausgeber &amp; Digitalisierung:</strong> Sanskritkurs Payer Project</li>
        <li><strong>Webmaster &amp; Kontakt:</strong> webmaster@birchville.cc</li>
        <li><strong>Lektorat &amp; Mitarbeit:</strong> onboarding@birchville.cc</li>
        <li><strong>Open-Source Editor:</strong> https://github.com/marcodem/zentauri</li>
        <li><strong>Lizenz &amp; Quellen:</strong> Vollständiges Quellen- &amp; Lizenzverzeichnis im Anhang (licenses.md)</li>
        <li><strong>Dokument-Typ:</strong> Offizielles Artefakt (Sanskritkurs Payer Project)</li>
      </ul>
    </div>
  </div>
`;

  for (const fullPath of htmlFilePaths) {
    let content = fs.readFileSync(fullPath, 'utf-8');

    // Rewrite relative image src="/images/..." to absolute file:/// URLs
    content = content.replace(/src="\/images\//g, `src="file://${DIST_DIR}/images/`);

    const match = content.match(/<main[^>]*>([\s\S]*?)<\/main>/i) || content.match(/<div class="vp-doc[^"]*">([\s\S]*?)<\/div>/i);
    if (match) {
      combinedHtml += `<div class="page-break" style="padding: 30px;">${match[1]}</div>`;
    }
  }

  combinedHtml += `</body></html>`;

  const tmpHtmlPath = path.join(EXPORT_DIR, `temp_${lang}.html`);
  fs.writeFileSync(tmpHtmlPath, combinedHtml, 'utf-8');

  // 1. Generate PDF via Playwright (Headless Chromium)
  await page.goto(`file://${tmpHtmlPath}`, { waitUntil: 'networkidle' });
  const pdfPath = path.join(EXPORT_DIR, `Sanskritkurs_Payer_${lang.toUpperCase()}.pdf`);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' }
  });
  console.log(`✅ Saved pixel-perfect VitePress PDF: ${pdfPath}`);
  await browser.close();

  // 2. Generate EPUB via Pandoc from rendered HTML
  const epubPath = path.join(EXPORT_DIR, `Sanskritkurs_Payer_${lang.toUpperCase()}.epub`);
  try {
    execSync(`pandoc "${tmpHtmlPath}" -o "${epubPath}" --toc`, { stdio: 'inherit' });
    console.log(`✅ Saved pixel-perfect VitePress EPUB: ${epubPath}`);
  } catch (err) {
    console.log(`⚠️ EPUB conversion via pandoc skipped: ${err.message}`);
  }
}

const targetLang = process.argv[2] || 'de';
exportVitePressMedia(targetLang);
