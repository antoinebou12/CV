# Article reading review

Reviewed the Mitsuba article in English and French at 390, 768 and 1280 pixels,
in light and dark themes, using the existing Playwright installation.

## Pass 1: reading order

Moved project documentation into the article heading, removed its redundant label,
disabled the duplicate Mitsuba hero, and replaced italic caption paragraphs with
figure captions. The mobile introduction now appears within the first 950 pixels.
The contents disclosure appears before the introduction and remains keyboard accessible.

The first test counted a rendered diagram as a duplicate image. Corrected the
assertion to count figures containing images; the two illustrations remain distinct.

## Pass 2: loading and interactions

Mermaid source starts inside a disclosure with a loading label. A failed renderer
import changes the label to unavailable and leaves the source accessible. Successful
rendering replaces the disclosure with the interactive diagram. Added command-copy
controls to article code blocks and verified the rendered captions in screenshots.

## Pass 3: technical scanning

Added bilingual input/processing/output tables and links to the source interface
and material blending implementation. Playwright checks real clipboard contents,
contents disclosure behavior, image count, caption styling, introduction position,
horizontal overflow, and unavailable-renderer recovery. Existing project viewer
checks run alongside the article checks to catch shared-script regressions.

Screenshots are written to `tools/ux-audit/e2e-results/article-loop-*` (ignored build
artifacts). The source test is `tools/ux-audit/e2e/article-reading.spec.ts`.
