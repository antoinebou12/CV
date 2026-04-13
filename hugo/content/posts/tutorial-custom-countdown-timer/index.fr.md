---
post_kind: tutorial
title: "Minuteur décompte personnalisé (HTML, CSS, JavaScript)"
date: 2016-02-01T10:00:00-04:00
description: Saisie en minutes, démarrage/réinitialisation, affichage à l’écran et son optionnel à zéro — petit minuteur vanilla HTML/CSS/JS façon tutoriels du milieu des années 2010.
translationKey: tutorial-custom-countdown-timer
tags:
    - JavaScript
    - HTML
    - CSS
    - Timer
    - Tutorial
    - Frontend
---

Un décompte classique DOM + `setInterval` : saisie en minutes, tick, démarrage et reset, et un court fichier audio à l’arrivée à zéro — le genre d’exemple qu’on trouvait partout dans les blogs « apprendre JavaScript » vers 2016, avant que les frameworks ne dominent la une.

### Tutoriel : construire un minuteur décompte

#### Étape 1 : structure HTML
On pose la base : champ pour les minutes, affichage du décompte, boutons démarrer et réinitialiser.

```html
<div class="Time-option">
  <div class="input-group">
    <input id="input" autocomplete="off" type="text"/>
    <label>minutes</label>
    <button onclick="Reset()" class="btn btn-lg button-refresh">
      <span id="refresh" class="glyphicon refresh-animate glyphicon-refresh glyphicon-refresh-animate"/>
    </button>
  </div>
</div>

<div class="Time">
  <span id="minutes">00</span>
  <span class="min">min</span>
  <span id="seconds">00</span>
  <span class="sec">sec</span>
</div>
<audio></audio>
```

#### Étape 2 : CSS
Ajoutez des styles pour rendre le minuteur lisible et agréable visuellement.

```css
/* Ajoutez vos styles ici */
/* Exemple : */
.Time {
  font-size: 2em;
  font-weight: 300;
}
/* Styles pour champs, labels, boutons */
```

#### Étape 3 : JavaScript
Logique de décompte et de réinitialisation.

```javascript
$(function() {
  // jQuery / JS ici
  // Exemple :
  $('#input').keypress(function(e) {
    if (e.which == 13) { // Entrée
      CheckTick();
    }
  });
});

// Fonctions décompte, CheckTick, Reset
```

#### Étape 4 : tests
- Tester la saisie et le décompte.
- Vérifier le son à zéro.
- Vérifier le reset.

#### Étape 5 : améliorations possibles
- Gestion d’erreur pour entrées non numériques.
- Indicateur visuel « en cours ».
- Mise en page responsive.

#### Étape 6 : déploiement
- Intégrer HTML, CSS et JS aux bons endroits du site.
- Tester sur plusieurs navigateurs.

### Conclusion
Vous obtenez un décompte fonctionnel, démarrage/reset et alarme optionnelle. Le modèle est ancien mais limpide : facile à adapter, toujours adapté aux sites statiques ou widgets sans étape de build.
