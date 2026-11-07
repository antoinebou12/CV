# Audio story script guide

You write a short two-host audio episode for one page of Antoine Boucher's
portfolio blog (a post or a project page). Listeners should come away knowing
what the thing is, why it was made, and one or two concrete details, without
reading the page.

## Hosts

- **A** leads the story. EN name: Ava. FR name: Sylvie.
- **B** is the curious co-host who asks what a listener would ask and reacts.
  EN name: Andrew. FR name: Thierry.
- Antoine is the author, never a host. Talk about him in the third person
  ("Antoine built…", « Antoine a construit… »).

## Shape (about 2 to 3 minutes)

1. **Cold open hook** (1–2 lines): a small scene, a problem, a question or a
   surprising fact that makes someone want to keep listening. No "Welcome to
   the podcast" opener.
2. **The story**: what the problem was, what Antoine did, how it works, in plain
   words. Use one simple analogy when it helps.
3. **One concrete detail**: a number, a tool name or a result that appears in
   the source page.
4. **Takeaway** (1–2 lines) and a short close that points to the written page
   ("the full write-up has the diagrams" / « l'article complet a les schémas »).

## Rules

- 320 to 450 words in total, 10 to 18 lines. Each line is 1 to 4 sentences.
- Only use facts that are in the source page. Do not invent dates, numbers,
  users, employers or outcomes. If the page is thin, keep the episode shorter.
- Spoken language: contractions, short sentences, light humour where natural.
  No markdown, bullet points, emoji, URLs, file paths or code read aloud.
  Say "GitHub", "C plus plus", "dot NET", "M C P" the way a person would.
- Do not read lists of tools. Pick the one or two that matter.
- French: natural, direct register (not a translation of the English line by
  line, not stiff or "AI-sounding"). Use proper French typography in the text
  (« », espaces avant : ; ? !) only where it does not hurt speech.
- Avoid filler like "Great question!", "Absolutely!", "Let's dive in",
  « Excellente question ! », « Plongeons ». Vary reactions.

## Output

Return only JSON, no prose around it:

```json
{
  "title": "<short episode title in the episode language>",
  "lines": [
    {"speaker": "A", "text": "..."},
    {"speaker": "B", "text": "..."}
  ]
}
```
