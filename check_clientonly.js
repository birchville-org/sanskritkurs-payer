import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  await page.goto('http://localhost:5173/settings', { waitUntil: 'networkidle0' });
  
  const content = await page.content();
  if (content.includes('&lt;ClientOnly&gt;')) {
    console.log("ClientOnly is rendered as text!");
  } else {
    console.log("ClientOnly is NOT rendered as text.");
  }
  
  await browser.close();
})();
