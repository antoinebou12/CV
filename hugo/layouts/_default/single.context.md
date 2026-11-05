{{- /* Markdown context view of one page: front matter facts, then either the project note
       data (source-backed) or the article body. Published at <page-url>index.md. */ -}}
{{- $fr := eq .Lang "fr" -}}
{{- $i := cond $fr 1 0 -}}
# {{ .Title | plainify }}

{{ with .Description }}> {{ . | plainify }}{{ end }}

- {{ if $fr }}Page HTML{{ else }}HTML page{{ end }}: {{ .Permalink }}
- {{ if $fr }}Langue{{ else }}Language{{ end }}: {{ .Lang }}
{{- range .Translations }}
- {{ if $fr }}Traduction{{ else }}Translation{{ end }} ({{ .Lang }}): {{ .Permalink }}index.md
{{- end }}
{{- with .Date }}
- {{ if $fr }}Publié{{ else }}Published{{ end }}: {{ .Format "2006-01-02" }}
{{- end }}
{{- with .Lastmod }}
- {{ if $fr }}Mis à jour{{ else }}Updated{{ end }}: {{ .Format "2006-01-02" }}
{{- end }}
{{- with .GetTerms "tags" }}
- Tags: {{ range $k, $t := . }}{{ if $k }}, {{ end }}{{ $t.Title }}{{ end }}
{{- end }}
- {{ if $fr }}Auteur{{ else }}Author{{ end }}: {{ site.Params.name | default site.Title }} (https://antoineboucher.info/CV/index-en.html)
{{- with .Params.repository_note }}
{{- $repo := . }}
{{- $note := index (where (hugo.Data.repository_notes.notes | default slice) "repo" $repo) 0 }}
{{- $analysis := index (hugo.Data.repository_analysis.repositories | default dict) $repo | default dict }}
{{- $profile := index (hugo.Data.repository_profiles.repositories | default dict) $repo | default dict }}
{{- $guide := index (hugo.Data.repository_handbooks.repositories | default dict) $repo | default dict }}
{{- $cat := index (hugo.Data.repository_categories.repositories | default dict) $repo | default dict }}
{{- $api := index (hugo.Data.repository_api_guides.repositories | default dict) $repo }}
{{- $url := printf "https://github.com/%s/%s" (site.Params.github | default "antoinebou12") $repo }}
{{- with $note }}{{ with .url }}{{ $url = . }}{{ end }}{{ end }}
- {{ if $fr }}Dépôt{{ else }}Repository{{ end }}: {{ $url }}
{{- with $guide.license }}
- {{ if $fr }}Licence{{ else }}License{{ end }}: {{ . }}
{{- end }}
{{- with $analysis.commit }}
- {{ if $fr }}Révision inspectée{{ else }}Inspected revision{{ end }}: {{ . }}
{{- end }}

{{ with $note }}## {{ if $fr }}Résumé{{ else }}Summary{{ end }}

{{ index .intro $i }}
{{ end }}
{{- with $cat }}
{{ with .why_good }}**{{ if $fr }}Pourquoi il existe{{ else }}Why it exists{{ end }}:** {{ index . $i }}{{ end }}

{{ with .use_case }}**{{ if $fr }}Cas d’usage{{ else }}Best fit{{ end }}:** {{ index . $i }}{{ end }}
{{ end }}
{{- with $analysis.languages }}
## {{ if $fr }}Langages (octets GitHub Linguist){{ else }}Languages (GitHub Linguist bytes){{ end }}

| {{ if $fr }}Langage{{ else }}Language{{ end }} | % |
| --- | ---: |
{{ range . }}| {{ .name }} | {{ .percent }} |
{{ end }}{{ end }}
{{- with $profile.badges }}
## {{ if $fr }}Technologies vérifiées{{ else }}Verified technologies{{ end }}

{{ range . }}- {{ .label }}{{ with .title }} — {{ . }}{{ end }}
{{ end }}{{ end }}
{{- with $analysis.installation }}
## {{ if $fr }}Démarrage (commandes du dépôt, non exécutées ici){{ else }}Getting started (repository commands, not run here){{ end }}

{{ range . }}### {{ .file }} · {{ .heading }}

```bash
{{ .commands }}
```

{{ end }}{{ end }}
{{- with $profile.docker_commands }}
### Docker

```bash
{{ if reflect.IsSlice . }}{{ range . }}{{ . }}
{{ end }}{{ else }}{{ . }}
{{ end }}```
{{ end }}
{{- with $note }}
## {{ if $fr }}Fonctions et composants{{ else }}Features and components{{ end }}

{{ range .parts }}- **{{ index . $i }}** — {{ index . (add $i 2) }}
{{ end }}
## Architecture

{{ if $fr }}Composants et connexions vérifiés dans le dépôt.{{ else }}Components and connections verified in the repository.{{ end }}

{{ range .edges }}- {{ index (index $note.nodes (int (index . 0))) $i }} → {{ index (index $note.nodes (int (index . 1))) $i }}
{{ end }}
```mermaid
flowchart LR
{{ range $index, $label := .nodes }}  n{{ $index }}["{{ replace (index $label $i) "\"" "'" }}"]
{{ end }}{{ range .edges }}  n{{ index . 0 }} --> n{{ index . 1 }}
{{ end }}```

**{{ if $fr }}Un parcours dans le code{{ else }}One path through the code{{ end }}:** {{ index .trace $i }}
{{ end }}
{{- with $profile.workflow }}
## {{ if $fr }}Parcours{{ else }}Workflow{{ end }}

{{ range $n, $step := . }}{{ add $n 1 }}. **{{ index $step.title $i }}** — {{ index $step.body $i }}
{{ end }}{{ end }}
{{- with $profile.services }}
## {{ if $fr }}Services Compose{{ else }}Compose services{{ end }}

| {{ if $fr }}Service{{ else }}Service{{ end }} | Runtime | Ports | {{ if $fr }}Dépend de{{ else }}Depends on{{ end }} |
| --- | --- | --- | --- |
{{ range . }}| {{ .name }} | {{ .runtime }} | {{ .ports }} | {{ .depends }} |
{{ end }}{{ end }}
{{- with $api }}
## API

{{ with .summary }}{{ index . $i }}{{ end }}
{{ range .endpoints }}- `{{ .method }} {{ .path }}`{{ with .summary }} — {{ index . $i }}{{ end }}
{{ end }}{{ end }}
{{- with $note }}
## {{ if $fr }}Limites et points à vérifier{{ else }}Constraints and checks{{ end }}

{{ index .limits $i }}

## {{ if $fr }}Fichiers à lire{{ else }}Files to read{{ end }}

{{ range .sources }}- [{{ .path }}]({{ .url }})
{{ end }}{{ end }}
{{- else }}
{{- /* Article body: resolve ref/relref shortcodes to URLs, turn figures into images, drop other shortcodes. */ -}}
{{- $raw := .RawContent -}}
{{- range findRE `\{\{<\s*(?:rel)?ref\s+"[^"]+"\s*>\}\}` $raw -}}
  {{- $target := replaceRE `\{\{<\s*(?:rel)?ref\s+"([^"]+)"\s*>\}\}` "$1" . -}}
  {{- $url := "" -}}
  {{- with $.GetPage $target }}{{ $url = .Permalink }}{{ else }}{{ with site.GetPage $target }}{{ $url = .Permalink }}{{ end }}{{ end -}}
  {{- $raw = replace $raw . $url -}}
{{- end -}}
{{- $raw = replaceRE `\{\{<\s*figure\s+[^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"[^>]*>\}\}` (printf "![$2](%s$1)" .Permalink) $raw -}}
{{- $raw = replaceRE `\{\{<\s*figure\s+[^>]*?src="([^"]+)"[^>]*>\}\}` (printf "![]($1)" ) $raw -}}
{{- $raw = replaceRE `(?s)\{\{<[^>]*?>\}\}` "" $raw -}}
{{- $raw = replaceRE `(?s)\{\{%[^%]*?%\}\}` "" $raw -}}
{{- $raw = replace $raw "<!--more-->" "" -}}
{{- $raw = replaceRE `\n{3,}` "\n\n" $raw -}}

{{ $raw | strings.TrimSpace }}
{{- end }}
