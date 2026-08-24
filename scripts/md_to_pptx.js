const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const pptxgen = require("pptxgenjs");

const SRC = process.argv[2] || "/home/claude/slides_training_ibankcore.md";
const OUT = process.argv[3] || "/home/claude/materi_training_ibankcore.pptx";
const BASE_DIR = path.dirname(SRC);

const NAVY = "1E2761";
const NAVY_DARK = "12233F";
const ICE = "CADCFC";
const WHITE = "FFFFFF";
const GOLD = "C0862B";
const GREY_TXT = "44546A";
const LIGHT_BG = "F5F8FC";
const CARD_BG = "EAF1F8";
const FONT_HEAD = "Cambria";
const FONT_BODY = "Calibri";

function imgSize(p) {
  return require("image-size").imageSize(fs.readFileSync(p));
}

const raw = fs.readFileSync(SRC, "utf8");
const slideChunks = raw.split(/\n===\n/).map(s => s.trim()).filter(Boolean);
const slides = slideChunks.map(chunk => yaml.load(chunk));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

function shadow() { return { type: "outer", color: "12233F", opacity: 0.18, blur: 6, offset: 2, angle: 90 }; }

function titleBar(slide, kicker, title) {
  slide.addText((kicker || "").toUpperCase(), {
    x: 0.6, y: 0.35, w: 8, h: 0.35, fontFace: FONT_BODY, fontSize: 13, bold: true, color: GOLD, charSpacing: 2,
  });
  slide.addText(title || "", {
    x: 0.6, y: 0.65, w: 12.1, h: 0.85, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: NAVY_DARK,
  });
}
function footerLabel(slide) {
  slide.addText("IBANKCORE — Training Core Banking", {
    x: 0.6, y: 7.05, w: 6, h: 0.35, fontFace: FONT_BODY, fontSize: 10, color: GREY_TXT,
  });
}
function pageNum(slide, n, dark) {
  slide.addText(String(n), {
    x: 12.7, y: 7.05, w: 0.5, h: 0.35, fontFace: FONT_BODY, fontSize: 10, color: dark ? ICE : GREY_TXT, align: "right",
  });
}

