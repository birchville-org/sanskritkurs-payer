import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', error => console.log('BROWSER ERROR:', error.message));
  
  await page.goto('http://localhost:5173/arc/settings', { waitUntil: 'networkidle0' });
  
  const content = await page.content();
  if (content.includes('language-settings')) {
    console.log("Settings component rendered!");
  } else {
    console.log("Settings component NOT rendered.");
  }
  
  await browser.close();
})();
