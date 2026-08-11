const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const MarkdownIt = require('markdown-it');
const container = require('markdown-it-container');
const { PDFDocument, PDFName, PDFString } = require('pdf-lib');

const ROOT = path.join(__dirname, '..');
const EXPORT_DIR = path.join(ROOT, 'dist_exports');
const PKG = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf-8'));
const VERSION = PKG.version || '1.6.4';

// Setup MarkdownIt with VitePress-compatible container extensions
const md = new MarkdownIt({ html: true, linkify: true, breaks: false });
['grammar-box', 'media', 'indent', 'deleteme-box', 'center', 'no-header', 'laut-table'].forEach(c => {
  md.use(container, c);
});

// Custom inline replacements for Signalrot and Sanskrit brackets
function renderMarkdownContent(rawMarkdown) {
  let body = rawMarkdown.replace(/^---[\s\S]*?---\s*/, '');

  // Convert Signalrot sig[...] -> <span class="sig">...</span>
  body = body.replace(/sig\[([^\]]+)\]/g, '<span class="sig">$1</span>');

  // Convert Sanskrit ⟪...⟫ -> <span class="sanskrit">...</span> (never red, never italic)
  body = body.replace(/⟪([^⟫]+)⟫/g, '<span class="sanskrit">$1</span>');

  // Replace image paths with local file:/// URLs
  const publicImgDir = path.join(ROOT, 'docs', 'public', 'images');
  body = body.replace(/!\[(.*?)\]\(\/images\/([^)]+)\)/g, (match, alt, filename) => {
    const absPath = path.join(publicImgDir, filename);
    return `<img src="file://${absPath}" alt="${alt}" style="max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 4px;" />`;
  });

  return md.render(body);
}

const COMMON_CSS = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap');

