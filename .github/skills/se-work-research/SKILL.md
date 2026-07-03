---
name: se-work-research
description: 'Research topics from internal work sources (Outlook emails, Teams messages, meetings, documents) using the WorkIQ MCP server. Use when asked to "check work emails about", "find internal context on", "what did the team discuss about", "pull from emails", "gather internal sources", "work research on", "find meeting notes about", "what emails mention X", or when building source material from Microsoft 365 workplace data. Saves results as immutable raw source files in raw/ directory, same as se-open-research but from internal workplace sources.'
---

# Work Research

Gather raw sources from **internal workplace data** — Outlook emails, Teams messages, meetings, calendar events, and shared documents — using the [WorkIQ MCP server](https://github.com/microsoft/work-iq). This skill populates the **Raw sources** layer of the LLM Wiki pattern with internal/organizational knowledge that isn't available on the public internet.

> **Where sources are saved (updated model):** the shared raw dump now lives in **Azure DevOps** at `https://dev.azure.com/SE-Brain-AzDev/SE-Brain`, repo path `raw/`. Write shared work-derived sources under `raw/work--<slug>.md` (keep the `work--` prefix and `source_origin: work-research` frontmatter), update `raw/sources.md`, and commit/open an Azure DevOps PR unless the user asks for local-only staging. Strictly-private results go to local `KB-Local/` instead. The `raw/` paths below are paths in the Azure DevOps repo checkout. The wiki is built locally by **se-wiki-generator** from this dump.

## When to Use This Skill

- User wants to research a topic from internal communications
- User says "check work emails about X", "what did the team say about X"
- User says "find internal context on X", "pull from emails about X"
- User says "gather internal sources on X", "work research on X"
- User says "what meetings discussed X", "find Teams messages about X"
- User wants to combine internal knowledge with external research (use alongside **se-open-research**)
- User is building context for onboarding from real workplace conversations

## Prerequisites

- **WorkIQ MCP server** configured and accessible (`mcp_workiq_ask_work_iq` tool available)
- User must have accepted the WorkIQ EULA (`mcp_workiq_accept_eula` if prompted)
- Microsoft 365 account with access to Outlook, Teams, Calendar, SharePoint/OneDrive
- File creation tools to write sources to disk
- The workspace should have (or will get) a `raw/` directory at the project root

## How It Differs from Open Research

| Aspect | se-open-research | se-work-research |
|--------|--------------|---------------|
| Source | Public internet (web articles, papers) | Microsoft 365 (emails, Teams, meetings, docs) |
| Tool | `fetch_webpage` | `mcp_workiq_ask_work_iq` |
| Content type | Articles, papers, blog posts | Emails, meeting notes, chat threads, shared docs |
| Source type tag | `article`, `paper`, `blog` | `email`, `meeting`, `teams-message`, `document` |
| Privacy | Public content | Internal/confidential — treat carefully |

## Directory Structure

Same as se-open-research — sources land in `raw/`:

```
raw/
├── sources.md              # Manifest (shared with se-open-research sources)
├── assets/                 # Downloaded attachments if relevant
├── <source-slug>.md        # Individual source documents from work
└── ...
```

### File Naming Convention

Derive slugs from the email subject, meeting title, or query topic:
- Lowercase, hyphens instead of spaces, no special characters
- Prefix with `work--` to distinguish from internet sources
- Max 60 characters for the slug portion
- Examples: `work--competitor-x-pricing-thread.md`, `work--q3-security-review-meeting.md`

### Source File Format

Every source markdown file MUST include YAML frontmatter:

```yaml
---
title: "Email Thread: Competitor X Pricing Discussion"
url: "outlook://message-id-or-reference"
date_retrieved: "2026-05-19"
source_type: email | meeting | teams-message | document | calendar
source_origin: work-research
tags: [competitor-intel, pricing]
participants: [person-a, person-b]
date_original: "2026-05-15"
---
```

**Additional fields vs se-open-research:**
- `source_origin: work-research` — marks this as internal workplace data
- `participants` — people involved in the email/meeting/thread
- `date_original` — when the original communication happened (not when retrieved)

## Step-by-Step Workflow

### Step 1: Clarify the Research Topic

Ask the user (if not already clear):
- **What topic** to research from work communications
- **Scope**: specific person's emails, specific time range, specific project/topic
- **Source preferences**: emails only, meetings only, or all available data
- **Time range**: last week, last month, all time (narrow is better for relevance)

### Step 2: Ensure Directory Structure Exists

Ensure `raw/` and `raw/assets/` exist. If `raw/sources.md` already exists, read it to avoid duplicating existing sources.

### Step 3: Query WorkIQ for Relevant Content

Use the `mcp_workiq_ask_work_iq` tool to search workplace data. Strategy:

1. **Start with the main question** — ask WorkIQ directly about the topic
2. **Follow up on key threads** — if WorkIQ surfaces specific email threads or meetings, ask for more detail
3. **Ask about specific people** — "What has [person] said about [topic]?"
4. **Check meetings** — "Were there any meetings about [topic] in the last month?"
5. **Look for documents** — "Are there any shared documents about [topic]?"

**Example queries to WorkIQ:**
- "What emails discuss our competitive positioning against Competitor X?"
- "What was discussed in meetings about the Q3 security initiative?"
- "What has the SE team said about cloud-native architecture?"
- "Find any documents shared about customer onboarding workflows"
- "What did [person] communicate about [project] last month?"

### Step 4: Convert Results to Source Documents

**This step is MANDATORY — do not skip it.** Every substantive result from WorkIQ MUST be written to disk as a markdown file in `raw/`. Do not just report findings to the user — actually create the files.

For each substantive result from WorkIQ:

1. **Extract the key content** — the actual information, discussion points, decisions made
2. **Structure as clean markdown** preserving:
   - Who said what (attribute quotes/points to people)
   - Timeline of the discussion
   - Any decisions or action items mentioned
   - Links to documents or resources shared
3. **Generate YAML frontmatter** with all required fields:
   ```yaml
   ---
   title: "<Descriptive title>"
   url: "outlook://message-id-or-reference"
   date_retrieved: "<today's date>"
   source_type: email | meeting | teams-message | document | calendar
   source_origin: work-research
   tags: [tag1, tag2]
   participants: [person-a, person-b]
   date_original: "<when the original communication happened>"
   ---
   ```
4. **Create the file** at `raw/work--<slug>.md` using the file creation tool
5. **Verify the file was created** before moving to the next result

**Important:** Summarize and extract insights — don't dump raw email bodies wholesale. Focus on the knowledge content, not the email formatting. But DO create the actual file — the whole point is populating `raw/` for the wiki pipeline.

### Step 5: Handle Sensitive Content

Workplace data may contain sensitive information. Follow these rules:

- **Keep factual content** — product decisions, technical discussions, competitive intel, architecture choices
- **Attribute carefully** — note who said what, but don't include personal/HR-related content
- **Flag confidentiality** — if a source contains confidential info, add a `confidential: true` frontmatter field
- **Don't store credentials** — never save API keys, passwords, or secrets found in emails
- **Respect context** — "off the record" or clearly personal messages should be excluded

### Step 6: Update the Source Manifest

**This step is MANDATORY.** After all source files are created, update `raw/sources.md`:

- If `raw/sources.md` does not exist, create it with the full manifest template (see se-open-research skill for format)
- If it exists, append the new entries to the existing table
- Increment the source count in the Summary section

```markdown
| # | Title | Type | Tags | File |
|---|-------|------|------|------|
| 14 | [Competitor X Pricing Thread](outlook://ref) | email | competitor-intel, pricing | [work--competitor-x-pricing-thread.md](work--competitor-x-pricing-thread.md) |
| 15 | [Q3 Security Review Meeting](outlook://ref) | meeting | security, quarterly | [work--q3-security-review-meeting.md](work--q3-security-review-meeting.md) |
```

### Step 7: Report Results and Offer Wiki Build

Provide a summary:
- How many internal sources were collected and saved to `raw/`
- Brief description of each (1 line)
- Key people/threads surfaced
- Suggestions for follow-up queries or areas to dig deeper
- Note if any results seem stale or contradictory

**Then immediately offer the next steps in this order:**

1. **"Would you like me to build/update the wiki from these sources?"** — Trigger the se-wiki-generator skill to ingest the new raw sources into structured wiki pages.
2. **"Would you also like me to do se-open-research on this topic?"** — Suggest complementing internal knowledge with external public sources for full coverage.

**Do NOT stop after just reporting.** The natural flow is:
```
se-work-research (query + save to raw/) → se-wiki-generator (ingest into wiki/) → done
```

If the user says yes to wiki build, immediately proceed to run the se-wiki-generator skill's Ingest workflow on the newly created sources.

## Immutability Rule

**Files in `raw/` are IMMUTABLE once written.** The LLM must never modify an existing source file. If a source needs to be updated (e.g., a newer email thread has additional replies), save it as a new file with a version suffix (e.g., `work--competitor-x-pricing-thread-v2.md`) and update the manifest.

The only exception is `raw/sources.md`, which is updated whenever new sources are added.

## Combining with Open Research

The most powerful workflow combines both skills:

1. **se-work-research** first — gather what the team already knows internally
2. **se-open-research** second — fill gaps with external public sources
3. **se-wiki-generator** — build the wiki from both internal and external sources together

This gives the wiki a mix of:
- What the market/industry says (external)
- What your team actually thinks/knows/decided (internal)

## Tips

- **Be specific with time ranges.** "Emails about X from the last 2 weeks" gets better results than "all emails about X ever."
- **Name people when relevant.** "What did Sarah share about the integration?" is more targeted than "any emails about the integration."
- **Combine queries.** If the first query gives partial results, follow up with more specific questions.
- **Internal sources are gold for onboarding.** They capture decisions, context, and tribal knowledge that no public source has.
- **Mark internal sources clearly.** The `work--` prefix and `source_origin: work-research` field make it easy to distinguish internal vs. external sources in the wiki.
- **Don't over-collect.** 5-10 well-chosen internal sources beat 50 random email snippets.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| WorkIQ returns "no results" | Broaden the query, try different keywords, check time range |
| WorkIQ needs EULA acceptance | Call `mcp_workiq_accept_eula` first, then retry |
| Results are too noisy | Narrow by person, date range, or specific project name |
| Sensitive content in results | Summarize the factual content only, skip personal/HR topics |
| Duplicate with existing raw sources | Check `raw/sources.md` manifest before saving; skip duplicates |
| WorkIQ tool not available | Ensure the WorkIQ MCP server is configured in VS Code settings |
