#!/usr/bin/env node
/**
 * Render existing deck HTML (.page elements) to 1080x1440 PNGs using Playwright.
 *
 * This is the RECOMMENDED method for small red book carousel screenshots.
 * It directly captures each .page element without relying on CSS :target selectors,
 * which are unreliable in headless browsers.
 *
 * Features:
 *   - Directly screenshots each .page element (no CSS hash tricks needed)
 *   - 2x device scale factor for crisp text
 *   - Waits for PlantUML images to load before capturing
 *   - Stable and reliable - no blank/black screenshots
 *
 * Dependencies:
 *   npm i playwright
 *   (No need for "npx playwright install" if using system Chrome)
 *
 * Usage:
 *   node scripts/render_deck_playwright.js <htmlPath> [--output-dir <dir>] [--prefix <prefix>]
 *
 * Example:
 *   node scripts/render_deck_playwright.js "./deck.html" --output-dir "./out" --prefix "topic"
 *
 * Quick start (in HTML folder):
 *   npm init -y && npm install playwright
 *   node /path/to/render_deck_playwright.js "my_deck.html"
 */

const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

function fileUrl(p) {
  const resolved = path.resolve(p);
  return "file://" + resolved.split(path.sep).map(encodeURIComponent).join("/");
}

async function waitForPlantUmlImages(page, timeoutMs = 45000) {
  try {
    await page.waitForFunction(() => {
      const imgs = Array.from(document.querySelectorAll("img.plantuml"));
      if (!imgs.length) return true;
      return imgs.every((img) => img.complete && img.naturalWidth > 0);
    }, { timeout: timeoutMs });
  } catch (_) {
    console.warn("PlantUML images may not have loaded completely.");
  }
}

async function launchBrowser() {
  try {
    return await chromium.launch({ channel: "chrome", headless: true });
  } catch {
    return await chromium.launch({ headless: true });
  }
}

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node render_deck_playwright.js <htmlPath> [--output-dir <dir>] [--prefix <prefix>]");
    process.exit(1);
  }

  let htmlPath = null;
  let outputDir = null;
  let prefix = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output-dir" || args[i] === "-o") {
      outputDir = args[i + 1];
      i++;
    } else if (args[i] === "--prefix" || args[i] === "-p") {
      prefix = args[i + 1];
      i++;
    } else if (!args[i].startsWith("-") && !htmlPath) {
      htmlPath = args[i];
    }
  }

  if (!htmlPath) {
    console.error("Error: htmlPath is required.");
    process.exit(1);
  }
  if (!fs.existsSync(htmlPath)) {
    console.error(`Error: file not found: ${htmlPath}`);
    process.exit(1);
  }

  // Default output dir: same folder as HTML, with _png suffix
  if (!outputDir) {
    const htmlDir = path.dirname(htmlPath);
    const htmlName = path.basename(htmlPath, path.extname(htmlPath));
    outputDir = path.join(htmlDir, `${htmlName}_png`);
  }

  // Default prefix: derive from HTML filename
  if (!prefix) {
    prefix = path.basename(htmlPath, path.extname(htmlPath));
  }

  return { htmlPath, outputDir, prefix };
}

async function main() {
  const { htmlPath, outputDir, prefix } = parseArgs();

  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await launchBrowser();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1440 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  await page.goto(fileUrl(htmlPath), { waitUntil: "load" });
  await page.waitForTimeout(500); // Brief wait for any CSS/fonts to settle
  await waitForPlantUmlImages(page);

  const pages = page.locator(".page");
  const count = await pages.count();

  if (!count) {
    console.error("No .page elements found in HTML.");
    await browser.close();
    process.exit(2);
  }

  for (let i = 0; i < count; i++) {
    const idx = String(i + 1).padStart(2, "0");
    const outPath = path.join(outputDir, `${prefix}_p${idx}.png`);
    await pages.nth(i).screenshot({ path: outPath });
    console.log(`OK: ${outPath}`);
  }

  await browser.close();
  console.log(`\nDone. ${count} images saved to ${outputDir}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
