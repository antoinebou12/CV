---
post_kind: article
title: "Diagram prompts with ChatGPT and AIPRM (PlantUML, Mermaid, and more)"
date: 2022-09-06T10:00:00-04:00
description: "AIPRM prompt template for diagram type, elements, purpose, and tool — plus PlantUML and Mermaid sequence examples (React, FastAPI, Redis, MongoDB, cache hit/miss)."
translationKey: chatgpt-airprm-sequence-diagrams
tags:
    - ChatGPT
    - AIPRM
    - PlantUML
    - Mermaid
    - Draw.io
    - Lucidchart
    - Creately
    - Gliffy
    - UML
    - FastAPI
    - Redis
    - MongoDB
    - Diagram tools
images:
    - featured.jpeg
---

The [AIPRM](https://www.aiprm.com/) browser extension gives you reusable prompt templates inside ChatGPT. Combined with a small **structured prompt** (diagram type, what to draw, why, and which tool), you get consistent output whether you want text-first formats like **PlantUML** or **Mermaid**, or a recipe for redrawing the same flow in a canvas tool.

**[Full article in French]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.fr.md" >}})** (same slug — you can also switch to **FR** in the site header).

## AIPRM prompt template (copy and adapt)

Fill one line per dimension. You can paste the block below into ChatGPT (with or without AIPRM) and edit the bracketed values.

```text
[DIAGRAM TYPE] - Sequence | Use Case | Class | Activity | Component | State | Object | Deployment | Timing | Network | Wireframe | Archimate | Gantt | MindMap | WBS | JSON | YAML

[ELEMENT TYPE] - Actors | Messages | Objects | Classes | Interfaces | Components | States | Nodes | Edges | Links | Frames | Constraints | Entities | Relationships | Tasks | Events | Modules

[PURPOSE] - Communication | Planning | Design | Analysis | Modeling | Documentation | Implementation | Testing | Debugging
(optional: add your stack or scenario, e.g. "Communication: React server frontend — FastAPI backend — Redis cache — MongoDB database")

[DIAGRAMMING TOOL] - PlantUML | Mermaid | Draw.io | Lucidchart | Creately | Gliffy
```

### Example: sequence diagram for a cached API stack

```text
[DIAGRAM TYPE] - Sequence
[ELEMENT TYPE] - Messages
[PURPOSE] - Communication Frontend React Server - Backend FastAPI - Cache Redis - Database MongoDB
[DIAGRAMMING TOOL] - PlantUML
```

## Public AIPRM link

I published a prompt you can add from the AIPRM library here: [AIPRM prompt (LinkedIn)](https://lnkd.in/gcV25_BY). Use it as a starting point, then narrow `[PURPOSE]` and `[DIAGRAMMING TOOL]` for your team’s stack and deliverables.

## Introduction to sequence diagrams

Sequence diagrams are a type of UML diagram that show how parts of a system exchange **messages** over time. They are useful for onboarding, design reviews, and documenting request paths (especially when a cache or database sits on the critical path).

## Frontend–backend communication with caching

The figure below is a concrete example: a user request flows through a **React** frontend and **FastAPI** backend, with **Redis** as a cache and **MongoDB** as the system of record. The source listings that follow include both a **cache hit** and a **cache miss** branch.

![Frontend-Backend Communication with Caching](images/frontend-backend-caching.jpeg)

## PlantUML (cache hit and cache miss)

```plantuml
@startuml
actor User
participant "ReactServer" as RS
participant "FastAPIServer" as API
participant "RedisCache" as R
database "MongoDB" as M

User -> RS: Sends Request
RS -> API: Forwards Request

alt Cache hit
  API -> R: Check Cache
  R --> API: Found Data
  API -> RS: Sends Response from Cache
  RS -> User: Returns Response from Cache
else Cache miss
  API -> R: Get Data from Cache
  R --> API: Data Not Found
  API -> M: Get Data from DB
  M --> API: Returns Data
  API -> R: Save Data in Cache
  R --> API: Data Saved
  API -> RS: Sends Response
  RS -> User: Returns Response
end
@enduml
```

## Mermaid (cache hit and cache miss)

```mermaid
sequenceDiagram
    actor User
    participant ReactServer
    participant FastAPIServer
    participant RedisCache
    participant MongoDB

    User->>ReactServer: Sends Request
    ReactServer->>FastAPIServer: Forwards Request

    alt Cache hit
        FastAPIServer->>RedisCache: Check Cache
        RedisCache-->>FastAPIServer: Found Data
        FastAPIServer->>ReactServer: Sends Response from Cache
        ReactServer->>User: Returns Response from Cache
    else Cache miss
        FastAPIServer->>RedisCache: Get Data from Cache
        RedisCache-->>FastAPIServer: Data Not Found
        FastAPIServer->>MongoDB: Get Data from DB
        MongoDB-->>FastAPIServer: Returns Data
        FastAPIServer->>RedisCache: Save Data in Cache
        RedisCache-->>FastAPIServer: Data Saved
        FastAPIServer->>ReactServer: Sends Response
        ReactServer->>User: Returns Response
    end
```

## Draw.io, Lucidchart, Creately, and Gliffy

These tools are **canvas-first**: the fastest path is often to generate **PlantUML or Mermaid** in ChatGPT, then:

- **Export** from a PlantUML server or CLI to **SVG** or **PNG** and **import** that graphic into your diagram tool as a baseline layer, or
- Ask ChatGPT (using your template) for a **numbered list of lifelines and messages** in order, and recreate them with the tool’s shapes and connectors.

That avoids blank-canvas syndrome while keeping the diagram editable for styling and annotations your team expects.

## Conclusion

Structured prompts make diagramming repeatable: you choose the **diagram type**, the **elements** to emphasize, the **purpose** (and context), and the **tool** so the model’s answer matches how you will ship the artifact. AIPRM simply makes that workflow one click away once the template lives in your library.

---

*Hashtags for sharing:* #ChatGPT #diagram #UML #software #designtools #PlantUML #Mermaid #Drawio #Lucidchart #Creately #Gliffy
