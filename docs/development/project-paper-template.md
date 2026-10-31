# Numbered project documentation

All project-note pages use the same numbered contents and references pattern as
articles. The inventory contains 51 projects in two languages (102 pages).

`project-paper.html` numbers the rendered second- and third-level headings, so
sections created by repository shortcodes and partials are included. It builds the
contents from those headings rather than maintaining an independent section list.
Existing section IDs remain available; headings without IDs receive deterministic
IDs. Dynamic workflow step titles are left under the stepper's control.

Desktop contents stay within the viewport and scroll for long dossiers. Mobile
contents retain the native disclosure control. Smaller Markdown-only project notes
receive a contents disclosure after the title.

`article_sources.py` also writes `hugo/data/project_sources.json`. Entries cover
repositories, README links, inspected source files and related project articles.
Repository owners come from their URLs. Article dates come from front matter;
unverified source publication dates remain `n.d.` / `s. d.`. Existing source links
retain their pinned revisions when available.

`project-paper.spec.ts` visits every translation in mobile/light and desktop/dark
layouts. It checks sequential headings, matching contents entries, anchor targets,
reference counts and page overflow. Focused screenshots cover numbered contents
and reference entries; the existing viewer tests cover disclosure behavior and zoom.

The contents use a fixed number column and a wrapping, left-aligned label column.
Desktop shows one heading; mobile keeps the disclosure heading. Counts displayed
beside section titles are omitted from contents labels. `project-polish.spec.ts`
checks sidebar width, label alignment and badge styling at 390, 768 and 1440 pixels
in both themes, with screenshots of CV and ChitUI.
