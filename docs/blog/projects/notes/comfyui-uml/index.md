# ComfyUI-UML: Diagram rendering inside a node graph

> ComfyUI-UML adds diagram-oriented nodes to ComfyUI. Text enters a workflow, a rendering backend turns it into an image, and the workflow can retain the…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/comfyui-uml/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/comfyui-uml/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/ComfyUI-UML
- Inspected revision: 1f1411580e0db67efd7a4ad669e42ba8677f546a

## Summary

ComfyUI-UML adds diagram-oriented nodes to ComfyUI. Text enters a workflow, a rendering backend turns it into an image, and the workflow can retain the source and viewer links alongside that output.

**Why it exists:** Custom node implementation for ComfyUI node graphs integrating automated UML synthesis into image pipelines.

**Best fit:** Visual AI workflows combining diagram generation with image refinement.

## Use cases

ComfyUI custom nodes that render Mermaid, PlantUML, Graphviz and other Kroki diagrams, optionally from LLM code.

- **Render a diagram from code** (ComfyUI user, Kroki API): The UML Render node (nodes/uml_diagram.py) sends code to Kroki through nodes/kroki_client.py and returns png, svg, jpeg, pdf, txt or base64, checked against each type’s supported formats.
- **Render Mermaid offline** (ComfyUI user): With backend set to local, web/js/render_mermaid.mjs uses beautiful-mermaid (after npm ci in web/js) to make SVG or PNG; Graphviz renders locally when the graphviz package is installed.
- **Generate code with an LLM** (ComfyUI user, LLM provider): UML Code Assistant (nodes/uml_llm.py), or LLM Prompt Engine followed by LLM Call, fills a template from prompts/ and calls Ollama, OpenAI, Anthropic or Gemini; the result feeds UML Render.
- **Preview and share a link** (ComfyUI user, Kroki API): Diagram Viewer URL (nodes/uml_viewer_url.py) turns kroki_url into a viewer link and an iframe link (viewer.html?embed=1) and shows a live preview in the node.
- **Save a diagram to ComfyUI** (ComfyUI user): The viewer’s Save button posts to /comfyui-uml/save, registered with the other routes in nodes/uml_routes.py.

### Scenario: Draw a sequence diagram from a prompt with a local Ollama model

1. Run comfy node install comfyui-uml (or clone into ComfyUI/custom_nodes and pip install -r requirements.txt), then restart ComfyUI.
2. Load workflows/uml_llm_ollama.json in the ComfyUI canvas.
3. Describe the diagram in UML Code Assistant, with provider ollama and a local model.
4. Queue the prompt; UML Render sends the generated code to Kroki and outputs the image.
5. Open the link from Diagram Viewer URL to zoom, copy the link or save the diagram to ComfyUI.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 50.91 |
| JavaScript | 45.75 |
| HTML | 3.34 |

## Getting started (repository commands, not run here)

### README.md · Installation

```bash
comfy node install comfyui-uml
```


## Features and components

- **Plugin registration** — The root __init__.py loads the nodes package under the unique name comfyui_uml_nodes. This avoids colliding with ComfyUI’s own nodes module. It exports the class mappings and the web directory used by the extension.
- **Rendering and viewer** — The nodes directory separates diagram generation, Kroki communication and viewer URLs. Browser assets are exposed through WEB_DIRECTORY, while route registration adds the viewer’s save-to-output integration. Local rendering options and Kroki are distinct backends.

## Architecture

Components and connections verified in the repository.

- Diagram text → Registered ComfyUI node
- Registered ComfyUI node → Local renderer
- Registered ComfyUI node → Kroki service
- Local renderer → Image and viewer links
- Kroki service → Image and viewer links

```mermaid
flowchart LR
  n0["Diagram text"]
  n1["Registered ComfyUI node"]
  n2["Local renderer"]
  n3["Kroki service"]
  n4["Image and viewer links"]
  n0 --> n1
  n1 --> n2
  n1 --> n3
  n2 --> n4
  n3 --> n4
```

**One path through the code:** Start at NODE_CLASS_MAPPINGS, then follow a diagram node into its renderer. The loader uses an explicit module specification because ComfyUI may import the plugin directly from a file path.

## Constraints and checks

Kroki rendering sends diagram text to the configured service. Use a suitable private endpoint for confidential diagrams and check which local renderer dependencies are installed.

## Files to read

- [__init__.py](https://github.com/antoinebou12/ComfyUI-UML/blob/main/__init__.py)
- [nodes/uml_diagram.py](https://github.com/antoinebou12/ComfyUI-UML/blob/main/nodes/uml_diagram.py)
- [nodes/kroki_client.py](https://github.com/antoinebou12/ComfyUI-UML/blob/main/nodes/kroki_client.py)


