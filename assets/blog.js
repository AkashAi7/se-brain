/* ============================================================
   SE Brain — blog engine
   Markdown + YAML-frontmatter posts, rendered client-side.
   No build step. Works on GitHub Pages and any static server.

   Authoring a post:
     1. Add  blog/posts/<slug>.md  (with YAML frontmatter)
     2. Add  "<slug>"  to  blog/posts.json
   It then appears on the blog index (newest first).

   Note: posts load via fetch(), so preview with a static server
   (e.g. `python -m http.server`) — opening from file:// will block
   the fetch. On GitHub Pages it just works.
   ============================================================ */
(() => {
  "use strict";

  const containers = document.querySelectorAll("[data-blog]");
  if (!containers.length) return;

  /* ---------- path helpers (subpath / GitHub Pages safe) ---------- */
  function joinPath(base, rest) {
    if (!base || base === "." || base === "./") return rest;
    return base.replace(/\/+$/, "") + "/" + rest;
  }
  function linkBaseFrom(base) {
    if (!base || base === "." || base === "./") return "";
    return base.replace(/\/+$/, "") + "/";
  }

  /* ---------- tiny YAML frontmatter parser (key: value + tags) ---------- */
  function parseFrontMatter(text) {
    const m = /^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n?/.exec(text);
    if (!m) return { data: {}, body: text };
    const data = {};
    const unquote = (s) => s.replace(/^["']|["']$/g, "");
    m[1].split(/\r?\n/).forEach((line) => {
      if (!line.trim() || /^\s*#/.test(line)) return;
      const idx = line.indexOf(":");
      if (idx === -1) return;
      const key = line.slice(0, idx).trim();
      let val = line.slice(idx + 1).trim();
      if (key === "tags") {
        val = val.replace(/^\[|\]$/g, "");
        data.tags = val
          ? val.split(",").map((s) => unquote(s.trim())).filter(Boolean)
          : [];
      } else {
        data[key] = unquote(val);
      }
    });
    return { data, body: text.slice(m[0].length) };
  }

  /* ---------- formatting ---------- */
  function formatDate(s) {
    if (!s) return "";
    const parts = String(s).split("-").map(Number);
    const [y, mo, d] = parts;
    if (!y) return s;
    const dt = new Date(y, (mo || 1) - 1, d || 1);
    return dt.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  }
  function readingTime(body) {
    const words = (body || "").trim().split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 200));
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );
  }

  /* ---------- data loading ---------- */
  async function fetchText(url) {
    const res = await fetch(url, { cache: "no-cache" });
    if (!res.ok) throw new Error("HTTP " + res.status + " for " + url);
    return res.text();
  }
  async function loadManifest(base) {
    const json = JSON.parse(await fetchText(joinPath(base, "posts.json")));
    return Array.isArray(json) ? json : json.posts || [];
  }
  async function loadPost(base, slug) {
    const text = await fetchText(joinPath(base, "posts/" + slug + ".md"));
    const { data, body } = parseFrontMatter(text);
    return {
      slug,
      title: data.title || slug,
      date: data.date || "",
      category: data.category || "Note",
      description: data.description || "",
      tags: data.tags || [],
      readingTime: readingTime(body),
      body,
    };
  }
  async function loadAll(base) {
    const slugs = await loadManifest(base);
    const posts = await Promise.all(
      slugs.map((s) => loadPost(base, s).catch((e) => (console.error(e), null)))
    );
    return posts
      .filter(Boolean)
      .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  }

  /* ---------- rendering: cards ---------- */
  function cardHTML(post, linkBase) {
    const href = linkBase + "post.html?slug=" + encodeURIComponent(post.slug);
    const meta = [post.category, formatDate(post.date)].filter(Boolean).join(" · ");
    return (
      '<a class="blog-card reveal in" href="' + href + '">' +
      '<span class="blog-meta">' + esc(meta) + "</span>" +
      "<h3>" + esc(post.title) + "</h3>" +
      "<p>" + esc(post.description) + "</p>" +
      '<span class="blog-link">' + post.readingTime + " min read <span aria-hidden=\"true\">→</span></span>" +
      "</a>"
    );
  }
  function renderList(el, posts, limit) {
    const linkBase = linkBaseFrom(el.dataset.base || ".");
    const list = limit ? posts.slice(0, limit) : posts;
    el.innerHTML = list.length
      ? list.map((p) => cardHTML(p, linkBase)).join("")
      : '<p class="blog-empty">No posts yet — check back soon.</p>';
    const count = document.querySelector("[data-blog-count]");
    if (count) count.textContent = posts.length + (posts.length === 1 ? " post" : " posts");
  }
  function renderListError(el) {
    const linkBase = linkBaseFrom(el.dataset.base || ".");
    el.innerHTML =
      '<p class="blog-empty">Posts load from local files — preview with a static ' +
      "server (e.g. <code>python -m http.server</code>). " +
      '<a href="' + linkBase + 'index.html">Open the blog →</a></p>';
  }

  /* ---------- rendering: single post ---------- */
  function renderPost(el, post) {
    document.title = post.title + " — SE Brain blog";
    const md = document.querySelector('meta[name="description"]');
    if (md && post.description) md.setAttribute("content", post.description);

    const meta = [post.category, formatDate(post.date), post.readingTime + " min read"]
      .filter(Boolean)
      .join(" · ");
    const tags = (post.tags || [])
      .map((t) => '<span class="post-tag">' + esc(t) + "</span>")
      .join("");

    let bodyHTML = window.marked ? marked.parse(post.body) : esc(post.body);
    if (window.DOMPurify) bodyHTML = DOMPurify.sanitize(bodyHTML);

    el.innerHTML =
      '<span class="post-meta">' + esc(meta) + "</span>" +
      '<h1 class="post-title">' + esc(post.title) + "</h1>" +
      (tags ? '<div class="post-tags">' + tags + "</div>" : "") +
      '<div class="prose">' + bodyHTML + "</div>";
  }

  function getSlug() {
    return new URLSearchParams(location.search).get("slug") || "";
  }

  /* ---------- boot ---------- */
  if (window.marked && marked.setOptions) {
    marked.setOptions({ gfm: true, breaks: false });
  }

  containers.forEach(async (el) => {
    const mode = el.dataset.blog;
    const base = el.dataset.base || ".";
    try {
      if (mode === "home") {
        renderList(el, await loadAll(base), parseInt(el.dataset.limit || "3", 10));
      } else if (mode === "index") {
        renderList(el, await loadAll(base), 0);
      } else if (mode === "post") {
        const slug = getSlug();
        if (!slug) {
          el.innerHTML = '<p class="blog-empty">No post specified. <a href="index.html">Back to the blog →</a></p>';
          return;
        }
        renderPost(el, await loadPost(base, slug));
      }
    } catch (e) {
      console.error(e);
      if (mode === "post") {
        el.innerHTML =
          '<p class="blog-empty">Could not load this post. <a href="index.html">Back to the blog →</a></p>';
      } else {
        renderListError(el);
      }
    }
  });
})();
