# HTML to PDF Conversion

## Directory Structure

```
decks/
├── html/              ← Source HTML slide presentations
├── pdf/               ← Generated PDF outputs
├── generatePDF.js     ← Conversion script
├── package.json       ← Dependencies
└── README.md          ← Quick start guide
```

## Quick Start

```bash
# Install dependencies (one time)
npm install

# Convert a single file
npm run pdf -- my-slides.html

# Convert ALL HTML files
npm run pdf:all
```

## Usage

### Single File

```bash
# Any of these work:
node generatePDF.js my-slides
node generatePDF.js my-slides.html
npm run pdf -- my-slides

# Faster with Bun:
bun generatePDF.js my-slides
```

### Batch Convert All

```bash
npm run pdf:all
# or
bun generatePDF.js --all
```

## Performance

| Runtime | ~59 slides |
|---------|-----------|
| **Bun** | ~18s 🏆 |
| Node.js | ~31s |

## How It Works

1. Launches headless Chrome via Puppeteer
2. Sets viewport to 1280x720 (16:9 aspect ratio)
3. Loads HTML from `html/` directory
4. Iterates through each `.slide-container` element
5. Takes PNG screenshots at 3x resolution
6. Combines into PDF using pdf-lib
7. Saves to `pdf/` directory

## Quality Settings

Edit `generatePDF.js` to adjust:

```javascript
const QUALITY = {
  deviceScaleFactor: 3,  // 2=fast, 3=excellent, 4=overkill
  waitTime: 100,         // ms between slides
  optimizeForSpeed: false
};
```

| Setting | Speed | Quality | Use Case |
|---------|-------|---------|----------|
| deviceScaleFactor: 2 | Fast | Good | Quick drafts |
| deviceScaleFactor: 3 | Moderate | **Excellent** | **Production** ⭐ |
| deviceScaleFactor: 4 | Slow | Overkill | Not needed |

## Troubleshooting

**Slides appear cut off or wrong position:**
- The script resets `--scale` CSS variable to 1
- Body display is set to `block` not `flex`
- Slides positioned `absolute` at `top: 0; left: 0`

**Fonts or images missing:**
- Script waits for `networkidle0` before screenshots
- Increase `waitTime` in QUALITY settings if needed

## Why Node.js/Bun?

**Considered alternatives:**
- ❌ **Pyppeteer**: Unmaintained since 2021
- ⚠️ **Playwright (Python)**: Slower, heavier
- ❌ **WeasyPrint/pdfkit**: Poor CSS support, no JS

**Verdict:** Puppeteer is the gold standard. Bun makes it even faster.

## Notes

- Output PDFs: 1280x720pt page size (standard presentation)
- Screenshots: 3x device scale for ultra-sharp quality
- Navigation controls and footers hidden during export
- Section dividers preserve dark backgrounds
