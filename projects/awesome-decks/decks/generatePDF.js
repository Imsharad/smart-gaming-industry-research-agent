#!/usr/bin/env node

const puppeteer = require('puppeteer');
const path = require('path');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

// ============================================
// DIRECTORY CONFIGURATION
// ============================================
const HTML_DIR = path.join(__dirname, 'html');
const PDF_DIR = path.join(__dirname, 'pdf');

// ============================================
// QUALITY SETTINGS (adjust these if needed)
// ============================================
const QUALITY = {
  deviceScaleFactor: 3,  // 2=good, 3=excellent (default), 4=overkill
  waitTime: 100,         // ms to wait between slides (higher = better font loading)
  optimizeForSpeed: false // false = prioritize quality
};

// Ensure pdf directory exists
if (!fs.existsSync(PDF_DIR)) {
  fs.mkdirSync(PDF_DIR, { recursive: true });
}

// Get list of HTML files to convert
function getFilesToConvert() {
  const arg = process.argv[2];
  
  if (!arg || arg === '--all') {
    // Convert all HTML files in html directory
    const files = fs.readdirSync(HTML_DIR)
      .filter(f => f.endsWith('.html'))
      .map(f => path.basename(f, '.html'));
    
    if (files.length === 0) {
      console.error('No HTML files found in html/ directory');
      process.exit(1);
    }
    return files;
  }
  
  // Single file - strip path and extension if provided
  let filename = path.basename(arg, '.html');
  return [filename];
}

