---
name: se-html-explainer
description: 'Convert verbose markdown files, wiki pages, or LLM responses into clean, visually appealing, conceptually clear HTML explainer pages. Use when asked to "explain this visually", "make an HTML explainer", "convert to HTML", "visualize this markdown", "make this easier to understand", "create an HTML view", "generate a visual summary", or when the user wants a polished, browsable HTML page from dense text. Saves output to html-files/ directory. Supports single-page and batch conversion.'
---

# HTML Explainer

Convert dense markdown content — wiki pages, raw sources, LLM responses, or any verbose text — into clean, visually appealing HTML explainer pages that are easy to read, navigate, and understand. Output goes to the `html-files/` directory at the project root.

## When to Use This Skill

- User says "explain this visually", "make an HTML explainer", "create an HTML view"
- User says "convert this to HTML", "make this easier to understand"
- User says "generate a visual summary", "visualize this markdown"
- User wants a polished, browsable HTML page from a wiki page, analysis, or LLM response
- User asks to convert one or more markdown files into HTML explainers
- After a long or complex LLM response, the user wants it preserved as a shareable HTML file
- User says "convert the wiki to HTML", "make HTML pages for these concepts"

## Prerequisites

- Content to convert: a markdown file path, a wiki page, a raw source, or inline text
- File creation tools to write HTML to `html-files/`
- The workspace should have (or will get) an `html-files/` directory at the project root

## Directory Structure

```
html-files/
├── index.html                  # Optional: catalog of all generated explainer pages
├── <slug>.html                 # Individual explainer pages
└── ...
```

### File Naming Convention

- Derive the filename from the source: `wiki/concepts/cap-theorem.md` → `cap-theorem.html`
- For LLM responses or inline text, ask the user for a name or derive from the topic
- Lowercase, hyphens for spaces, no special characters
- Max 60 characters for the slug portion

## Design Principles

Every HTML explainer page MUST follow these principles:

### 1. Conceptual Clarity Over Completeness
- Restructure content for understanding, not just reformatting
- Lead with the core idea ("What is this?") before diving into details
- Use progressive disclosure: overview → key points → details
- Group related information visually

### 2. Visual Hierarchy
- Clear heading structure with distinct visual weight
- Card-based layouts for grouping related concepts
- Tables for comparisons and structured data
- Callout boxes for key takeaways, warnings, and notes
- Adequate whitespace — never a wall of text

### 3. Self-Contained
- All CSS inline in a `<style>` block (no external dependencies)
- No JavaScript required for core content (progressive enhancement only)
- Works offline — can be opened directly in any browser
- Responsive design that works on desktop and mobile

### 4. Source Attribution
- If the content comes from wiki pages or raw sources, include source links/citations
- Add a subtle footer noting the source file and generation date
- Preserve any existing citations from the markdown

## Step-by-Step Workflow

### Step 1: Identify the Source Content

Determine what to convert:

| Source Type | How to Find It |
|------------|----------------|
| Wiki page | `read_file` the local `wiki/<category>/<slug>.md` |
| Raw source | Read `raw/<slug>.md` from Azure DevOps through MCP tools or a confirmed-current local checkout (or `read_file` a `KB-Local/` note) |
| LLM response | Use the text from the current conversation |
| Markdown file | Read from the specified file path |
| Multiple files | Process each one, optionally create an index |

If the user doesn't specify, ask:
- **What content** to convert (file path, topic, or "the last response")
- **Scope**: single page or batch conversion

### Step 2: Ensure `html-files/` Directory Exists

Create the directory if it doesn't exist:
```
html-files/
```

### Step 3: Analyze and Restructure the Content

Before converting to HTML, **restructure for clarity**:

1. **Extract the core message** — what is this page fundamentally about?
2. **Identify the structure** — is it a concept explanation, comparison, entity profile, analysis, or narrative?
3. **Group related information** — sections, subsections, related points
4. **Identify visual opportunities**:
   - Lists → card grids or styled lists
   - Comparisons → tables or side-by-side layouts
   - Processes → step diagrams or numbered flows
   - Key facts → callout boxes or highlight cards
   - Relationships → diagrams or link maps
5. **Decide on layout** — single column narrative, two-column layout, card grid, etc.

### Step 4: Generate the HTML

Build a self-contained HTML file following this template structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title] — SE Brain</title>
  <style>
    /* Dark theme by default with clean typography */
    /* All styles inline — no external dependencies */
  </style>
</head>
<body>
  <!-- Hero / Title Section -->
  <!-- Core Concept / Overview -->
  <!-- Main Content (cards, tables, lists, narrative) -->
  <!-- Source Attribution Footer -->
