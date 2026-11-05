{{- /* Markdown catalog of a section: one line per page with its HTML and Markdown URLs. */ -}}
{{- $fr := eq .Lang "fr" -}}
# {{ .Title | plainify }}

{{ with .Description }}> {{ . | plainify }}{{ end }}

- {{ if $fr }}Page HTML{{ else }}HTML page{{ end }}: {{ .Permalink }}
- {{ if $fr }}Langue{{ else }}Language{{ end }}: {{ .Lang }}
{{- range .Translations }}
- {{ if $fr }}Traduction{{ else }}Translation{{ end }} ({{ .Lang }}): {{ .Permalink }}index.md
{{- end }}

{{ if $fr }}Chaque entrée renvoie à la page HTML et à sa vue Markdown (`index.md` ajouté à l’URL).{{ else }}Each entry links the HTML page and its Markdown view (append `index.md` to the URL).{{ end }}

{{ range .RegularPages.ByDate.Reverse }}- [{{ .Title | plainify }}]({{ .Permalink }}) — [{{ if $fr }}Markdown{{ else }}Markdown{{ end }}]({{ .Permalink }}index.md){{ with .Date }} · {{ .Format "2006-01-02" }}{{ end }}{{ with .Description }}
  {{ . | plainify }}{{ end }}
{{ end }}