// Convert a single HTML file to PDF
async function convertToPDF(browser, filename) {
  const htmlPath = path.join(HTML_DIR, `${filename}.html`);
  const pdfPath = path.join(PDF_DIR, `${filename}.pdf`);
  
  if (!fs.existsSync(htmlPath)) {
    console.error(`❌ File not found: ${htmlPath}`);
    return false;
  }
  
  const startTime = Date.now();
  console.log(`\n📄 Converting: ${filename}.html`);
  
  const page = await browser.newPage();
  await page.setViewport({
    width: 1280,
    height: 720,
    deviceScaleFactor: QUALITY.deviceScaleFactor
  });

  await page.goto(`file://${htmlPath}`, {
    waitUntil: 'networkidle0'
  });

  // Force font rendering quality
  await page.evaluateOnNewDocument(() => {
    document.documentElement.style.webkitFontSmoothing = 'antialiased';
    document.documentElement.style.mozOsxFontSmoothing = 'grayscale';
  });

  const slideCount = await page.evaluate(() => {
    return document.querySelectorAll('.slide-container').length;
  });

  console.log(`   Found ${slideCount} slides`);

  // Setup PDF export CSS once
  await page.evaluate(() => {
    if (!document.getElementById('pdf-export-style')) {
      const style = document.createElement('style');
      style.id = 'pdf-export-style';
      style.textContent = `
        /* Disable ALL animations and transitions */
        body.pdf-export *, body.pdf-export *::before, body.pdf-export *::after {
          animation: none !important;
          transition: none !important;
        }

        body.pdf-export {
          margin: 0 !important;
          padding: 0 !important;
          width: 1280px !important;
          height: 720px !important;
          overflow: hidden !important;
          display: block !important;
          background-color: var(--bg-color, #fdfbf7) !important;
        }
        body.pdf-export::before { display: none !important; }

        /* Force FULL opacity on everything */
        body.pdf-export .slide-container,
        body.pdf-export .slide-container * {
          opacity: 1 !important;
        }

        body.pdf-export .slide-container {
          position: absolute !important;
          top: 0 !important;
          left: 0 !important;
          transform: none !important;
          transform-origin: top left !important;
          margin: 0 !important;
          border-radius: 0 !important;
        }
        body.pdf-export .slide-container.section-divider {
          background-color: #1c1917 !important;
        }

        /* Force text colors to be fully opaque */
        body.pdf-export .slide-container h1,
        body.pdf-export .slide-container h2,
        body.pdf-export .slide-container h3,
        body.pdf-export .slide-container h4,
        body.pdf-export .slide-container p,
        body.pdf-export .slide-container li,
        body.pdf-export .slide-container span,
        body.pdf-export .slide-container div {
          opacity: 1 !important;
        }

        /* Override any rgba colors with low opacity */
        body.pdf-export .slide-footer,
        body.pdf-export .slide-footer * {
          color: #57534e !important;
          opacity: 1 !important;
        }

        /* Ensure primary text is dark enough */
        body.pdf-export .slide-container .slide-title {
          color: #1c1917 !important;
        }

        /* Secondary text should be visible */
        body.pdf-export .slide-container p,
        body.pdf-export .slide-container li {
          color: #44403c !important;
        }
      `;
      document.head.appendChild(style);
    }
    document.body.classList.add('pdf-export');
    document.documentElement.style.setProperty('--scale', '1');
  });

  // Render all slides
  const screenshots = [];
  for (let i = 0; i < slideCount; i++) {
    process.stdout.write(`\r   Rendering slide ${i + 1}/${slideCount}...`);
    
    await page.evaluate((idx) => {
      const slides = document.querySelectorAll('.slide-container');
      slides.forEach((slide, i) => {
        if (i === idx) {
          slide.classList.add('active');
          slide.style.display = 'flex';
          slide.style.opacity = '1';
          slide.style.position = 'absolute';
          slide.style.top = '0';
          slide.style.left = '0';
          slide.style.transform = 'none';
          slide.style.width = '1280px';
          slide.style.height = '720px';
          slide.style.overflow = 'hidden';
          slide.style.margin = '0';
        } else {
          slide.classList.remove('active');
          slide.style.display = 'none';
        }
      });

      const navControls = document.querySelector('.nav-controls');
      if (navControls) navControls.style.display = 'none';
      const footerTemplate = document.getElementById('footer-template');
      if (footerTemplate) footerTemplate.style.display = 'none';
    }, i);

    await new Promise(resolve => setTimeout(resolve, QUALITY.waitTime));

    screenshots.push(await page.screenshot({
      type: 'png',
      clip: { x: 0, y: 0, width: 1280, height: 720 },
      omitBackground: false,
      optimizeForSpeed: QUALITY.optimizeForSpeed
    }));
  }
  console.log(); // New line after progress

  await page.close();

  // Build PDF
  const pdfDoc = await PDFDocument.create();
  for (const screenshot of screenshots) {
    const pngImage = await pdfDoc.embedPng(screenshot);
    const pdfPage = pdfDoc.addPage([1280, 720]);
    pdfPage.drawImage(pngImage, {
      x: 0,
      y: 0,
      width: 1280,
      height: 720
    });
  }

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(pdfPath, pdfBytes);

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
  console.log(`   ✓ Generated: pdf/${filename}.pdf (${slideCount} pages in ${elapsed}s)`);
  
  return true;
}

// Main
(async () => {
  const files = getFilesToConvert();
  const totalStartTime = Date.now();
  
  console.log('═══════════════════════════════════════════');
  console.log('  HTML to PDF Converter');
  console.log('═══════════════════════════════════════════');
  console.log(`Files to convert: ${files.length}`);
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--no-first-run',
      '--no-zygote',
      '--single-process',
      '--disable-extensions',
      '--disable-background-networking',
      '--disable-background-timer-throttling',
      '--disable-renderer-backgrounding'
    ]
  });

  let successCount = 0;
  for (const file of files) {
    const success = await convertToPDF(browser, file);
    if (success) successCount++;
  }

  await browser.close();

  const totalElapsed = ((Date.now() - totalStartTime) / 1000).toFixed(2);
  console.log('\n═══════════════════════════════════════════');
  console.log(`✓ Complete: ${successCount}/${files.length} files converted in ${totalElapsed}s`);
  console.log('═══════════════════════════════════════════');
})();
