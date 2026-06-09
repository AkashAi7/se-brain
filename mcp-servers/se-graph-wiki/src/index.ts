import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { DefaultAzureCredential } from "@azure/identity";

// ─── Configuration ───────────────────────────────────────────────────────────
// Set via environment variables:
//   GRAPH_SITE_HOSTNAME  — e.g. "contoso.sharepoint.com"
//   GRAPH_SITE_PATH      — e.g. "/sites/SE-Brain-Wiki"
//   GRAPH_LIBRARY_NAME   — e.g. "Documents" or "Wiki" (default: "Documents")

const SITE_HOSTNAME = process.env.GRAPH_SITE_HOSTNAME!;
const SITE_PATH = process.env.GRAPH_SITE_PATH || "";
const LIBRARY_NAME = process.env.GRAPH_LIBRARY_NAME || "Documents";
const GRAPH_BASE = "https://graph.microsoft.com/v1.0";

const credential = new DefaultAzureCredential();

// ─── Graph API Helpers ───────────────────────────────────────────────────────

async function getToken(): Promise<string> {
  const token = await credential.getToken("https://graph.microsoft.com/.default");
  return token.token;
}

function headers(token: string, contentType = "application/json") {
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": contentType,
  };
}

/**
 * Resolve the SharePoint site ID from hostname + path.
 * Caches after first call.
 */
let cachedSiteId: string | null = null;
async function getSiteId(): Promise<string> {
  if (cachedSiteId) return cachedSiteId;

  const token = await getToken();
  const siteUrl = SITE_PATH
    ? `${GRAPH_BASE}/sites/${SITE_HOSTNAME}:${SITE_PATH}`
    : `${GRAPH_BASE}/sites/${SITE_HOSTNAME}`;

  const res = await fetch(siteUrl, { headers: headers(token) });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to resolve site: ${res.status} — ${err}`);
  }
  const site = (await res.json()) as { id: string };
  cachedSiteId = site.id;
  return site.id;
}

/**
 * Resolve the document library (drive) ID by name.
 * Caches after first call.
 */
let cachedDriveId: string | null = null;
async function getDriveId(): Promise<string> {
  if (cachedDriveId) return cachedDriveId;

  const token = await getToken();
  const siteId = await getSiteId();
  const res = await fetch(`${GRAPH_BASE}/sites/${siteId}/drives`, {
    headers: headers(token),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to list drives: ${res.status} — ${err}`);
  }
  const data = (await res.json()) as { value: Array<{ id: string; name: string }> };
  const drive = data.value.find(
    (d) => d.name.toLowerCase() === LIBRARY_NAME.toLowerCase()
  );
  if (!drive) {
    const available = data.value.map((d) => d.name).join(", ");
    throw new Error(
      `Drive "${LIBRARY_NAME}" not found. Available: ${available}`
    );
  }
  cachedDriveId = drive.id;
  return drive.id;
}

/**
 * Build the item-by-path URL for a file in the library.
 */
function itemPath(filePath: string): string {
  // Ensure path starts with /
  const normalized = filePath.startsWith("/") ? filePath : `/${filePath}`;
  return `root:${normalized}`;
}

// ─── Core Operations ─────────────────────────────────────────────────────────

async function readFile(filePath: string): Promise<string> {
  const token = await getToken();
  const driveId = await getDriveId();
  const url = `${GRAPH_BASE}/drives/${driveId}/${itemPath(filePath)}:/content`;

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    if (res.status === 404) {
      throw new Error(`File not found: ${filePath}`);
    }
    const err = await res.text();
    throw new Error(`Failed to read file: ${res.status} — ${err}`);
  }
  let text = await res.text();
  // Strip UTF-8 BOM if present
  if (text.charCodeAt(0) === 0xfeff) {
    text = text.slice(1);
  }
  return text;
}

async function writeFile(filePath: string, content: string): Promise<string> {
  const token = await getToken();
  const driveId = await getDriveId();
  const url = `${GRAPH_BASE}/drives/${driveId}/${itemPath(filePath)}:/content`;

  const res = await fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "text/plain",
    },
    body: content,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to write file: ${res.status} — ${err}`);
  }
  const item = (await res.json()) as { webUrl: string; lastModifiedDateTime: string };
  return `Written successfully. URL: ${item.webUrl} | Modified: ${item.lastModifiedDateTime}`;
}

async function listFiles(folderPath: string): Promise<string> {
  const token = await getToken();
  const driveId = await getDriveId();

  // Root or subfolder
  const url = folderPath && folderPath !== "/"
    ? `${GRAPH_BASE}/drives/${driveId}/${itemPath(folderPath)}:/children`
    : `${GRAPH_BASE}/drives/${driveId}/root/children`;

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to list files: ${res.status} — ${err}`);
  }
  const data = (await res.json()) as {
    value: Array<{
      name: string;
      folder?: { childCount: number };
      size: number;
      lastModifiedDateTime: string;
    }>;
  };

  const lines = data.value.map((item) => {
    const type = item.folder ? `📁 [${item.folder.childCount} items]` : `📄 ${formatSize(item.size)}`;
    return `${type} ${item.name} (${item.lastModifiedDateTime.split("T")[0]})`;
  });

  return lines.length > 0 ? lines.join("\n") : "(empty folder)";
}

