---
title: "MCP Integration"
type: concept
created: "2026-05-19"
updated: "2026-05-19"
sources: [raw/work--projects-customers-overview-3months.md]
tags: [mcp, model-context-protocol, integration, architecture, federation]
backlinks: [wiki/sources/work-projects-customers-overview.md, wiki/entities/indigo-airlines.md, wiki/entities/tcs.md, wiki/concepts/agentic-ai.md]
---

# MCP Integration

## Definition

**Model Context Protocol (MCP)** is an open standard for connecting AI models/agents to external tools and data sources. In the context of current engagements, MCP serves as the **architectural glue** enabling federated knowledge graphs, multi-source agent systems, and cross-platform integrations (Snowflake, Blue Prism, enterprise data).

## Key Points

- MCP is a **unifying technical pattern** across multiple engagements — appears in IndiGo (federated knowledge graph), TCS (Blue Prism integration), and is part of the broader agentic architecture. (from [overview source](../../raw/work--projects-customers-overview-3months.md))
- IndiGo uses MCP for **federated knowledge graph architecture** — connecting agents to multiple enterprise data sources (CLMS, Crew Portal, PEP, Snowflake). (from [overview source](../../raw/work--projects-customers-overview-3months.md))
- TCS explored **Blue Prism + Copilot via MCP-based integration** — connecting RPA tools to AI. (from [overview source](../../raw/work--projects-customers-overview-3months.md))
- MCP + Snowflake integration is in progress at IndiGo. (from [overview source](../../raw/work--projects-customers-overview-3months.md))

## How Sources Relate to This Concept

| Source | Perspective | Key Contribution |
|--------|------------|-----------------|
| [Work Overview](../sources/work-projects-customers-overview.md) | Portfolio synthesis | Identifies MCP as a recurring architectural pattern across engagements |

## Implementation Patterns

### 1. Federated Knowledge Graph (IndiGo)
- MCP connects multiple enterprise data sources
- Enables agents to query across CLMS, Crew Portal, PEP
- Snowflake integration via MCP in progress

### 2. RPA + AI Integration (TCS)
- Blue Prism connected to Copilot via MCP
- Bridges legacy automation with AI-native workflows

### 3. Agent-to-Tool Connectivity
- Standard protocol for agents to invoke external tools
- Enables multi-agent orchestration patterns
- Supports the "agentic touchpoints in business processes" vision

## Significance

MCP is emerging as the **infrastructure layer** for agentic systems — it's not a product feature but an architectural decision that determines how agents interact with the world. Deep MCP expertise is a differentiator as the ecosystem matures.

## Open Questions

- How does MCP scale in production with many concurrent agents?
- What's the security model for MCP connections to sensitive enterprise data?
- How does MCP evolve for multi-agent-to-multi-agent communication (not just agent-to-tool)?

## Related Concepts

- [Agentic AI](agentic-ai.md) — MCP enables agentic systems to interact with external world
- [Agentic DevOps](agentic-devops.md) — potential MCP-based pipeline integrations

## Related Entities

- [IndiGo Airlines](../entities/indigo-airlines.md) — federated knowledge graph via MCP
- [TCS](../entities/tcs.md) — Blue Prism + Copilot MCP integration
