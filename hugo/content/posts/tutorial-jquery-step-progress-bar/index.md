---
title: "Responsive step progress bar (jQuery + CSS)"
date: 2024-02-12T10:00:00-04:00
description: Multi-step indicator with numbered nodes, connectors, and responsive label text.
tags:
    - jQuery
    - CSS
    - UI
    - Progress
    - Tutorial
    - Frontend
---

This code creates a responsive progress bar with four steps. It uses jQuery for dynamic text changes and CSS for styling. Here's a breakdown of its functionality:

### HTML Structure
- The progress bar is wrapped inside a `div` with the class `progressbar_container`.
- An unordered list (`ul`) with the class `progressbar` represents the progress bar.
- Each step in the progress bar is an `li` element with the class `progressbar_node`.
- The current step is highlighted by adding the class `current_node`.

### CSS Styling
- The `.progressbar_container` is styled to position the progress bar, manage its size, and center it.
- Each `.progressbar_node` represents a step in the progress bar.
- The `:before` pseudo-element of `.progressbar_node` creates circular step indicators with numbers.
- The `:after` pseudo-element creates connecting lines between the steps.
- The current and completed steps are highlighted with a darker color and a solid border.

### JavaScript Functionality
- On document ready (`$(document).ready`), the previous steps to the current step are marked as completed using the class `activated_node`.
- A resize event listener (`$(window).resize`) changes the text of the first step based on the window's width. It toggles between "PASSENGER" and "PASSENGER DETAILS".

### Notes
- Ensure you have included the jQuery library to use the jQuery syntax.
- The resizing functionality helps maintain responsiveness, providing a better experience on different screen sizes.

### Example Usage
To use this progress bar, include the provided HTML in your document. Ensure your CSS is properly linked, and the jQuery library is included for the JavaScript to work correctly.

### Enhancements
- You can modify the number of steps by adjusting the HTML and potentially tweaking the CSS.
- Consider adding ARIA attributes for accessibility, making the progress bar usable for screen readers.
- You could enhance the responsiveness further by using CSS media queries instead of JavaScript for text changes.

This progress bar is a great way to visually represent progress through a multi-step process, such as a checkout or registration flow.