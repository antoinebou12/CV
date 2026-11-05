# donneesqc-mcp: An MCP gateway to public data

> donneesqc-mcp is a fork exposing Québec and Montréal open-data operations through MCP tools. Its entry point registers the tool collection and starts an…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/donneesqc-mcp/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/donneesqc-mcp/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/donneesqc-mcp
- License: MIT
- Inspected revision: 53a6ee4209c44ccfe360556a1b86c29d855f3e2f

## Summary

donneesqc-mcp is a fork exposing Québec and Montréal open-data operations through MCP tools. Its entry point registers the tool collection and starts an HTTP transport, leaving dataset access and geographic helpers in separate modules.

**Why it exists:** Production MCP server connecting AI assistants to Quebec & Montreal open data APIs with strict schema validation.

**Best fit:** Natural language querying of public municipal and provincial datasets across transportation, demographics, and municipal services.

## Use cases

An MCP server that lets AI agents search, query in SQL and map Québec and Montréal open data in conversation.

- **Search open datasets** (Analyst with an agent, CKAN open data portals): search_datasets and search_montreal_datasets call the CKAN APIs of Données Québec and Montréal (DQ_API_URL, MTL_API_URL) through helpers/ckan_api.py.
- **Run read-only SQL queries** (Analyst with an agent, CKAN open data portals): query_resource_sql and query_montreal_sql send SQL to the CKAN DataStore after validate_sql() rejects anything that is not a SELECT.
- **Find and query in one call** (Analyst with an agent, CKAN open data portals): find_and_query chains search, resource listing and DataStore query so the agent avoids three round trips.
- **Explore geospatial layers** (Analyst with an agent, IGO geo services): list_geospatial_layers, get_geospatial_features and get_map_url query the IGO WFS and build WMS GetMap URLs through helpers/geo_api.py.
- **Geocode, convert coordinates** (Analyst with an agent, IGO geo services): geocode and reverse_geocode use the icherche geocoder (GEOCODER_URL); convert_coordinates switches between EPSG:32198 and EPSG:4326.

### Scenario: Counting public trees per borough in Montréal

1. Start the server with docker compose up -d (or uv sync then uv run python main.py); it listens on port 8000 with streamable HTTP.
2. Register it in the client, for example claude mcp add --transport http donneesqc http://localhost:8000/mcp.
3. Ask the agent for public tree data; it calls search_montreal_datasets to find the dataset.
4. The agent calls query_montreal_data to see the columns of the DataStore resource.
5. It sends a SELECT … GROUP BY query through query_montreal_sql and answers with the per-borough counts.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 98.28 |
| Shell | 1.36 |
| Dockerfile | 0.36 |

## Getting started (repository commands, not run here)

### README.md · Installation manuelle

```bash
git clone https://github.com/Stefen-Taime/donneesqc-mcp.git
cd donneesqc-mcp
uv sync
cp .env.example .env
set -a && source .env && set +a
uv run python main.py
```

### README.md · Quick start

```bash
git clone https://github.com/Stefen-Taime/donneesqc-mcp.git
cd donneesqc-mcp
docker compose up -d
```


## Features and components

- **Server bootstrap** — main.py configures logging, optionally initializes Sentry, calls register_all_tools and runs the MCP object with streamable-http. Monitoring is optional; it is not the mechanism that serves dataset queries.
- **Data-service boundary** — The documented tool groups cover catalog discovery, CKAN DataStore access, resource downloads and geographic enrichment. A catalog result describes a resource; the actual table or file is a separate request and may use a different format.

## Architecture

Components and connections verified in the repository.

- MCP client → Registered HTTP tools
- Registered HTTP tools → Catalog search
- Catalog search → Table or file resource
- Table or file resource → Structured result
- Structured result → MCP client

```mermaid
flowchart LR
  n0["MCP client"]
  n1["Registered HTTP tools"]
  n2["Catalog search"]
  n3["Table or file resource"]
  n4["Structured result"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n0
```

**One path through the code:** Follow main into register_all_tools, then choose the dataset-access tool behind a catalog result. Resource identifiers, formats and geographic coordinate systems matter more than a dataset title alone.

## Constraints and checks

Open-data catalogs and schemas can change. A successful catalog query does not prove that every resource is fresh, complete or compatible with a downstream calculation.

## Files to read

- [main.py](https://github.com/antoinebou12/donneesqc-mcp/blob/main/main.py)
- [tools/__init__.py](https://github.com/antoinebou12/donneesqc-mcp/blob/main/tools/__init__.py)
- [README.md](https://github.com/antoinebou12/donneesqc-mcp/blob/main/README.md)


