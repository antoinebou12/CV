---
post_kind: article
title: "Créer un CV professionnel avec JSON Resume"
date: 2022-09-10T10:00:00-04:00
description: Utiliser le schéma JSON Resume et l’outil npm pour publier en HTML, PDF ou intégrer les données du CV.
translationKey: professional-resume-json-resume
tags:
    - JSON Resume
    - npm
    - Career
    - HTML
    - PDF
---

## Introduction

Avoir un CV en ligne compte. Une approche efficace consiste à utiliser le paquet npm **JSON Resume** : rédiger le CV en JSON, puis l’exporter en **HTML**, **PDF** ou l’intégrer à un site personnel.

## Format JSON Resume

JSON Resume est une initiative open source communautaire pour un standard CV en JSON. Le format est léger et facile à manipuler, ce qui permet de construire des outils autour.

Sections typiques :

### Section basics

Nom, intitulé, contact, court résumé, localisation, profils pro.

```json
"basics": {
  "name": "Your Name",
  "label": "Job Title",
  "email": "your.email@example.com",
  "website": "https://yourwebsite.com",
  "summary": "A brief summary about yourself.",
  "location": {
    "city": "City",
    "region": "Region",
    "countryCode": "Country Code"
  },
  "profiles": [
    {
      "network": "LinkedIn",
      "username": "yourusername",
      "url": "https://www.linkedin.com/in/yourusername/"
    }
  ]
}
```

### Expérience professionnelle

```json
"work": [
  {
    "name": "Company Name",
    "position": "Your Position",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD",
    "summary": "Description of your role."
  }
]
```

### Formation

```json
"education": [
  {
    "institution": "University Name",
    "area": "Field of Study",
    "studyType": "Degree Type",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD"
  }
]
```

### Compétences

```json
"skills": [
  {
    "name": "Programming",
    "level": "Intermediate",
    "keywords": ["Python", "JavaScript"]
  }
]
```

### Projets

```json
"projects": [
  {
    "name": "Project Name",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD",
    "description": "Project description.",
    "url": "https://projecturl.com"
  }
]
```

## Paquet npm

1. **Installer resume-cli globalement** :
   ```
   npm install -g resume-cli
   ```

2. **Créer resume.json** selon le schéma JSON Resume.

3. **Exporter** :
   ```
   resume export resume.html
   resume export resume.pdf
   ```

4. **Hébergement** : le registre JSON Resume permet d’héberger gratuitement.

JSON Resume offre un moyen standardisé et souple de créer et partager un profil pro. Avec le schéma et la CLI, vous obtenez un CV moderne à partager avec employeurs et contacts.

## Ressources avec Hugo et JSON Resume

### Profile Studio

Outil en ligne pour prévisualiser et personnaliser le JSON Resume en temps réel.

- [Profile Studio Preview](https://profile-studio.netlify.app/#/preview)

### SkillSet

Visualisation interactive des compétences (D3.js).

- [SkillSet](https://jac21.github.io/SkillSet/)

### Export LinkedIn vers JSON Resume

- [LinkedIn to JSON Resume Exporter](https://joshuatz.com/projects/web-stuff/linkedin-profile-to-json-resume-exporter/)

### Hugo-Mod-JSON-Resume

Module Hugo pour intégrer JSON Resume, avec données multilingues et modèles par section.

- [Hugo-Mod-JSON-Resume](https://github.com/schnerring/hugo-mod-json-resume)

Ces ressources aident à construire un CV en ligne plus riche et interactif.
