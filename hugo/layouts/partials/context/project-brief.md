{{- /* Project brief in Markdown: facts from the repository data files only. Expects a project note page. */ -}}
{{- $fr := eq .Lang "fr" -}}
{{- $i := cond $fr 1 0 -}}
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
{{- range where (hugo.Data.project_org_repositories.repositories | default slice) "name" $repo }}{{ $url = .url }}{{ end }}
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
{{- with index (hugo.Data.project_use_cases.repositories | default dict) $repo }}
## {{ if $fr }}Cas d’utilisation{{ else }}Use cases{{ end }}

{{ index .summary $i }}

{{ $uc := . }}{{ range .use_cases }}- **{{ index .label $i }}** ({{ range $k, $id := .actors }}{{ if $k }}, {{ end }}{{ with index (where $uc.actors "id" $id) 0 }}{{ index .label $i }}{{ end }}{{ end }}){{ with .detail }}: {{ index . $i }}{{ end }}
{{ end }}
{{ with .scenario }}### {{ if $fr }}Scénario : {{ else }}Scenario: {{ end }}{{ index .title $i }}

{{ range $k, $s := .steps }}{{ add $k 1 }}. {{ index $s $i }}
{{ end }}{{ end }}
{{- end }}
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
{{- end }}