slides.forEach((sl, idx) => {
  const n = idx + 1;
  const s = pres.addSlide();

  if (sl.layout === "title") {
    s.background = { color: NAVY_DARK };
    s.addShape(pres.ShapeType.ellipse, { x: 9.8, y: -2.5, w: 7, h: 7, fill: { color: NAVY, transparency: 40 }, line: { type: "none" } });
    s.addShape(pres.ShapeType.ellipse, { x: 11.2, y: 4.3, w: 4.5, h: 4.5, fill: { color: GOLD, transparency: 82 }, line: { type: "none" } });
    s.addText((sl.kicker || "").toUpperCase(), { x: 0.9, y: 2.05, w: 9, h: 0.4, fontFace: FONT_BODY, fontSize: 14, bold: true, color: GOLD, charSpacing: 3 });
    s.addText(sl.title || "", { x: 0.85, y: 2.4, w: 11.5, h: 1.3, fontFace: FONT_HEAD, fontSize: 48, bold: true, color: WHITE });
    s.addText((sl.subtitle || "").trim(), { x: 0.9, y: 3.65, w: 10, h: 0.9, fontFace: FONT_BODY, fontSize: 18, color: ICE, lineSpacingMultiple: 1.3 });
    s.addShape(pres.ShapeType.line, { x: 0.9, y: 4.75, w: 2.2, h: 0, line: { color: GOLD, width: 2.5 } });
    s.addText(sl.footer || "", { x: 0.9, y: 4.95, w: 9, h: 0.4, fontFace: FONT_BODY, fontSize: 13, color: ICE });
    return;
  }

  s.background = { color: WHITE };
  titleBar(s, sl.kicker, sl.title);

  if (sl.layout === "cards") {
    const cw = 3.95, ch = 1.95, gx = 0.25, gy = 0.3, startX = 0.6, startY = 1.85, cols = 3;
    sl.cards.forEach((it, i) => {
      const col = i % cols, row = Math.floor(i / cols);
      const x = startX + col * (cw + gx), y = startY + row * (ch + gy);
      s.addShape(pres.ShapeType.roundRect, { x, y, w: cw, h: ch, rectRadius: 0.08, fill: { color: CARD_BG }, line: { color: ICE, width: 1 }, shadow: shadow() });
      s.addText(it.num, { x: x + 0.2, y: y + 0.15, w: 1.2, h: 0.6, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: GOLD });
      s.addText(it.heading, { x: x + 0.2, y: y + 0.85, w: cw - 0.4, h: 0.55, fontFace: FONT_BODY, fontSize: 15, bold: true, color: NAVY_DARK });
      s.addText(it.text, { x: x + 0.2, y: y + 1.35, w: cw - 0.4, h: 0.5, fontFace: FONT_BODY, fontSize: 11.5, color: GREY_TXT });
    });
  }

  else if (sl.layout === "image") {
    const full = path.join(BASE_DIR, sl.image);
    const dims = imgSize(full);
    const ratio = dims.width / dims.height;
    const areaX0 = 0.6, areaX1 = 12.73, areaY0 = 1.75, areaY1 = 7.05;
    const maxW = areaX1 - areaX0, maxH = areaY1 - areaY0;
    let w = maxW, h = w / ratio;
    if (h > maxH) { h = maxH; w = h * ratio; }
    const x = areaX0 + (maxW - w) / 2;
    const y = areaY0 + (maxH - h) / 2;
    s.addImage({ path: full, x, y, w, h });
  }

  else if (sl.layout === "table-grid") {
    const cw = 5.95, ch = 0.98, gx = 0.3, gy = 0.18, startX = 0.6, startY = 1.75;
    sl.rows.forEach((m, i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = startX + col * (cw + gx), y = startY + row * (ch + gy);
      s.addShape(pres.ShapeType.roundRect, { x, y, w: cw, h: ch, rectRadius: 0.06, fill: { color: LIGHT_BG }, line: { color: ICE, width: 1 } });
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.15, y: y + 0.19, w: 0.1, h: 0.6, fill: { color: GOLD }, line: { type: "none" } });
      s.addText(m[0], { x: x + 0.4, y: y + 0.08, w: cw - 0.6, h: 0.4, fontFace: FONT_BODY, fontSize: 14, bold: true, color: NAVY_DARK });
      s.addText(m[1], { x: x + 0.4, y: y + 0.46, w: cw - 0.6, h: 0.45, fontFace: FONT_BODY, fontSize: 10.5, color: GREY_TXT });
    });
  }

  else if (sl.layout === "numbered-cards") {
    s.addText(sl.intro || "", { x: 0.6, y: 1.7, w: 11.8, h: 0.5, fontFace: FONT_BODY, fontSize: 13.5, color: GREY_TXT });
    const cw = 2.85, ch = 3.15, gx = 0.25;
    sl.cards.forEach((c, i) => {
      const x = 0.6 + i * (cw + gx);
      s.addShape(pres.ShapeType.roundRect, { x, y: 2.5, w: cw, h: ch, rectRadius: 0.08, fill: { color: i % 2 === 0 ? NAVY_DARK : NAVY } });
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.25, y: 2.8, w: 0.55, h: 0.55, rectRadius: 0.28, fill: { color: GOLD } });
      s.addText(String(i + 1), { x: x + 0.25, y: 2.8, w: 0.55, h: 0.55, align: "center", valign: "middle", fontFace: FONT_HEAD, fontSize: 18, bold: true, color: NAVY_DARK });
      s.addText(c.heading, { x: x + 0.25, y: 3.55, w: cw - 0.5, h: 0.7, fontFace: FONT_BODY, fontSize: 13.5, bold: true, color: WHITE });
      s.addText(c.text, { x: x + 0.25, y: 4.25, w: cw - 0.5, h: 1.25, fontFace: FONT_BODY, fontSize: 10.8, color: ICE });
    });
  }

  else if (sl.layout === "two-column") {
    renderColumn(s, sl.left, 0.6, 5.9, false);
    renderColumn(s, sl.right, 6.85, 5.9, true);
  }

  else if (sl.layout === "summary") {
    s.background = { color: NAVY_DARK };
    s.addShape(pres.ShapeType.ellipse, { x: -2, y: 4.5, w: 6, h: 6, fill: { color: NAVY, transparency: 45 }, line: { type: "none" } });
    s.addText((sl.kicker || "").toUpperCase(), { x: 0.7, y: 0.55, w: 8, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: GOLD, charSpacing: 2 });
    s.addText(sl.title || "", { x: 0.65, y: 0.9, w: 11, h: 0.8, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: WHITE });
    let py = 2.05;
    sl.points.forEach((k, i) => {
      s.addShape(pres.ShapeType.roundRect, { x: 0.7, y: py, w: 0.5, h: 0.5, rectRadius: 0.25, fill: { color: GOLD } });
      s.addText(String(i + 1), { x: 0.7, y: py, w: 0.5, h: 0.5, align: "center", valign: "middle", fontFace: FONT_HEAD, fontSize: 16, bold: true, color: NAVY_DARK });
      s.addText(k, { x: 1.45, y: py - 0.05, w: 10.8, h: 0.65, valign: "middle", fontFace: FONT_BODY, fontSize: 14.5, color: ICE });
      py += 0.85;
    });
    s.addShape(pres.ShapeType.line, { x: 0.7, y: 5.75, w: 11.9, h: 0, line: { color: NAVY, width: 1 } });
    s.addText(sl.discussion_heading || "", { x: 0.7, y: 5.95, w: 6, h: 0.4, fontFace: FONT_HEAD, fontSize: 15, bold: true, color: GOLD });
    s.addText(sl.discussion || "", { x: 0.7, y: 6.4, w: 11.9, h: 0.5, fontFace: FONT_BODY, fontSize: 12.5, italic: true, color: ICE });
    pageNum(s, n, true);
    return;
  }

  footerLabel(s);
  pageNum(s, n);
});

