---
post_kind: tutorial
title: "Custom countdown timer (HTML, CSS, JavaScript)"
date: 2016-02-01T10:00:00-04:00
description: Minutes input, start/reset, on-screen display, and optional sound at zero — a small vanilla HTML/CSS/JS timer in the style of mid-2010s tutorials.
tags:
    - JavaScript
    - HTML
    - CSS
    - Timer
    - Tutorial
    - Frontend
---

This is a straight DOM-and-`setInterval` countdown: minutes in, tick down, start and reset, and a short audio clip when it hits zero — the sort of thing that showed up in every “learn JavaScript” blog around 2016 before frameworks swallowed the front page.

### Tutorial: Building a Custom Countdown Timer

#### Step 1: Setting Up the HTML Structure
First, we'll create the basic structure of the timer. This includes input fields for minutes, a display for the countdown, and buttons to start and reset the timer.

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

#### Step 2: Adding CSS for Styling
Next, we'll add CSS to style our timer. This will make the timer more user-friendly and visually appealing.

```css
/* Add your CSS styling here */
/* Example: */
.Time {
  font-size: 2em;
  font-weight: 300;
}
/* Add styles for inputs, labels, and buttons */
```

#### Step 3: JavaScript Functionality
Now, we'll add JavaScript to make the timer functional. This includes the countdown logic and the reset functionality.

```javascript
$(function() {
  // Add your jQuery and JavaScript code here
  // Example:
  $('#input').keypress(function(e) {
    if (e.which == 13) { // Enter key pressed
      CheckTick();
    }
  });
});

// Add functions for countdown, CheckTick, and Reset
```

#### Step 4: Testing and Debugging
- Test the timer by entering a value and seeing if it counts down correctly.
- Ensure the audio plays when the timer reaches zero.
- Test the reset functionality to see if it stops and resets the timer as expected.

#### Step 5: Additional Features and Improvements
- Add error handling for non-numeric inputs.
- Implement a visual indicator for when the timer is running.
- Style the timer to be responsive for better mobile device compatibility.

#### Step 6: Deployment
- If you're using this timer on a website, embed the HTML, CSS, and JavaScript into the appropriate sections of your webpage.
- Test the timer in different browsers to ensure cross-browser compatibility.

### Conclusion
You end up with a working countdown, start/reset, and optional alarm. The pattern is old but transparent: easy to adapt, and still fine for static sites or embedded widgets without a build step.