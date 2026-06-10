#!/usr/bin/env python3
"""
Build a lightweight knowledge-graph view of the wiki/ folder.

Scans every wiki/**/*.md file, extracts YAML-ish frontmatter
(title, type, tags, backlinks, sources) plus inline markdown links,
and emits a single self-contained index.html next to this script.

No external Python deps. Run:  python build_graph.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OUT = Path(__file__).resolve().parent / "index.html"

TYPE_COLORS = {
    "index": "#f59e0b",
    "overview": "#f97316",
    "concept": "#38bdf8",
    "entity": "#a78bfa",
    "source-summary": "#34d399",
    "comparison": "#f472b6",
    "analysis": "#fb7185",
    "unknown": "#94a3b8",
}

FM_LIST_KEYS = ("backlinks", "sources", "tags")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)[^)]*\)")


def parse_frontmatter(text):
    """Return (frontmatter_dict, body) from a markdown string."""
    fm = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end].strip("\n")
            body = text[end + 4 :]
            for line in block.splitlines():
                if ":" not in line:
                    continue
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip()
                if key in FM_LIST_KEYS:
                    val = val.strip("[]")
                    items = [v.strip().strip('"').strip("'") for v in val.split(",")]
                    fm[key] = [i for i in items if i]
                else:
                    fm[key] = val.strip('"').strip("'")
    return fm, body


def rel_id(path):
    """Stable node id: posix path relative to repo root, e.g. wiki/concepts/x.md"""
    return path.relative_to(ROOT).as_posix()


def resolve_link(src_path, target):
    """Resolve a markdown link target (relative or wiki/-rooted) to a node id."""
    target = target.split("#")[0].strip()
    if not target:
        return None
    if target.startswith("wiki/") or target.startswith("raw/"):
        return target
    try:
        resolved = (src_path.parent / target).resolve()
        return resolved.relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return None


def main():
    files = sorted(WIKI.rglob("*.md"))
    nodes = {}
    edges = set()  # (source_id, target_id, kind)

    for f in files:
        nid = rel_id(f)
        text = f.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        ntype = fm.get("type", "unknown")
        words = len(body.split())
        nodes[nid] = {
            "id": nid,
            "label": fm.get("title", f.stem),
            "type": ntype,
            "tags": fm.get("tags", []),
            "folder": f.parent.name if f.parent != WIKI else "wiki",
            "words": words,
        }

    valid = set(nodes)

    for f in files:
        nid = rel_id(f)
        text = f.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)

        # inline links found in the body -> outgoing references
        for m in LINK_RE.finditer(body):
            tgt = resolve_link(f, m.group(1))
            if tgt and tgt in valid and tgt != nid:
                edges.add((nid, tgt, "link"))

        # backlinks frontmatter -> incoming references (other -> this)
        for bl in fm.get("backlinks", []):
            src = bl if bl.startswith("wiki/") else "wiki/" + bl
            if src in valid and src != nid:
                edges.add((src, nid, "link"))

    node_list = list(nodes.values())
    # degree for sizing
    deg = {n["id"]: 0 for n in node_list}
    for s, t, _ in edges:
        deg[s] = deg.get(s, 0) + 1
        deg[t] = deg.get(t, 0) + 1
    for n in node_list:
        n["degree"] = deg.get(n["id"], 0)

    edge_list = [{"from": s, "to": t, "kind": k} for (s, t, k) in sorted(edges)]

    data = {"nodes": node_list, "edges": edge_list, "colors": TYPE_COLORS}
    html = TEMPLATE.replace("/*__DATA__*/", json.dumps(data, indent=2))
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  {len(node_list)} nodes, {len(edge_list)} edges")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Wiki Knowledge Graph</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
  :root {
    --bg: #0b1020;
    --panel: #121933;
    --panel-2: #1a2342;
    --border: #26304f;
    --text: #e6ecff;
    --muted: #93a0c7;
    --accent: #38bdf8;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); }
  #app { display: flex; height: 100vh; overflow: hidden; }
  #graph { flex: 1; height: 100%; background: radial-gradient(circle at 30% 20%, #131c3a 0%, #0b1020 60%); }
  aside { width: 320px; flex-shrink: 0; background: var(--panel); border-left: 1px solid var(--border); display: flex; flex-direction: column; }
  header { padding: 18px 20px 14px; border-bottom: 1px solid var(--border); }
  header h1 { margin: 0; font-size: 16px; letter-spacing: .3px; }
  header p { margin: 6px 0 0; font-size: 12px; color: var(--muted); }
  .section { padding: 16px 20px; border-bottom: 1px solid var(--border); }
  .section h2 { margin: 0 0 10px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); font-weight: 600; }
  #search { width: 100%; padding: 9px 11px; border-radius: 8px; border: 1px solid var(--border); background: var(--panel-2); color: var(--text); font-size: 13px; outline: none; }
  #search:focus { border-color: var(--accent); }
  .legend-item { display: flex; align-items: center; gap: 9px; font-size: 13px; padding: 4px 0; cursor: pointer; user-select: none; opacity: .95; }
  .legend-item .dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; box-shadow: 0 0 8px rgba(0,0,0,.4); }
  .legend-item.off { opacity: .35; }
  .legend-item .count { margin-left: auto; color: var(--muted); font-size: 12px; }
  #details { flex: 1; overflow-y: auto; padding: 16px 20px; }
  #details .empty { color: var(--muted); font-size: 13px; line-height: 1.6; }
  #details .title { font-size: 15px; font-weight: 600; margin: 0 0 4px; }
  #details .badge { display: inline-block; font-size: 11px; padding: 2px 9px; border-radius: 20px; color: #0b1020; font-weight: 600; margin-bottom: 12px; }
  #details .path { font-size: 11px; color: var(--muted); word-break: break-all; margin-bottom: 14px; font-family: ui-monospace, "SF Mono", Menlo, monospace; }
  #details .meta { font-size: 12px; color: var(--muted); margin: 10px 0 4px; text-transform: uppercase; letter-spacing: .5px; }
  .tags { display: flex; flex-wrap: wrap; gap: 6px; }
  .tag { font-size: 11px; background: var(--panel-2); border: 1px solid var(--border); color: var(--muted); padding: 2px 8px; border-radius: 6px; }
  .links a { display: block; font-size: 12px; color: var(--accent); text-decoration: none; padding: 3px 0; cursor: pointer; }
  .links a:hover { text-decoration: underline; }
  .stat-row { display: flex; gap: 18px; }
  .stat { flex: 1; }
  .stat .num { font-size: 22px; font-weight: 700; }
  .stat .lbl { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; }
  .controls { display: flex; gap: 8px; }
  .controls button { flex: 1; padding: 8px; font-size: 12px; border-radius: 7px; border: 1px solid var(--border); background: var(--panel-2); color: var(--text); cursor: pointer; }
  .controls button:hover { border-color: var(--accent); color: var(--accent); }
</style>
</head>
<body>
<div id="app">
  <div id="graph"></div>
  <aside>
    <header>
      <h1>Wiki Knowledge Graph</h1>
      <p id="subtitle">Loading…</p>
    </header>
    <div class="section">
      <input id="search" type="text" placeholder="Search nodes…" autocomplete="off" />
    </div>
    <div class="section">
      <h2>Node Types</h2>
      <div id="legend"></div>
    </div>
    <div class="section">
      <div class="controls">
        <button id="fit">Fit view</button>
        <button id="physics">Pause motion</button>
      </div>
    </div>
    <div id="details">
      <div class="empty">Click any node to see its title, type, tags, and connections. Hover to highlight neighbours. Use the legend to toggle types.</div>
    </div>
  </aside>
</div>
<script>
const DATA = /*__DATA__*/;
const colors = DATA.colors;
const byId = {};
DATA.nodes.forEach(n => byId[n.id] = n);

function shortLabel(s){ return s.length > 34 ? s.slice(0,32) + '…' : s; }

const nodes = new vis.DataSet(DATA.nodes.map(n => ({
  id: n.id,
  label: shortLabel(n.label),
  group: n.type,
  value: 4 + n.degree,
  title: n.label + '  ·  ' + n.type,
  color: { background: colors[n.type] || colors.unknown, border: colors[n.type] || colors.unknown },
})));

const edges = new vis.DataSet(DATA.edges.map((e,i) => ({
  id: i, from: e.from, to: e.to,
})));

const container = document.getElementById('graph');
const groups = {};
Object.entries(colors).forEach(([type, col]) => {
  groups[type] = { color: { background: col, border: col, highlight: { background: col, border: '#fff' }, hover: { background: col, border: '#fff' } } };
});
const network = new vis.Network(container, { nodes, edges }, {
  groups,
  nodes: {
    shape: 'dot',
    scaling: { min: 8, max: 34, label: { enabled: true, min: 11, max: 20 } },
    font: { color: '#cdd7f5', size: 13, face: 'Segoe UI', strokeWidth: 0 },
    borderWidth: 2,
  },
  edges: {
    color: { color: 'rgba(120,140,200,0.28)', highlight: '#38bdf8', hover: '#38bdf8' },
    width: 1, hoverWidth: 1.5, smooth: { type: 'continuous' },
    arrows: { to: { enabled: true, scaleFactor: 0.4 } },
  },
  physics: {
    solver: 'forceAtlas2Based',
    forceAtlas2Based: { gravitationalConstant: -45, springLength: 110, springConstant: 0.05, avoidOverlap: 0.6 },
    stabilization: { iterations: 220 },
  },
  interaction: { hover: true, tooltipDelay: 120, navigationButtons: false },
});

// adjacency for highlighting
const adj = {};
DATA.edges.forEach(e => {
  (adj[e.from] = adj[e.from] || new Set()).add(e.to);
  (adj[e.to] = adj[e.to] || new Set()).add(e.from);
});

document.getElementById('subtitle').textContent =
  DATA.nodes.length + ' pages · ' + DATA.edges.length + ' links';

// Legend
const typeCounts = {};
DATA.nodes.forEach(n => typeCounts[n.type] = (typeCounts[n.type]||0)+1);
const hidden = new Set();
const legend = document.getElementById('legend');
Object.keys(typeCounts).sort().forEach(type => {
  const el = document.createElement('div');
  el.className = 'legend-item';
  el.innerHTML = `<span class="dot" style="background:${colors[type]||colors.unknown}"></span>`+
                 `<span>${type}</span><span class="count">${typeCounts[type]}</span>`;
  el.onclick = () => {
    if (hidden.has(type)) hidden.delete(type); else hidden.add(type);
    el.classList.toggle('off');
    applyVisibility();
  };
  legend.appendChild(el);
});

function applyVisibility(){
  const upd = DATA.nodes.map(n => ({ id: n.id, hidden: hidden.has(n.type) }));
  nodes.update(upd);
}

// Details panel
function showDetails(id){
  const n = byId[id];
  if(!n){ return; }
  const neighbours = [...(adj[id]||[])].map(x=>byId[x]).filter(Boolean)
    .sort((a,b)=>a.label.localeCompare(b.label));
  const tags = (n.tags||[]).map(t=>`<span class="tag">${t}</span>`).join('') || '<span class="empty" style="font-size:12px">none</span>';
  const links = neighbours.map(x=>`<a data-id="${x.id}">${x.label}</a>`).join('') || '<span class="empty" style="font-size:12px">none</span>';
  document.getElementById('details').innerHTML =
    `<div class="title">${n.label}</div>`+
    `<span class="badge" style="background:${colors[n.type]||colors.unknown}">${n.type}</span>`+
    `<div class="path">${n.id}</div>`+
    `<div class="stat-row"><div class="stat"><div class="num">${n.degree}</div><div class="lbl">connections</div></div>`+
    `<div class="stat"><div class="num">${n.words}</div><div class="lbl">words</div></div></div>`+
    `<div class="meta">Tags</div><div class="tags">${tags}</div>`+
    `<div class="meta">Connected pages</div><div class="links">${links}</div>`;
  document.querySelectorAll('#details .links a').forEach(a=>{
    a.onclick = () => { network.selectNodes([a.dataset.id]); network.focus(a.dataset.id,{scale:1.1,animation:true}); showDetails(a.dataset.id); };
  });
}

network.on('click', p => { if(p.nodes.length) showDetails(p.nodes[0]); });

// Hover highlight
network.on('hoverNode', p => {
  const id = p.node; const keep = new Set([id, ...(adj[id]||[])]);
  nodes.update(DATA.nodes.map(n => ({ id: n.id,
    opacity: keep.has(n.id) ? 1 : 0.15,
  })));
});
network.on('blurNode', () => {
  nodes.update(DATA.nodes.map(n => ({ id: n.id, opacity: 1 })));
});

// Search
document.getElementById('search').addEventListener('input', e => {
  const q = e.target.value.trim().toLowerCase();
  if(!q){ nodes.update(DATA.nodes.map(n=>({id:n.id, opacity:1, hidden:hidden.has(n.type)}))); return; }
  const matches = DATA.nodes.filter(n => n.label.toLowerCase().includes(q) || (n.tags||[]).some(t=>t.toLowerCase().includes(q)));
  const set = new Set(matches.map(m=>m.id));
  nodes.update(DATA.nodes.map(n=>({id:n.id, opacity: set.has(n.id)?1:0.12})));
  if(matches.length){ network.selectNodes(matches.map(m=>m.id)); }
});

document.getElementById('fit').onclick = () => network.fit({animation:true});
let physicsOn = true;
const pbtn = document.getElementById('physics');
pbtn.onclick = () => { physicsOn=!physicsOn; network.setOptions({physics:{enabled:physicsOn}}); pbtn.textContent = physicsOn ? 'Pause motion' : 'Resume motion'; };
network.once('stabilizationIterationsDone', () => network.fit({animation:true}));
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