async function deleteFile(filePath: string): Promise<string> {
  const token = await getToken();
  const driveId = await getDriveId();
  const url = `${GRAPH_BASE}/drives/${driveId}/${itemPath(filePath)}`;

  const res = await fetch(url, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Failed to delete: ${res.status} — ${err}`);
  }
  return `Deleted: ${filePath}`;
}

async function searchFiles(query: string): Promise<string> {
  const token = await getToken();
  const driveId = await getDriveId();
  const url = `${GRAPH_BASE}/drives/${driveId}/root/search(q='${encodeURIComponent(query)}')`;

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Search failed: ${res.status} — ${err}`);
  }
  const data = (await res.json()) as {
    value: Array<{
      name: string;
      parentReference?: { path?: string };
      webUrl: string;
      lastModifiedDateTime: string;
    }>;
  };

  if (data.value.length === 0) return `No results for: "${query}"`;

  const lines = data.value.slice(0, 20).map((item) => {
    const parent = item.parentReference?.path?.split("root:")[1] || "/";
    return `📄 ${parent}/${item.name} (${item.lastModifiedDateTime.split("T")[0]})`;
  });

  return `Found ${data.value.length} result(s):\n${lines.join("\n")}`;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

// ─── MCP Server ──────────────────────────────────────────────────────────────

const server = new McpServer({
  name: "se-graph-wiki",
  version: "1.0.0",
});

// Tool: Read a file from the wiki
server.tool(
  "wiki_read",
  "Read a markdown file from the SharePoint wiki library. Returns the file content as text.",
  {
    path: z.string().describe(
      "Path to the file relative to the document library root. Example: 'wiki/concepts/compete-landscape.md'"
    ),
  },
  async ({ path }) => {
    try {
      const content = await readFile(path);
      return { content: [{ type: "text" as const, text: content }] };
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      return { content: [{ type: "text" as const, text: `Error: ${msg}` }], isError: true };
    }
  }
);

// Tool: Write/update a file in the wiki
server.tool(
  "wiki_write",
  "Write or update a markdown file in the SharePoint wiki library. Creates parent folders automatically. Use for wiki updates, broadcasts, and data pushes.",
  {
    path: z.string().describe(
      "Path to the file relative to the document library root. Example: 'broadcasts/2026-06-08-deck-generator.md'"
    ),
    content: z.string().describe("The full content to write to the file (markdown text)."),
  },
  async ({ path, content }) => {
    try {
      const result = await writeFile(path, content);
      return { content: [{ type: "text" as const, text: result }] };
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      return { content: [{ type: "text" as const, text: `Error: ${msg}` }], isError: true };
    }
  }
);

// Tool: List files in a folder
server.tool(
  "wiki_list",
  "List files and folders in a SharePoint wiki library directory. Returns names, sizes, types, and last modified dates.",
  {
    folder: z
      .string()
      .optional()
      .describe(
        "Folder path relative to library root. Omit or use '/' for root. Example: 'wiki/concepts'"
      ),
  },
  async ({ folder }) => {
    try {
      const result = await listFiles(folder || "/");
      return { content: [{ type: "text" as const, text: result }] };
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      return { content: [{ type: "text" as const, text: `Error: ${msg}` }], isError: true };
    }
  }
);

// Tool: Search files by name or content
server.tool(
  "wiki_search",
  "Search for files in the SharePoint wiki library by keyword. Searches file names and content.",
  {
    query: z.string().describe("Search query — matches file names and content. Example: 'compete Google'"),
  },
  async ({ query }) => {
    try {
      const result = await searchFiles(query);
      return { content: [{ type: "text" as const, text: result }] };
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      return { content: [{ type: "text" as const, text: `Error: ${msg}` }], isError: true };
    }
  }
);

// Tool: Delete a file
server.tool(
  "wiki_delete",
  "Delete a file from the SharePoint wiki library. Use with caution — moves to SharePoint recycle bin (recoverable).",
  {
    path: z.string().describe("Path to the file to delete. Example: 'broadcasts/old-broadcast.md'"),
  },
  async ({ path }) => {
    try {
      const result = await deleteFile(path);
      return { content: [{ type: "text" as const, text: result }] };
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);
      return { content: [{ type: "text" as const, text: `Error: ${msg}` }], isError: true };
    }
  }
);

// ─── Start ───────────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("se-graph-wiki MCP server started");
  console.error(`  Site: ${SITE_HOSTNAME}${SITE_PATH}`);
  console.error(`  Library: ${LIBRARY_NAME}`);
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
