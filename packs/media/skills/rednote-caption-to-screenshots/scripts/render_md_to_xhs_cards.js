#!/usr/bin/env node
/**
 * Render Markdown -> Xiaohongshu cards (cover + cards).
 *
 * Design reference: https://github.com/comeonzhj/Auto-Redbook-Skills (MIT).
 * This script is adapted to this workspace and uses local templates:
 * - assets/xhs_cover.html
 * - assets/xhs_card.html
 *
 * Dependencies (install once):
 *   npm i playwright marked js-yaml
 *   npx playwright install chromium
 *
 * Usage:
 *   node scripts/render_md_to_xhs_cards.js <markdownFile> [--output-dir <dir>]
 *
 * Input markdown format:
 * - Optional YAML frontmatter:
 *   ---
 *   emoji: "✦"
 *   title: "封面标题"
 *   subtitle: "副标题"
 *   ---
 * - Use `---` separators to split multiple card sections.
 */

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { marked } = require("marked");
const yaml = require("js-yaml");

const SKILL_DIR = path.join(__dirname, "..");
const ASSETS_DIR = path.join(SKILL_DIR, "assets");

const CARD_WIDTH = 1080;
const CARD_HEIGHT = 1440;

function loadTemplate(name) {
  return fs.readFileSync(path.join(ASSETS_DIR, name), "utf-8");
}

function parseMarkdownFile(filePath) {
  const content = fs.readFileSync(filePath, "utf-8");
  const yamlPattern = /^---\s*\n([\s\S]*?)\n---\s*\n/;
  const yamlMatch = content.match(yamlPattern);

  let metadata = {};
  let body = content;

  if (yamlMatch) {
    try {
      metadata = yaml.load(yamlMatch[1]) || {};
    } catch {
      metadata = {};
    }
    body = content.slice(yamlMatch[0].length);
  }

  return { metadata, body: body.trim() };
}

function splitBySeparator(body) {
  const parts = body.split(/\n---+\n/);
  return parts.filter((p) => p.trim()).map((p) => p.trim());
}

function markdownToHtml(md) {
  return marked.parse(md, { breaks: true, gfm: true });
}

function generateCoverHtml(metadata) {
  const tpl = loadTemplate("xhs_cover.html");
  const emoji = String(metadata.emoji || "✦").slice(0, 6);
  const title = String(metadata.title || "标题").slice(0, 15);
  const subtitle = String(metadata.subtitle || "").slice(0, 18);

  return tpl
    .replace("{{EMOJI}}", emoji)
    .replace("{{TITLE}}", title)
    .replace("{{SUBTITLE}}", subtitle);
}

function generateCardHtml(sectionMd, pageNumber, totalPages) {
  const tpl = loadTemplate("xhs_card.html");
  const html = markdownToHtml(sectionMd);
  const pageText = totalPages > 1 ? `${pageNumber}/${totalPages}` : "";
  return tpl.replace("{{CONTENT}}", html).replace("{{PAGE_NUMBER}}", pageText);
}

async function renderHtmlToPng(htmlContent, outputPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: CARD_WIDTH, height: CARD_HEIGHT },
    deviceScaleFactor: 2,
  });

  await page.setContent(htmlContent, { waitUntil: "networkidle" });
  await page.waitForTimeout(300);

  // screenshot full card area (min 1440)
  const clipHeight = await page.evaluate(() => {
    const root = document.querySelector(".card") || document.querySelector(".cover");
    const h = root ? root.scrollHeight : document.body.scrollHeight;
    return Math.max(1440, h);
  });

  await page.screenshot({
    path: outputPath,
    type: "png",
    clip: { x: 0, y: 0, width: CARD_WIDTH, height: clipHeight },
  });

  await browser.close();
}

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node scripts/render_md_to_xhs_cards.js <markdownFile> [--output-dir <dir>]");
    process.exit(1);
  }

  let markdownFile = null;
  let outputDir = process.cwd();

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output-dir" || args[i] === "-o") {
      outputDir = args[i + 1];
      i++;
      continue;
    }
    if (!args[i].startsWith("-") && !markdownFile) markdownFile = args[i];
  }

  if (!markdownFile) {
    console.error("Error: markdownFile is required.");
    process.exit(1);
  }
  if (!fs.existsSync(markdownFile)) {
    console.error(`Error: file not found: ${markdownFile}`);
    process.exit(1);
  }

  return { markdownFile, outputDir };
}

async function main() {
  const { markdownFile, outputDir } = parseArgs();
  fs.mkdirSync(outputDir, { recursive: true });

  const { metadata, body } = parseMarkdownFile(markdownFile);
  const sections = splitBySeparator(body);

  // cover (optional)
  if (metadata.title || metadata.emoji || metadata.subtitle) {
    const coverHtml = generateCoverHtml(metadata);
    const coverPath = path.join(outputDir, "cover.png");
    await renderHtmlToPng(coverHtml, coverPath);
    console.log(`OK: ${coverPath}`);
  }

  // cards
  const total = sections.length;
  for (let i = 0; i < total; i++) {
    const pageNum = i + 1;
    const cardHtml = generateCardHtml(sections[i], pageNum, total);
    const out = path.join(outputDir, `card_${pageNum}.png`);
    await renderHtmlToPng(cardHtml, out);
    console.log(`OK: ${out}`);
  }
}

main().catch((e) => {
  console.error("Render failed:", e);
  process.exit(1);
});

