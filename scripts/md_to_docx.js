const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ImageRun, AlignmentType, ShadingType, PageBreak, LevelFormat,
  Header, Footer, PageNumber,
} = require("docx");

const SRC = process.argv[2] || "/home/claude/materi_training_ibankcore.md";
const OUT = process.argv[3] || "/home/claude/materi_training_ibankcore.docx";
const BASE_DIR = path.dirname(SRC);

const NAVY = "12233F";
const BLUE = "1F4E79";
const GREY = "6B7280";

const raw = fs.readFileSync(SRC, "utf8");

// ---- front matter ----
const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
let meta = {};
let body = raw;
if (fmMatch) {
  fmMatch[1].split("\n").forEach((line) => {
    const m = line.match(/^(\w+):\s*(.*)$/);
    if (m) meta[m[1]] = m[2].trim();
  });
  body = fmMatch[2];
}

// ---- helpers ----
function h1(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 } }); }
function h2(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 260, after: 120 } }); }
function h3(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 100 } }); }
function parseInline(text) {
  // Split on **bold** markers, return array of TextRun
  const parts = text.split(/(\*\*[^*]+\*\*)/g).filter(s => s.length > 0);
  return parts.map(part => {
    const boldMatch = part.match(/^\*\*([^*]+)\*\*$/);
    if (boldMatch) return new TextRun({ text: boldMatch[1], bold: true });
    return new TextRun({ text: part });
  });
}
function para(text) {
  return new Paragraph({ spacing: { after: 160, line: 300 }, children: parseInline(text) });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "main-bullets", level: 0 },
    spacing: { after: 80 },
    children: parseInline(text),
  });
}
function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.header ? { type: ShadingType.CLEAR, fill: BLUE } : undefined,
    children: [new Paragraph({
      children: [new TextRun({ text, bold: !!opts.header, color: opts.header ? "FFFFFF" : "000000", size: 20 })],
    })],
  });
}
function mdTable(headerRow, dataRows) {
  const nCols = headerRow.length;
  const totalWidth = 9300;
  const firstColWidth = Math.round(totalWidth * 0.28);
  const restWidth = Math.round((totalWidth - firstColWidth) / (nCols - 1));
  const widths = [firstColWidth, ...Array(nCols - 1).fill(restWidth)];
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ children: headerRow.map((hh, i) => cell(hh, { header: true, width: widths[i] })) }),
      ...dataRows.map(r => new TableRow({ children: r.map((c, i) => cell(c, { width: widths[i] })) })),
    ],
  });
}
function img(imgPath, caption) {
  const full = path.isAbsolute(imgPath) ? imgPath : path.join(BASE_DIR, imgPath);
  const dims = require("image-size").imageSize(fs.readFileSync(full));
  const maxW = 560;
  const w = maxW;
  const h = Math.round(maxW * (dims.height / dims.width));
  const children = [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 80 },
      children: [new ImageRun({ data: fs.readFileSync(full), transformation: { width: w, height: h }, type: "png" })],
    }),
  ];
  if (caption) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
      children: [new TextRun({ text: caption, italics: true, size: 18, color: GREY })],
    }));
  }
  return children;
}

// ---- markdown body parser ----
const lines = body.split("\n");
const children = [];
let i = 0;
let tocHeadings = [];

// cover page
children.push(new Paragraph({ spacing: { before: 1600 }, alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: (meta.title || "").toUpperCase(), bold: true, size: 30, color: BLUE })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 },
  children: [new TextRun({ text: meta.subtitle || "", bold: true, size: 44, color: NAVY })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
  children: [new TextRun({ text: meta.tagline || "", size: 24, color: GREY })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 800 },
  children: [new TextRun({ text: meta.org || "", size: 22, color: GREY })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: meta.note || "", size: 20, color: GREY })] }));
children.push(new Paragraph({ children: [new PageBreak()] }));

while (i < lines.length) {
  let line = lines[i];

  if (/^#\s+/.test(line)) {
    const text = line.replace(/^#\s+/, "").trim();
    tocHeadings.push(text);
    children.push(h1(text));
    i++;
    continue;
  }
  if (/^##\s+/.test(line)) {
    children.push(h2(line.replace(/^##\s+/, "").trim()));
    i++;
    continue;
  }
  if (/^###\s+/.test(line)) {
    children.push(h3(line.replace(/^###\s+/, "").trim()));
    i++;
    continue;
  }
  if (/^!\[(.*)\]\((.*)\)/.test(line)) {
    const m = line.match(/^!\[(.*)\]\((.*)\)/);
    children.push(...img(m[2], m[1]));
    i++;
    continue;
  }
  if (/^-\s+/.test(line)) {
    while (i < lines.length && /^-\s+/.test(lines[i])) {
      children.push(bullet(lines[i].replace(/^-\s+/, "").trim()));
      i++;
    }
    continue;
  }
  if (/^\|/.test(line)) {
    const tableLines = [];
    while (i < lines.length && /^\|/.test(lines[i])) {
      tableLines.push(lines[i]);
      i++;
    }
    const rows = tableLines
      .filter(l => !/^\|\s*-+\s*\|/.test(l.replace(/\s/g, "").length ? l : l))
      .filter(l => !/^\|[\s-]*\|[\s-]*(\|[\s-]*)*$/.test(l))
      .map(l => l.split("|").slice(1, -1).map(c => c.trim()));
    const headerRow = rows[0];
    const dataRows = rows.slice(1);
    children.push(mdTable(headerRow, dataRows));
    children.push(new Paragraph({ text: "" }));
    continue;
  }
  if (line.trim() === "") { i++; continue; }
  // plain paragraph
  children.push(para(line.trim()));
  i++;
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "main-bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 260 } } } },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({ alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: meta.header || "Materi Training", size: 16, color: GREY })] })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({ alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Halaman ", size: 16, color: GREY }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
            ] })],
        }),
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("written:", OUT);
});
