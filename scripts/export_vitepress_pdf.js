const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const EXPORT_DIR = path.join(ROOT, 'dist_exports');
const PKG = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf-8'));
const VERSION = PKG.version || '1.6.4';

function getDistDir() {
  const distPublic = path.join(ROOT, 'docs', '.vitepress', 'dist-public');
  if (fs.existsSync(distPublic)) return distPublic;
  const distStandard = path.join(ROOT, 'docs', '.vitepress', 'dist');
  if (fs.existsSync(distStandard)) return distStandard;
  return null;
}

async function exportVitePressMedia(lang = 'de') {
  console.log(`📄 Generating pixel-perfect VitePress PDF & EPUB for [${lang}] (Version v${VERSION})...`);
  if (!fs.existsSync(EXPORT_DIR)) {
    fs.mkdirSync(EXPORT_DIR, { recursive: true });
  }

  const DIST_DIR = getDistDir();
  if (!DIST_DIR) {
    console.log(`⚠️ Dist directory not found. Run 'npm run docs:build' first.`);
    return;
  }

  console.log(`Using VitePress build output at: ${DIST_DIR}`);

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

  // Build Table of Contents entries dynamically
  let tocItemsHtml = '';
  const lessonsData = [];

  for (const fullPath of htmlFilePaths) {
    let content = fs.readFileSync(fullPath, 'utf-8');
    const filename = path.basename(fullPath, '.html');
    const lessonNum = parseInt((filename.match(/\d+/) || [0])[0], 10);

    // Extract lesson title from <h1> tag
    const h1Match = content.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    let title = `Lektion ${lessonNum}`;
    if (h1Match) {
      title = h1Match[1].replace(/<[^>]+>/g, '').trim();
    }

    lessonsData.push({ lessonNum, title, fullPath });
    tocItemsHtml += `<li style="margin-bottom: 8px;"><a href="#lektion-${lessonNum}" style="color: #03192e; text-decoration: none;"><strong>Lektion ${lessonNum}:</strong> ${title}</a></li>\n`;
  }

  let combinedHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Sanskritkurs Payer (${lang.toUpperCase()}) - v${VERSION}</title>
  <style>
    ${cssStyles}
    @media print {
      .page-break { page-break-before: always; break-before: page; }
      nav, .VPNav, .VPSidebar, .VPFooter, .next-and-prev-link, .VPLocalNav { display: none !important; }
      body { background: #fcf9f2 !important; color: #03192e !important; font-family: "Newsreader", serif !important; }
    }
  </style>
</head>
<body class="vp-doc">
  <!-- Title Page -->
  <div style="padding: 100px 40px 60px; page-break-after: always; text-align: center;">
    <h1 style="font-size: 42px; color: #03192e; margin-bottom: 12px;">Sanskritkurs Payer</h1>
    <h2 style="font-size: 24px; color: #48626e; margin-bottom: 30px;">Ein vollständiger Lehrgang von Alois Payer</h2>
    <div style="font-size: 16px; font-weight: bold; color: #241500; margin-bottom: 40px;">Sprachversion: ${lang.toUpperCase()} &bull; Version v${VERSION}</div>
    <hr style="margin: 40px 0; border: 0; border-top: 2px solid #48626e;">
  </div>

  <!-- Page 2: Impressum & Legal Copyright Notice -->
  <div style="padding: 40px; page-break-after: always;">
    <div style="max-width: 650px; margin: 0 auto; font-size: 15px; line-height: 1.8; border: 1px solid #48626e; padding: 35px; border-radius: 8px; background: #f1eee7;">
      <h3 style="font-size: 22px; color: #241500; margin-top: 0;">Impressum &amp; Urheberrechtshinweis / Copyright Notice</h3>
      <ul>
        <li><strong>Originalautor:</strong> Alois Payer (Tüpfli's Global Village Library)</li>
        <li><strong>Herausgeber &amp; Digitalisierung:</strong> Sanskritkurs Payer Project</li>
        <li><strong>Version:</strong> Release v${VERSION}</li>
        <li><strong>Webmaster &amp; Kontakt:</strong> webmaster@birchville.cc</li>
        <li><strong>Lektorat &amp; Mitarbeit:</strong> onboarding@birchville.cc</li>
        <li><strong>Open-Source Editor:</strong> https://github.com/marcodem/zentauri</li>
        <li><strong>Lizenz &amp; Quellen:</strong> Vollständiges Quellen- &amp; Lizenzverzeichnis im Anhang (licenses.md)</li>
        <li><strong>Dokument-Typ:</strong> Offizielles Release-Artefakt (Sanskritkurs Payer Project)</li>
      </ul>
    </div>
  </div>

  <!-- Page 3: Table of Contents / Inhaltsverzeichnis -->
  <div style="padding: 40px; page-break-after: always;">
    <h2 style="font-size: 28px; color: #03192e; border-bottom: 2px solid #03192e; padding-bottom: 10px; margin-bottom: 25px;">Inhaltsverzeichnis / Table of Contents</h2>
    <ol style="column-count: 2; column-gap: 40px; font-size: 14px; line-height: 1.6; list-style: none; padding-left: 0;">
      ${tocItemsHtml}
    </ol>
  </div>
`;

  for (const item of lessonsData) {
    let content = fs.readFileSync(item.fullPath, 'utf-8');

    // Rewrite relative image src="/images/..." to absolute file:/// URLs
    content = content.replace(/src="\/images\//g, `src="file://${DIST_DIR}/images/`);

    const match = content.match(/<main[^>]*>([\s\S]*?)<\/main>/i) || content.match(/<div class="vp-doc[^"]*">([\s\S]*?)<\/div>/i);
    if (match) {
      combinedHtml += `<div id="lektion-${item.lessonNum}" class="page-break" style="padding: 30px 20px;">${match[1]}</div>`;
    }
  }

  combinedHtml += `</body></html>`;

  const tmpHtmlPath = path.join(EXPORT_DIR, `temp_${lang}.html`);
  fs.writeFileSync(tmpHtmlPath, combinedHtml, 'utf-8');

  // 1. Generate PDF via Playwright (Headless Chromium) with header & footer versioning
  await page.goto(`file://${tmpHtmlPath}`, { waitUntil: 'networkidle' });
  const pdfPath = path.join(EXPORT_DIR, `Sanskritkurs_Payer_${lang.toUpperCase()}.pdf`);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: `<div style="font-size: 9px; font-family: sans-serif; width: 100%; text-align: right; padding-right: 15mm; color: #48626e;">Sanskritkurs Payer (${lang.toUpperCase()}) &bull; Release v${VERSION}</div>`,
    footerTemplate: `<div style="font-size: 9px; font-family: sans-serif; width: 100%; text-align: center; color: #48626e;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
    margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' }
  });
  console.log(`✅ Saved pixel-perfect VitePress PDF: ${pdfPath}`);
  await browser.close();

  // 2. Generate EPUB via Pandoc from rendered HTML
  const epubPath = path.join(EXPORT_DIR, `Sanskritkurs_Payer_${lang.toUpperCase()}.epub`);
  try {
    execSync(`pandoc "${tmpHtmlPath}" -o "${epubPath}" --toc --metadata title="Sanskritkurs Payer (${lang.toUpperCase()})" --metadata author="Alois Payer" --metadata version="v${VERSION}"`, { stdio: 'inherit' });
    console.log(`✅ Saved pixel-perfect VitePress EPUB: ${epubPath}`);
  } catch (err) {
    console.log(`⚠️ EPUB conversion via pandoc skipped: ${err.message}`);
  }
}

const targetLang = process.argv[2] || 'de';
exportVitePressMedia(targetLang);
