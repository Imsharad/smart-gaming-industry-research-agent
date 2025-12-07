const puppeteer = require('puppeteer');
const path = require('path');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Set viewport to match the slide dimensions exactly
  await page.setViewport({
    width: 1280,
    height: 720,
    deviceScaleFactor: 2  // 2x for retina quality
  });

  // Get the HTML filename from command line args or default to seed.html
  const htmlFile = process.argv[2] || 'seed.html';
  const pdfFile = htmlFile.replace('.html', '.pdf');

  // Load the HTML file
  const htmlPath = path.join(__dirname, htmlFile);
  await page.goto(`file://${htmlPath}`, {
    waitUntil: 'networkidle0'
  });

  // Get total number of slides
  const slideCount = await page.evaluate(() => {
    return document.querySelectorAll('.slide-container').length;
  });

  console.log(`Found ${slideCount} slides`);

  // Create a new PDF document
  const pdfDoc = await PDFDocument.create();

  // Iterate through each slide
  for (let i = 0; i < slideCount; i++) {
    console.log(`Rendering slide ${i + 1}/${slideCount}...`);

    // Show only the current slide and prepare for screenshot
    await page.evaluate((slideIndex) => {
      // Hide everything first
      document.body.style.margin = '0';
      document.body.style.padding = '0';
      document.body.style.background = '#0f172a';  // Match dark background
      document.body.style.overflow = 'hidden';

      // Remove the ::before pseudo-element glow by setting a class
      document.body.classList.add('pdf-export');

      // Add CSS to hide the pseudo-element
      if (!document.getElementById('pdf-export-style')) {
        const style = document.createElement('style');
        style.id = 'pdf-export-style';
        style.textContent = `
          body.pdf-export::before { display: none !important; }
          body.pdf-export {
            background-image:
              linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
            background-size: 40px 40px !important;
          }
        `;
        document.head.appendChild(style);
      }

      const slides = document.querySelectorAll('.slide-container');
      slides.forEach((slide, idx) => {
        if (idx === slideIndex) {
          slide.classList.add('active');
          slide.style.display = 'flex';
          slide.style.opacity = '1';
          // Position slide to fill viewport exactly
          slide.style.position = 'fixed';
          slide.style.top = '50%';
          slide.style.left = '50%';
          slide.style.transform = 'translate(-50%, -50%)';
          slide.style.width = '1280px';
          slide.style.height = '720px';
          slide.style.overflow = 'hidden';
          slide.style.margin = '0';
        } else {
          slide.classList.remove('active');
          slide.style.display = 'none';
        }
      });

      // Hide navigation controls
      const navControls = document.querySelector('.nav-controls');
      if (navControls) navControls.style.display = 'none';

      // Hide footer template
      const footerTemplate = document.getElementById('footer-template');
      if (footerTemplate) footerTemplate.style.display = 'none';
    }, i);

    // Wait for rendering to settle
    await new Promise(resolve => setTimeout(resolve, 200));

    // Take a full-page screenshot at viewport size
    const screenshotBuffer = await page.screenshot({
      type: 'png',
      clip: {
        x: 0,
        y: 0,
        width: 1280,
        height: 720
      },
      omitBackground: false
    });

    // Embed the PNG image into the PDF
    const pngImage = await pdfDoc.embedPng(screenshotBuffer);

    // Get image dimensions (will be 2560x1440 due to deviceScaleFactor: 2)
    const imgWidth = pngImage.width;
    const imgHeight = pngImage.height;

    // Add a page with 16:9 aspect ratio (standard presentation size)
    // Using 1280x720 points which is a common presentation dimension
    const pdfPage = pdfDoc.addPage([1280, 720]);

    // Draw the image scaled to fit the page exactly
    pdfPage.drawImage(pngImage, {
      x: 0,
      y: 0,
      width: 1280,
      height: 720
    });
  }

  // Save the PDF
  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(pdfFile, pdfBytes);

  console.log(`PDF generated successfully: ${pdfFile} (${slideCount} pages)`);

  await browser.close();
})();
