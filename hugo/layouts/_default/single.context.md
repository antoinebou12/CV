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
{{- if .Params.repository_note }}
{{ partial "context/project-brief.md" . }}
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