body {
  background-color: #fcf9f2 !important;
  color: #03192e !important;
  font-family: "Source Serif 4", Georgia, serif !important;
  font-size: 18px !important;
  line-height: 1.7 !important;
  margin: 0;
  padding: 30px 40px;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

h1, h2, h3, h4 {
  font-family: "Source Serif 4", serif !important;
  color: #03192e !important;
}

h1 {
  font-size: 34px !important;
  border-top: 1px solid #a1a1a1;
  padding-top: 1.2rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

h2 {
  font-size: 26px !important;
  font-weight: 500;
  color: #241500 !important;
  border-top: 1px solid #a1a1a1;
  padding-top: 1rem;
  margin-top: 2.2rem;
  margin-bottom: 0.8rem;
}

h3 {
  font-size: 20px !important;
  font-weight: 500;
  color: #48626e !important;
  border-top: 1px solid #a1a1a1;
  padding-top: 0.8rem;
  margin-top: 1.8rem;
  margin-bottom: 0.6rem;
}

p, li {
  font-size: 18px !important;
  line-height: 1.7 !important;
  margin-bottom: 1rem;
}

table {
  width: 100% !important;
  border-collapse: collapse !important;
  margin: 1.5rem 0 !important;
  border: 1px solid #94a3b8 !important;
  border-radius: 6px;
}

th, td {
  padding: 10px 14px !important;
  border: 1px solid #94a3b8 !important;
  font-size: 17px !important;
  line-height: 1.5 !important;
}

th {
  background-color: #f1eee7 !important;
  font-family: "Inter", sans-serif !important;
  font-weight: 600 !important;
  color: #03192e !important;
}

tr:nth-child(even) {
  background-color: #f1eee7 !important;
}

.grammar-box, .custom-block.grammar-box, blockquote {
  background-color: #f1eee7 !important;
  border-left: 4px solid #03192e !important;
  padding: 1.2rem 1.5rem !important;
  margin: 1.5rem 0 !important;
  border-radius: 0 4px 4px 0 !important;
}

.indent {
  margin-left: 2rem !important;
  padding-left: 1rem !important;
  border-left: 2px solid #f1eee7 !important;
}

.sig {
  color: #d32f2f !important;
  font-weight: bold !important;
}

.sanskrit {
  color: #03192e !important;
  font-style: normal !important;
  font-size: 1.15em !important;
  font-weight: 600 !important;
}
`;

function buildPageHtml(title, bodyContent) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>${title}</title>
  <style>${COMMON_CSS}</style>
</head>
<body class="vp-doc">
  ${bodyContent}
</body>
</html>`;
}

async function exportVitePressMedia(lang = 'de') {
  console.log(`📄 Generating pixel-perfect PDF & EPUB for [${lang}] (Version v${VERSION}) directly from Markdown sources...`);
  if (!fs.existsSync(EXPORT_DIR)) {
    fs.mkdirSync(EXPORT_DIR, { recursive: true });
  }

  const lektionenDir = lang === 'de'
    ? path.join(ROOT, 'docs', 'lektionen')
    : path.join(ROOT, 'docs', lang, 'lektionen');

  if (!fs.existsSync(lektionenDir)) {
    console.log(`⚠️ Lektionen directory not found at: ${lektionenDir}`);
    return;
  }

  const files = fs.readdirSync(lektionenDir)
    .filter(f => f.startsWith('lektion') && f.endsWith('.md'))
    .sort((a, b) => {
      const na = parseInt((a.match(/\d+/) || [0])[0], 10);
      const nb = parseInt((b.match(/\d+/) || [0])[0], 10);
      return na - nb;
    });

  console.log(`Processing ${files.length} authentic Markdown lesson files...`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage({ viewport: { width: 1200, height: 1600 } });

  const mergedPdfDoc = await PDFDocument.create();
  const bookmarks = []; // { title: string, pageIndex: number }

  // 1. Title Page (Cover)
  const coverHtml = buildPageHtml('Title Page', `
    <div style="padding: 120px 40px 60px; text-align: center;">
      <h1 style="font-size: 46px !important; color: #03192e; margin-bottom: 16px; border: none; padding: 0;">Sanskritkurs Payer</h1>
      <h2 style="font-size: 26px !important; color: #48626e; margin-bottom: 35px; border: none; padding: 0;">Ein vollständiger Lehrgang von Alois Payer</h2>
      <div style="font-size: 18px; font-weight: bold; color: #241500; margin-bottom: 50px;">Sprachversion: ${lang.toUpperCase()} &bull; Version v${VERSION}</div>
      <hr style="margin: 50px 0; border: 0; border-top: 2px solid #48626e;">
    </div>
  `);
  await page.setContent(coverHtml, { waitUntil: 'load' });
  const coverPdfBuffer = await page.pdf({ format: 'A4', printBackground: true, margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' } });
  const coverDoc = await PDFDocument.load(coverPdfBuffer);
  const coverPages = await mergedPdfDoc.copyPages(coverDoc, coverDoc.getPageIndices());
  coverPages.forEach(p => mergedPdfDoc.addPage(p));
  bookmarks.push({ title: 'Titelblatt', pageIndex: 0 });

  // 2. Page 2: Impressum & Legal Copyright Notice
  const impressumHtml = buildPageHtml('Impressum', `
    <div style="padding: 40px 20px;">
      <div style="max-width: 700px; margin: 0 auto; font-size: 16px; line-height: 1.8; border: 1px solid #48626e; padding: 40px; border-radius: 8px; background: #f1eee7;">
        <h3 style="font-size: 24px !important; color: #241500; margin-top: 0; border: none; padding: 0;">Impressum &amp; Urheberrechtshinweis / Copyright Notice</h3>
        <ul style="line-height: 1.8;">
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
  `);
  await page.setContent(impressumHtml, { waitUntil: 'load' });
  const impressumPdfBuffer = await page.pdf({ format: 'A4', printBackground: true, margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' } });
  const impressumDoc = await PDFDocument.load(impressumPdfBuffer);
  const impressumPages = await mergedPdfDoc.copyPages(impressumDoc, impressumDoc.getPageIndices());
  impressumPages.forEach(p => mergedPdfDoc.addPage(p));
  bookmarks.push({ title: 'Impressum & Rechtliches', pageIndex: 1 });

  // Pre-process lesson metadata and TOC items
  const lessonsData = [];
  let tocItemsHtml = '';

  for (const filename of files) {
    const filePath = path.join(lektionenDir, filename);
    const rawMarkdown = fs.readFileSync(filePath, 'utf-8');
    const lessonNum = parseInt((filename.match(/\d+/) || [0])[0], 10);

    let displayTitle = `Lektion ${lessonNum}`;
    const subMatch = rawMarkdown.match(/^subtitle:\s*["']?([^"'\n]+)["']?/m);
    if (subMatch && subMatch[1].trim()) {
      displayTitle = `Lektion ${lessonNum}: ${subMatch[1].trim()}`;
    }

    const h2Matches = [...rawMarkdown.matchAll(/^##\s+(.+)$/gm)];
    const subHeadings = [];
    for (const m of h2Matches) {
      const cleanH2 = m[1].replace(/[*_#]/g, '').trim();
      if (cleanH2 && cleanH2.length < 80 && !cleanH2.toLowerCase().includes('inhaltsverzeichnis') && !cleanH2.toLowerCase().includes('payer')) {
        subHeadings.push(cleanH2);
      }
    }

    const htmlContent = renderMarkdownContent(rawMarkdown);
    lessonsData.push({ lessonNum, displayTitle, subHeadings, htmlContent, rawMarkdown });

    let subListHtml = '';
    if (subHeadings.length > 0) {
      subListHtml = `<ul style="margin: 3px 0 10px 15px; padding-left: 10px; font-size: 13px; color: #48626e; list-style-type: disc;">` +
        subHeadings.slice(0, 4).map(sh => `<li>${sh}</li>`).join('') +
        `</ul>`;
    }

    tocItemsHtml += `<li style="margin-bottom: 14px; page-break-inside: avoid;">
      <span style="color: #03192e; font-weight: bold; font-size: 15px;">${displayTitle}</span>
      ${subListHtml}
    </li>\n`;
  }

  // 3. Table of Contents Pages
  const tocHtml = buildPageHtml('Inhaltsverzeichnis', `
    <div style="padding: 20px 10px;">
      <h2 style="font-size: 30px !important; color: #03192e; border-bottom: 2px solid #03192e; padding-bottom: 10px; margin-bottom: 30px; margin-top: 0;">Inhaltsverzeichnis / Table of Contents</h2>
      <ol style="column-count: 2; column-gap: 40px; font-size: 14px; line-height: 1.6; list-style: none; padding-left: 0;">
        ${tocItemsHtml}
      </ol>
    </div>
  `);
  await page.setContent(tocHtml, { waitUntil: 'load' });
  const tocPdfBuffer = await page.pdf({ format: 'A4', printBackground: true, margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' } });
  const tocDoc = await PDFDocument.load(tocPdfBuffer);
  const tocPages = await mergedPdfDoc.copyPages(tocDoc, tocDoc.getPageIndices());
  tocPages.forEach(p => mergedPdfDoc.addPage(p));
  bookmarks.push({ title: 'Inhaltsverzeichnis', pageIndex: 2 });

  // 4. Render each lesson into PDF, record EXACT start page index, and merge into master PDF
  let fullEpubBodyHtml = coverHtml + impressumHtml + tocHtml;

  for (const item of lessonsData) {
    const startPageIndex = mergedPdfDoc.getPageCount();
    bookmarks.push({ title: item.displayTitle, pageIndex: startPageIndex });

    const lessonPageHtml = buildPageHtml(item.displayTitle, item.htmlContent);
    fullEpubBodyHtml += `<div class="lesson-break" style="page-break-before: always;">${item.htmlContent}</div>`;

    await page.setContent(lessonPageHtml, { waitUntil: 'load' });
    const lessonPdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: `<div style="font-size: 10px; font-family: sans-serif; width: 100%; text-align: right; padding-right: 15mm; color: #48626e;">Sanskritkurs Payer (${lang.toUpperCase()}) &bull; Release v${VERSION}</div>`,
      footerTemplate: `<div style="font-size: 10px; font-family: sans-serif; width: 100%; text-align: center; color: #48626e;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
      margin: { top: '20mm', bottom: '20mm', left: '15mm', right: '15mm' }
    });

    const lessonDoc = await PDFDocument.load(lessonPdfBuffer);
    const copiedPages = await mergedPdfDoc.copyPages(lessonDoc, lessonDoc.getPageIndices());
    copiedPages.forEach(p => mergedPdfDoc.addPage(p));
  }

  await browser.close();

  // 5. Inject 100% Mathematically Precise PDF Sidebar Bookmarks (PDF Catalog Outlines)
  const pdfContext = mergedPdfDoc.context;
  const pageRefs = mergedPdfDoc.getPages().map(p => p.ref);

  const outlineDictRef = pdfContext.nextRef();
  const itemRefs = bookmarks.map(() => pdfContext.nextRef());

  for (let i = 0; i < bookmarks.length; i++) {
    const { title, pageIndex } = bookmarks[i];
    const validIndex = Math.min(Math.max(0, pageIndex), pageRefs.length - 1);
    const pageRef = pageRefs[validIndex];

    const itemDict = pdfContext.obj({
      Title: PDFString.of(title),
      Parent: outlineDictRef,
      Dest: [pageRef, PDFName.of('XYZ'), null, null, null],
    });

    if (i > 0) itemDict.set(PDFName.of('Prev'), itemRefs[i - 1]);
    if (i < bookmarks.length - 1) itemDict.set(PDFName.of('Next'), itemRefs[i + 1]);

    pdfContext.assign(itemRefs[i], itemDict);
  }

  const outlineDict = pdfContext.obj({
    Type: PDFName.of('Outlines'),
    First: itemRefs[0],
    Last: itemRefs[itemRefs.length - 1],
    Count: bookmarks.length,
  });
  pdfContext.assign(outlineDictRef, outlineDict);
  mergedPdfDoc.catalog.set(PDFName.of('Outlines'), outlineDictRef);

  const finalPdfPath = path.join(EXPORT_DIR, `Sanskritkurs_Payer_${lang.toUpperCase()}.pdf`);
  const finalPdfBytes = await mergedPdfDoc.save();
  fs.writeFileSync(finalPdfPath, finalPdfBytes);
  console.log(`✅ Saved publication-grade PDF (${mergedPdfDoc.getPageCount()} pages) with ${bookmarks.length} exact sidebar bookmarks: ${finalPdfPath}`);

  // 6. EPUB Export via Pandoc
  const tmpEpubHtmlPath = path.join(EXPORT_DIR, `temp_epub_${lang}.html`);
  fs.writeFileSync(tmpEpubHtmlPath, fullEpubBodyHtml, 'utf-8');
  const epubPath = path.join(EXPORT_DIR, `Sanskritkurs_Payer_${lang.toUpperCase()}.epub`);
  try {
    execSync(`pandoc "${tmpEpubHtmlPath}" -o "${epubPath}" --toc --metadata title="Sanskritkurs Payer (${lang.toUpperCase()})" --metadata author="Alois Payer" --metadata version="v${VERSION}"`, { stdio: 'inherit' });
    console.log(`✅ Saved EPUB: ${epubPath}`);
  } catch (err) {
    console.log(`⚠️ EPUB conversion warning: ${err.message}`);
  }
}

const targetLang = process.argv[2] || 'de';
exportVitePressMedia(targetLang);
