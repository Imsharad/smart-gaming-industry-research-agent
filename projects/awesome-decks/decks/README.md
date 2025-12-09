# Awesome Decks - HTML Slide to PDF Converter

Convert HTML slide presentations to high-quality PDFs.

## Directory Structure

```
decks/
├── html/              ← Put your HTML slide files here
│   ├── claude_agent.html
│   └── ...
├── pdf/               ← Generated PDFs appear here
│   ├── claude_agent.pdf
│   └── ...
├── generatePDF.js     ← Main conversion script
├── package.json
└── README.md
```

## Quick Start

```bash
# Install dependencies (one time)
npm install

# Convert a single file
npm run pdf -- my-slides.html
# or
node generatePDF.js my-slides

# Convert ALL HTML files in html/
npm run pdf:all
# or
node generatePDF.js --all
```

## Usage

### Single File Conversion

```bash
# Any of these work:
node generatePDF.js my-slides
node generatePDF.js my-slides.html
npm run pdf -- my-slides.html
```

The script automatically:
- Looks for the file in `html/` directory
- Outputs the PDF to `pdf/` directory

### Batch Conversion

Convert all HTML files at once:

```bash
npm run pdf:all
```

## Performance

Using Bun for faster execution:

```bash
bun generatePDF.js my-slides.html
bun generatePDF.js --all
```

| Runtime | ~59 slides |
|---------|-----------|
| **Bun** | ~18s |
| Node.js | ~31s |

## Quality Settings

Edit `generatePDF.js` to adjust quality:

```javascript
const QUALITY = {
  deviceScaleFactor: 3,  // 2=good, 3=excellent, 4=overkill
  waitTime: 100,         // ms between slides (higher = better fonts)
  optimizeForSpeed: false
};
```

## Documentation

See [CLAUDE.md](./CLAUDE.md) for technical details and troubleshooting.
