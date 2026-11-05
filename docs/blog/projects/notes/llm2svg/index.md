# LLM2SVG: Dataset analysis before model claims

> This LLM2SVG fork contains SVG dataset utilities and an evaluation-oriented scaffold. The visible implementation is useful for inspecting examples and…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/llm2svg/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/llm2svg/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/LLM2SVG
- Inspected revision: a8337761b49bbdcbac24f58c6adc5f17d1ac2a07

## Summary

This LLM2SVG fork contains SVG dataset utilities and an evaluation-oriented scaffold. The visible implementation is useful for inspecting examples and constraints; it does not establish a completed or trained text-to-SVG model.

**Why it exists:** Structured prompt engineering framework and Python validator generating crisp, valid SVG illustrations from LLM responses.

**Best fit:** Automated vector icon and diagram generation for design systems.

## Use cases

Python utilities and data for a text-to-SVG challenge: load prompts, check SVG rules, build and render shapes.

- **Load prompts and SVG samples** (ML researcher): SVGDataLoader in utils/data_loader.py reads data/train/train.csv and data/test/test.csv and collects the SVG files stored under data/train/svg/<id>/; SVGDataset in utils/svg_dataset.py wraps them as a PyTorch Dataset.
- **Validate SVG constraints** (ML researcher): SVGConstraints.validate_svg in utils/svg_constraints.py rejects files over 10,000 bytes and any element or attribute outside the allowlist, parsing with defusedxml.
- **Extract terms from a prompt** (ML researcher): TextParser in utils/text_parser.py pulls colours, shapes, patterns, materials, clothing, landscape and architecture terms from a description and picks a primary category.
- **Build SVG from primitives** (ML researcher): utils/svg_utils.py has helpers for rect, circle, ellipse, path, polygon, line and group elements, a colour palette generator, generate_shapes and optimize_svg to shorten numbers.
- **Render SVG to PNG** (ML researcher, cairosvg renderer): svg_to_png in utils/svg_utils.py calls cairosvg.svg2png and either writes a file or returns PNG bytes.
- **Report on the SVG dataset** (ML researcher): SVGAnalyzer in utils/svg_analyzer.py counts SVGs, measures their sizes, tallies elements, validates every file and plots a size histogram against the 10 KB limit.

### Scenario: Check a set of candidate SVGs before submission

1. Point SVGDataLoader at the local data/ folder (the default path is hard-coded to the author’s Windows drive).
2. Read the prompts from data/train/train.csv, for example "a starlit night over snow-covered peaks".
3. Run SVGAnalyzer.validate_all_svgs("train") to test every SVG under data/train/svg/ with SVGConstraints.
4. Call generate_summary_report to get a table of sizes and inferred sources, then plot_svg_size_distribution.
5. Render a passing SVG with svg_to_png to compare it with the prompt.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 100 |

## Getting started (repository commands, not run here)

### README.md · Dependencies

```bash
pip install cairosvg torch torchvision
```


## Features and components

- **Loading and constraints** — SVGAnalyzer composes SVGDataLoader and SVGConstraints. It enumerates samples, records file sizes and checks constraints. Dataset loading and validation are separate responsibilities.
- **Dataset reports** — The analyzer counts element names and builds per-sample validation results, with a summary-report method returning a pandas DataFrame. Element counting uses a regular expression to tolerate malformed SVG text.

## Architecture

Components and connections verified in the repository.

- SVG dataset files → SVGDataLoader
- SVGDataLoader → Element and size analysis
- SVGDataLoader → Constraint checks
- Element and size analysis → Dataset report
- Constraint checks → Dataset report

```mermaid
flowchart LR
  n0["SVG dataset files"]
  n1["SVGDataLoader"]
  n2["Element and size analysis"]
  n3["Constraint checks"]
  n4["Dataset report"]
  n0 --> n1
  n1 --> n2
  n1 --> n3
  n2 --> n4
  n3 --> n4
```

**One path through the code:** Follow validate_all_svgs and compare it with analyze_elements. Passing the declared constraints and having a plausible set of element names are different checks; neither establishes visual similarity to a text prompt.

## Constraints and checks

The analyzer has a machine-specific default data path. Model quality, training results and evaluation scores should not be inferred from these utility files.

## Files to read

- [utils/svg_analyzer.py](https://github.com/antoinebou12/LLM2SVG/blob/main/utils/svg_analyzer.py)
- [utils/data_loader.py](https://github.com/antoinebou12/LLM2SVG/blob/main/utils/data_loader.py)
- [utils/svg_constraints.py](https://github.com/antoinebou12/LLM2SVG/blob/main/utils/svg_constraints.py)


