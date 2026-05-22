---
post_kind: article
title: "Créer un CV professionnel avec JSON Resume"
date: 2022-09-10T10:00:00-04:00
lastmod: 2026-05-22T22:00:00-04:00
description: Rédiger le CV une fois en JSON, exporter en HTML ou PDF avec des thèmes, ou brancher les données dans un site Hugo.
translationKey: professional-resume-json-resume
tags:
  - JSON Resume
  - npm
  - Career
  - HTML
images:
  - featured.png
---

![JSON Resume — aperçu de thèmes (Elegant, Paper, Kendall, Flat, etc.)](./json-resume-themes.png)

La plupart des parcours passent par le web. **JSON Resume** permet de garder un `resume.json` structuré et de le rendre en HTML, PDF ou données intégrées à votre site. **[English version]({{< ref "/posts/professional-resume-json-resume/index.md" >}})** du même article.

<!--more-->

## Pourquoi du JSON ?

[JSON Resume](https://jsonresume.org/) est un schéma ouvert maintenu par la communauté. Fichier JSON simple : les thèmes et outils CLI changent la présentation sans réécrire le contenu. L’écosystème propose de nombreux styles—la grille ci-dessus montre des thèmes comme **Elegant**, **Paper**, **Kendall** et **Flat**.

Vous mettez à jour les données une fois, régénérez les exports, ou réutilisez le même fichier dans un générateur de site statique.

## Sections principales

Un `resume.json` typique regroupe l’information en blocs prévisibles.

### Basics

Nom, titre, courriel, site, résumé court, localisation, profils (LinkedIn, GitHub, etc.).

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

### Expérience (`work`)

Entreprise, poste, dates, résumé du rôle.

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

### Formation (`education`)

Établissement, domaine, type de diplôme, dates.

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

### Compétences (`skills`)

Groupes avec niveau optionnel et mots-clés.

```json
"skills": [
  {
    "name": "Programming",
    "level": "Intermediate",
    "keywords": ["Python", "JavaScript"]
  }
]
```

### Projets (`projects`)

Portfolio ou projets significatifs avec dates, description et URL.

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

## Ligne de commande

Installation globale :

```bash
npm install -g resume-cli
```

Rédiger `resume.json` selon le [schéma](https://jsonresume.org/schema/), choisir un thème, exporter :

```bash
resume export resume.html
resume export resume.pdf
```

Publication possible sur le [registre JSON Resume](https://registry.jsonresume.org/) pour une page hébergée gratuite.

Même contenu, plusieurs sorties—pratique pour garder PDF et version web alignés.

## Hugo et outils autour

Avec **Hugo**, le module [hugo-mod-json-resume](https://github.com/schnerring/hugo-mod-json-resume) mappe les sections JSON vers des modèles (y compris multilingue)—utile pour intégrer le CV dans un blog personnel.

Autres liens utiles :

- **[Profile Studio](https://profile-studio.netlify.app/#/preview)** — prévisualisation en direct.
- **[SkillSet](https://jac21.github.io/SkillSet/)** — visualisation D3 des compétences.
- **[LinkedIn to JSON Resume](https://github.com/joshuatz/linkedin-to-jsonresume)** — amorcer `resume.json` depuis LinkedIn.

## En bref

JSON Resume, c’est surtout de la discipline : une source de vérité, des thèmes pour la mise en page, puis CLI ou Hugo quand le PDF statique ne suffit plus. Pour un portfolio développeur, séparer **contenu** et **présentation** vieillit bien.
