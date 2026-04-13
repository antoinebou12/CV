---
post_kind: tutorial
title: "Draggable, sortable image bubbles (Messenger-style)"
date: 2016-01-07T10:00:00-04:00
description: Messenger-style circular image tiles with jQuery UI — drag-and-drop and sortable lists, straight out of the jQuery-heavy tutorial blogs of ~2016.
translationKey: tutorial-jquery-messenger-image-bubbles
tags:
    - jQuery
    - jQuery UI
    - CSS
    - Drag and drop
    - Tutorial
    - Frontend
---

### Tutorial: Creating Draggable and Sortable Images with jQuery

#### Introduction
This walkthrough uses jQuery and jQuery UI to build circular “bubble” avatars you can drag and reorder — the same ingredients that showed up in countless demos when Messenger-style circles and sortable lists were everywhere (roughly the ES5 + jQuery era, ~2016). Handy for legacy pages or if you want the recipe in one place.

#### Prerequisites
- Basic knowledge of HTML, CSS, and JavaScript
- jQuery and jQuery UI library

#### HTML Structure
We start by setting up our HTML structure with two unordered lists (`ul`) and list items (`li`) containing images.

```html
<div id="draw">
    <ul id="ul1">
        <li class="li1"><img id="Logo" src="your-image-source-1.jpg"></li>
        <li class="li1"><img id="Logo2" src="your-image-source-2.jpg"></li>
    </ul>
    <ul id="ul2">
        <li class="li2"><img id="Logo3" src="your-image-source-3.jpg"></li>
        <li class="li2"><img id="Logo4" src="your-image-source-4.jpg"></li>
    </ul>
</div>
```

#### CSS Styling
Next, we style the unordered lists and images. We remove the default list styling and set some basic styles for the images.

```css
ul, li {
  list-style: none;
}

img {
  border-radius: 50%;
  border: 0.5px solid #888;
  width: 60px;
  height: 60px;
  margin: 0px;
}
```

#### jQuery Function

We create a jQuery function to apply the rounded shape and make images either draggable or default based on the option passed.

```javascript
(function($) {
    $.fn.roundShape = function(option) {
        if (option === "default") {
            this.css({
                "border-radius": "50%",
                "border": "0.5px solid #888",
                "width": "60px",
                "height": "60px",
                "margin": "0px"
            });
        };
        if (option === "draggable") {
            this.css({
                "border-radius": "50%",
                "border": "0.5px solid #888",
                "width": "60px",
                "height": "60px",
                "margin": "0px"
            }).draggable({ scroll: true, scrollSensitivity: 100 });
        }
    };
}(jQuery));
```

#### Applying the Function
Finally, we apply the jQuery function to our images and enable sorting and dragging functionalities.

```javascript
$(document).ready(function() {
    $('#ul1').sortable({
        revert: true
    });

    $('#Logo, #Logo2').roundShape("default");
    $('#Logo3, #Logo4').roundShape("draggable");
    $('#draw').draggable({ axis: "x" });

    $("#ul1, .li1, .li2").disableSelection();
});
```

Following these steps gives you draggable, sortable circular images on a page — jQuery UI all the way, but it still behaves the same in any browser where you include the libraries.
