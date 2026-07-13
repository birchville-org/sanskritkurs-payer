const { chromium } = require('playwright');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

async function generatePDF() {
  console.log('Starte lokalen Server...');
  // Start python http server in docs/.vitepress/dist
  const server = spawn('python3', ['-m', 'http.server', '8080', '-d', 'docs/.vitepress/dist']);
  
  // Wait a bit for server to start
  await new Promise(resolve => setTimeout(resolve, 2000));

  console.log('Starte Playwright Chromium...');
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Array to hold the PDF bytes of each page
  const pdfBuffers = [];

  console.log('Erzeuge Cover-Seite...');
  // wir erstellen später ein neues PDFDocument und laden das Bild

  console.log('Drucke Lektionen 1 bis 61...');
  for (let i = 1; i <= 61; i++) {
    const num = i.toString().padStart(2, '0');
    const url = `http://localhost:8080/lektionen/lektion${num}.html`;
    console.log(`Lade ${url}...`);
    
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    } catch (e) {
      console.log(`Timeout bei Lektion ${num}, drucke trotzdem...`);
    }
    
    // Wait for any potential hydration or fonts
    await page.waitForTimeout(2000);
    
    try {
      const pdfBuffer = await page.pdf({
        format: 'A4',
        printBackground: true,
        margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' }
      });
      pdfBuffers.push(pdfBuffer);
    } catch (e) {
      console.error(`Fataler Fehler beim Drucken von Lektion ${num}:`, e);
    }
  }

  await browser.close();
  server.kill(); // Shutdown server

  console.log('Füge alle Seiten zu einem Master-PDF zusammen...');
  const mergedPdf = await PDFDocument.create();
  
  // Add Cover Image
  if (fs.existsSync('docs/public/images/cover.png')) {
    console.log('Füge Cover hinzu...');
    const coverImageBytes = fs.readFileSync('docs/public/images/cover.png');
    // generate_image created a JPEG despite the .png extension
    const coverImage = await mergedPdf.embedJpg(coverImageBytes).catch(async () => {
      return await mergedPdf.embedPng(coverImageBytes);
    });
    
    // A4 dimensions in points: 595.28 x 841.89
    const a4Width = 595.28;
    const a4Height = 841.89;
    
    const coverPage = mergedPdf.addPage([a4Width, a4Height]);
    
    // Scale image to fill page
    const scale = Math.max(a4Width / coverImage.width, a4Height / coverImage.height);
    const drawWidth = coverImage.width * scale;
    const drawHeight = coverImage.height * scale;
    
    // Center image
    const x = (a4Width - drawWidth) / 2;
    const y = (a4Height - drawHeight) / 2;
    
    coverPage.drawImage(coverImage, {
      x, y, width: drawWidth, height: drawHeight
    });
  }

  // Merge Lektionen
  for (const buffer of pdfBuffers) {
    const tempPdf = await PDFDocument.load(buffer);
    const copiedPages = await mergedPdf.copyPages(tempPdf, tempPdf.getPageIndices());
    copiedPages.forEach((page) => mergedPdf.addPage(page));
  }

  const outputPath = 'docs/public/downloads/Payer_Sanskritkurs_de.pdf';
  if (!fs.existsSync('docs/public/downloads')) {
    fs.mkdirSync('docs/public/downloads', { recursive: true });
  }

  console.log(`Speichere Buch unter ${outputPath}...`);
  const finalPdfBytes = await mergedPdf.save();
  fs.writeFileSync(outputPath, finalPdfBytes);
  
  console.log('Fertig! 🎉');
  process.exit(0);
}

generatePDF().catch(console.error);
