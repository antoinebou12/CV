---
post_kind: tutorial
title: "Composant web de sélection de plage de dates (jQuery + plugin)"
date: 2016-02-05T10:00:00-04:00
description: Élément personnalisé `<daterangepicker-two-input>` avec jQuery, Moment.js et le plugin Date Range Picker — le genre d’UI de plage omniprésent dans les admins Bootstrap vers 2016.
translationKey: tutorial-date-range-picker-component
tags:
    - JavaScript
    - jQuery
    - Date picker
    - Web components
    - Tutorial
    - Frontend
---

Ce tutoriel date de l’ère **jQuery + Moment** : on enveloppe deux champs texte dans un élément `<daterangepicker-two-input>`, on l’enregistre avec `customElements.define`, et on confie le conteneur au plugin **Date Range Picker**. Les stacks récentes préfèrent souvent `<input type="date">`, flatpickr ou des composants de date du framework — mais beaucoup de tableaux de bord des années 2010 (et en maintenance) ressemblent encore à ça.

### Tutoriel : créer un élément personnalisé de plage de dates

#### Introduction
Vous obtenez une petite balise réutilisable qui ouvre le calendrier de plage familier (style arrivée / départ) avec un balisage homogène entre pages.

#### Prérequis
- Bases HTML, CSS et JavaScript
- jQuery et jQuery UI
- Plugin Date Range Picker

#### Étape 1 : HTML de base — librairies
```html
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>

  <script src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" />
</head>
```

#### Étape 2 : classe de l’élément personnalisé
```javascript
class DaterangepickerDoubleInput extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = `
    <div class="combine-input-container" id="combine-input-container">
      <div class="c-input-container c1-container">
        <input type='text' class="c-input c1-input" id="c1">
        <label alt='Departure' class="c-label c1-label"></label>
      </div>
      <div class="c-input-container c2-container">
        <input type='text' class="c-input c2-input" id="c2">
        <label alt='Return' class="c-label c2-label"></label>
      </div>
    </div>`;
    this.initDateRangePicker();
  }

  initDateRangePicker() {
    // Initialisation du Date Range Picker
  }
}

window.customElements.define('daterangepicker-two-input', DaterangepickerDoubleInput);
```

#### Étape 3 : initialiser le plugin
```javascript
initDateRangePicker() {
  $('#combine-input-container').daterangepicker({
    // options
  });

  // gestionnaires apply / cancel
}
```

#### Étape 4 : CSS
```css
.combine-input-container { /* … */ }
.c-input-container { /* … */ }
.c-label { /* … */ }
.c-input { /* … */ }
```

#### Étape 5 : utiliser l’élément
```html
<body>
  <daterangepicker-two-input></daterangepicker-two-input>
</body>
```

#### Étape 6 : tests
Tester sur plusieurs navigateurs.

#### Conclusion
Squelette : un élément personnalisé, le plugin sur le conteneur interne, CSS selon le produit.

#### Pistes d’amélioration
- Exposer les options du picker en attributs ou propriétés.
- Renforcer validation et formats locaux (Moment gérait souvent ça).
- Aligner le design sur le reste de l’app.

En maintenance, les pièces restent les mêmes : jQuery pour coller le DOM au plugin, Moment pour l’analyse (longtemps une dépendance du plugin), et le range picker pour l’UI.