function renderColumn(s, col, x, w, isRight) {
  if (!col) return;
  const dark = col.panel === "dark";
  const yTop = 1.8;
  // Case: panel_top / panel_bottom (kliring/pelaporan slide)
  if (col.panel_top || col.panel_bottom) {
    if (col.rows) renderMiniTable(s, col, x, w);
    if (col.panel_top) {
      const h = 2.35;
      s.addShape(pres.ShapeType.roundRect, { x, y: yTop, w, h, rectRadius: 0.08, fill: { color: NAVY_DARK } });
      s.addText(col.panel_top.heading, { x: x + 0.3, y: yTop + 0.2, w: w - 0.6, h: 0.4, fontFace: FONT_HEAD, fontSize: 14.5, bold: true, color: WHITE });
      s.addText(col.panel_top.text, { x: x + 0.3, y: yTop + 0.65, w: w - 0.6, h: 1.55, fontFace: FONT_BODY, fontSize: 11.5, color: ICE, valign: "top" });
    }
    if (col.panel_bottom) {
      const y2 = yTop + 2.5;
      const h = 2.4;
      s.addShape(pres.ShapeType.roundRect, { x, y: y2, w, h, rectRadius: 0.08, fill: { color: CARD_BG }, line: { color: ICE, width: 1 } });
      s.addText(col.panel_bottom.heading, { x: x + 0.3, y: y2 + 0.2, w: w - 0.6, h: 0.4, fontFace: FONT_HEAD, fontSize: 14.5, bold: true, color: NAVY_DARK });
      s.addText(col.panel_bottom.text, { x: x + 0.3, y: y2 + 0.65, w: w - 0.6, h: 1.6, fontFace: FONT_BODY, fontSize: 11.5, color: GREY_TXT, valign: "top" });
    }
    return;
  }

  if (col.heading && col.rows && !col.panel) {
    // simple heading + mini table (left column style, no big panel)
    s.addText(col.heading, { x, y: yTop, w, h: 0.4, fontFace: FONT_HEAD, fontSize: 15, bold: true, color: NAVY_DARK });
    renderMiniTable(s, col, x, w, yTop + 0.5);
    return;
  }

  // panel-based column (accounting slide, treasury slide, pindah-buku/syariah slide)
  const h = 4.9;
  s.addShape(pres.ShapeType.roundRect, { x, y: yTop, w, h, rectRadius: 0.08, fill: { color: dark ? NAVY_DARK : (col.panel === "light" ? CARD_BG : WHITE) }, line: col.panel === "light" ? { color: ICE, width: 1 } : undefined });
  let py = yTop + 0.25;
  const textColorHead = dark ? WHITE : NAVY_DARK;
  const textColorBody = dark ? ICE : GREY_TXT;
  const accentColor = dark ? GOLD : GOLD;

  s.addText(col.heading || "", { x: x + 0.3, y: py, w: w - 0.6, h: 0.45, fontFace: FONT_HEAD, fontSize: 17, bold: true, color: textColorHead });
  py += 0.55;
  if (col.intro) {
    s.addText(col.intro, { x: x + 0.3, y: py, w: w - 0.6, h: 0.4, fontFace: FONT_BODY, fontSize: 12, color: textColorBody });
    py += 0.55;
  }

  if (col.drcr) {
    const bw = (w - 0.6 - 0.3) / 2;
    col.drcr.forEach((label, i) => {
      const bx = x + 0.3 + i * (bw + 0.3);
      s.addShape(pres.ShapeType.roundRect, { x: bx, y: py, w: bw, h: 1.0, rectRadius: 0.06, fill: { color: NAVY } });
      const [big, small] = label.split(" / ");
      s.addText(big, { x: bx, y: py + 0.08, w: bw, h: 0.5, align: "center", fontFace: FONT_HEAD, fontSize: 22, bold: true, color: GOLD });
      s.addText(small || "", { x: bx, y: py + 0.58, w: bw, h: 0.3, align: "center", fontFace: FONT_BODY, fontSize: 11, color: ICE });
    });
    py += 1.3;
  }

  if (col.items) {
    col.items.forEach(it => {
      s.addText([
        { text: it.label + "  ", options: { bold: true, color: accentColor } },
        { text: "— " + it.text, options: { color: textColorBody } },
      ], { x: x + 0.3, y: py, w: w - 0.6, h: 0.55, fontFace: FONT_BODY, fontSize: 11.5, breakLine: true });
      py += 0.6;
    });
  }

  if (col.list_cards) {
    col.list_cards.forEach(pt => {
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.3, y: py, w: w - 0.6, h: 0.6, rectRadius: 0.05, fill: { color: WHITE }, line: { color: ICE, width: 1 } });
      s.addText(pt, { x: x + 0.55, y: py, w: w - 1.1, h: 0.6, valign: "middle", fontFace: FONT_BODY, fontSize: 12.5, bold: true, color: NAVY_DARK });
      py += 0.72;
    });
  }

  if (col.bullets) {
    col.bullets.forEach(pt => {
      s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: py + 0.06, w: 0.15, h: 0.15, fill: { color: GOLD }, line: { type: "none" } });
      s.addText(pt, { x: x + 0.65, y: py - 0.06, w: w - 0.95, h: 0.55, fontFace: FONT_BODY, fontSize: 12.5, color: textColorBody });
      py += 0.75;
    });
  }

  if (col.rows) {
    col.rows.forEach(r => {
      s.addShape(pres.ShapeType.roundRect, { x: x + 0.3, y: py, w: w - 0.6, h: 0.75, rectRadius: 0.05, fill: { color: dark ? NAVY : LIGHT_BG } });
      s.addText(r[0], { x: x + 0.5, y: py + 0.08, w: 2.2, h: 0.55, valign: "middle", fontFace: FONT_BODY, fontSize: 13, bold: true, color: GOLD });
      s.addText(r[1], { x: x + 2.7, y: py + 0.08, w: w - 3.0, h: 0.55, valign: "middle", fontFace: FONT_BODY, fontSize: 11, color: textColorBody });
      py += 0.9;
    });
  }

  if (col.note) {
    const noteY = yTop + h - 1.65 - 0.25;
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.3, y: noteY, w: w - 0.6, h: 1.65, rectRadius: 0.08, fill: { color: dark ? NAVY : NAVY_DARK } });
    s.addText(col.note, { x: x + 0.55, y: noteY + 0.15, w: w - 1.1, h: 1.35, fontFace: FONT_BODY, fontSize: 12, italic: true, color: ICE, valign: "middle" });
  }
}

function renderMiniTable(s, col, x, w, yStart) {
  let ry = yStart || 2.25;
  col.rows.forEach(r => {
    s.addShape(pres.ShapeType.roundRect, { x, y: ry, w, h: 0.95, rectRadius: 0.06, fill: { color: LIGHT_BG }, line: { color: ICE, width: 1 } });
    s.addText(r[0], { x: x + 0.2, y: ry + 0.1, w: 1.6, h: 0.75, valign: "middle", fontFace: FONT_HEAD, fontSize: 15, bold: true, color: GOLD });
    s.addText(r[1], { x: x + 1.8, y: ry + 0.1, w: w - 2.0, h: 0.75, valign: "middle", fontFace: FONT_BODY, fontSize: 11, color: GREY_TXT });
    ry += 1.1;
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("written:", OUT));
