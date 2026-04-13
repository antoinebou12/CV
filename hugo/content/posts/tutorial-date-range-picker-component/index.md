---
post_kind: tutorial
title: "Date range picker web component (jQuery + plugin)"
date: 2016-02-05T10:00:00-04:00
description: Custom `<daterangepicker-two-input>` element with jQuery, Moment.js, and the Date Range Picker plugin — the kind of range UI that dominated Bootstrap-era admin screens around 2016.
translationKey: tutorial-date-range-picker-component
tags:
    - JavaScript
    - jQuery
    - Date Picker
    - Tutorial
    - Frontend
---

This walkthrough is from the jQuery-and-Moment era: you wrap two text inputs in a custom element `<daterangepicker-two-input>`, register it with `customElements.define`, and hand the container off to the Date Range Picker plugin. Newer stacks usually reach for native `<input type="date">`, flatpickr, or framework date components — but plenty of dashboards shipped in the mid-2010s (and many still in maintenance) look exactly like this.

### Tutorial: Creating a Custom Date Range Picker Element

#### Introduction
You end up with a small reusable tag that opens the familiar range calendar UI (check-in / check-out style) while keeping the markup consistent across pages.

#### Prerequisites
- Basic knowledge of HTML, CSS, and JavaScript
- jQuery and jQuery UI libraries
- Date Range Picker plugin

#### Step 1: Setup Basic HTML
First, include the necessary libraries in your HTML file's head section:
```html
<head>
  <!-- jQuery and jQuery UI -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>

  <!-- Date Range Picker plugin -->
  <script src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" />
</head>
```

#### Step 2: Define Custom Element Structure
Create the custom element class in JavaScript:
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
    // Initialization code for the Date Range Picker
  }
}

window.customElements.define('daterangepicker-two-input', DaterangepickerDoubleInput);
```

#### Step 3: Initialize Date Range Picker
In the `initDateRangePicker` method, initialize the date range picker:
```javascript
initDateRangePicker() {
  $('#combine-input-container').daterangepicker({
    // Date Range Picker options here
  });

  // Event handlers for apply and cancel actions
}
```

#### Step 4: Style the Custom Element
Use CSS to style your custom element:
```css
.combine-input-container {
  /* Your styles here */
}

.c-input-container {
  /* Styles for input containers */
}

.c-label {
  /* Styles for labels */
}

.c-input {
  /* Styles for input fields */
}
```

#### Step 5: Add Custom Element to HTML
Use your custom element in the HTML body:
```html
<body>
  <daterangepicker-two-input></daterangepicker-two-input>
</body>
```

#### Step 6: Test and Debug
Test your custom element in various browsers to ensure compatibility and fix any bugs that arise.

#### Conclusion
That’s the skeleton: one custom element, the plugin bound to the inner container, and CSS however your product needs it.

#### Further Enhancements
- Expose picker options as attributes or properties on the element.
- Tighten validation and locale-specific formats (Moment still handled most of that in this stack).
- Match whatever design system the rest of the app used in 2019–2021.

If you’re maintaining something built this way, the moving parts are still the same: jQuery for DOM/plugin glue, Moment for parsing (the plugin depended on it for years), and the range picker for the actual UI.