</body>
</html>
```

#### Styling Guidelines

- **Color scheme**: Dark background (`#0f1117`), light text, accent colors for headings and highlights
- **Typography**: System fonts (`'Segoe UI', system-ui, -apple-system, sans-serif`), comfortable line-height (1.6-1.7)
- **Max width**: Content capped at ~1100px, centered
- **Cards**: Subtle background (`#1a1d27`), rounded corners (12px), 1px border
- **Tables**: Full-width, clean headers, hover row highlighting
- **Code**: Monospace font, subtle background, rounded corners
- **Responsive**: Stack columns on mobile, adjust font sizes

#### Content Element Mapping

Map markdown elements to enhanced HTML:

| Markdown Element | HTML Enhancement |
|-----------------|-----------------|
| `# Heading` | Hero section or major section divider with accent color |
| `## Heading` | Section heading with bottom border |
| Bullet lists | Styled lists with custom markers or card grids |
| Tables | Full-width styled tables with hover effects |
| `> Blockquote` | Callout box with left accent border |
| Code blocks | Syntax-highlighted pre blocks |
| Bold/emphasis | Accent-colored strong text |
| Links | Styled links (if to other HTML explainers, update paths) |
| YAML frontmatter | Parse for metadata, display as subtle header info |

### Step 5: Add Source Attribution

At the bottom of every HTML file, include:

```html
<footer>
  Source: <file-path> · Generated: <date> · SE Brain HTML Explainer
</footer>
```

If the content cites raw sources or wiki pages, preserve those citations in the body.

### Step 6: Save the File

Save to `html-files/<slug>.html`.

### Step 7: Update the HTML Index (Optional)

If `html-files/index.html` exists, add the new page. If the user is doing a batch conversion, create or update the index with all generated pages:

```html
<!-- Simple catalog of all explainer pages -->
<ul>
  <li><a href="cap-theorem.html">CAP Theorem</a> — from wiki/concepts/cap-theorem.md</li>
  <li><a href="raft-vs-paxos.html">Raft vs Paxos</a> — from wiki/comparisons/raft-vs-paxos.md</li>
</ul>
```

### Step 8: Report to User

Tell the user:
- What was generated and where it's saved
- How to open it (just open the `.html` file in a browser)
- Any content that was restructured significantly (so they can verify)

## Batch Conversion

When converting multiple files at once:

1. Identify all source files (e.g., "convert all wiki concepts to HTML")
2. Process each file through Steps 3-6
3. Create or update `html-files/index.html` as a catalog
4. Report summary: how many pages generated, total

## Content-Type Templates

### For Concept Pages
- Hero with concept name and one-line definition
- "What is it?" overview section
- Key points as a card grid
- Source comparison table (how different sources discuss it)
- Related concepts as linked cards
- Contradictions as a callout box

### For Comparison Pages
- Hero with "X vs Y" title
- Side-by-side comparison table (the main event)
- Narrative synthesis below the table
- Source citations per dimension

### For Entity Pages
- Hero with entity name and type badge
- Quick facts card (founded, location, key people, etc.)
- Narrative description
- Appearances across sources
- Related entities and concepts

### For Analysis Pages
- Hero with the original question
- Short answer callout box
- Detailed analysis sections
- Evidence table
- Contradictions and caveats
- Related pages

### For Overview / Long Responses
- Hero with topic and scope
- Table of contents (anchor links)
- Progressive sections with visual breaks
- Key takeaway boxes throughout
- Summary / conclusion section

## Tips

- **Don't just wrap markdown in HTML.** Restructure for clarity. A good explainer page rethinks the information architecture.
- **Use color meaningfully.** Different accent colors for different content types (blue for facts, orange for warnings, green for key takeaways).
- **Keep it scannable.** A reader should get the gist in 30 seconds by scanning headings, cards, and callout boxes.
- **Preserve citations.** The wiki's strength is traceability — don't lose source links when converting to HTML.
- **Test in a browser.** After generating, mentally verify the layout makes sense. Offer to adjust if the user wants changes.

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Content is too long for one page | Add a table of contents with anchor links, or split into multiple pages |
| Source file has no clear structure | Impose structure: extract a definition, list key points, note questions |
| Images referenced in markdown | Copy image references; if they're in `raw/assets/`, use relative paths from `html-files/` |
| User wants a different color scheme | Adjust the CSS variables; the template uses CSS custom properties for easy theming |
| Batch conversion produces too many files | Offer to create a consolidated single-page explainer instead |
