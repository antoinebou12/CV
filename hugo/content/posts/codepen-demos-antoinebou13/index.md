---
post_kind: article
title: "CodePen demos (collection)"
date: 2017-01-10T10:00:00-04:00
lastmod: 2026-05-22T23:15:00-04:00
description: Live CodePen embeds from the mid-2010s front-end era—forms, jQuery widgets, getDisplayMedia, Canvas blackboard, and a Three.js wave—in one bookmark.
translationKey: codepen-demos-antoinebou13
aliases:
  - /posts/codepen-blackboard-canvas-tutorial/
  - /fr/posts/codepen-blackboard-canvas-tutorial/
  - /posts/codepen-threejs-wave-tutorial/
  - /fr/posts/codepen-threejs-wave-tutorial/
  - /posts/tutorial-jquery-step-progress-bar/
  - /fr/posts/tutorial-jquery-step-progress-bar/
  - /posts/tutorial-webrtc-screen-capture/
  - /fr/posts/tutorial-webrtc-screen-capture/
  - /posts/tutorial-custom-countdown-timer/
  - /fr/posts/tutorial-custom-countdown-timer/
  - /posts/tutorial-date-range-picker-component/
  - /fr/posts/tutorial-date-range-picker-component/
  - /posts/tutorial-jquery-messenger-image-bubbles/
  - /fr/posts/tutorial-jquery-messenger-image-bubbles/
tags:
  - CodePen
  - Frontend
  - JavaScript
  - CSS
  - Canvas
  - Three.js
  - WebGL
  - jQuery
  - HTML
  - WebRTC
images:
  - featured.png
---

CodePen was my **public lab notebook** before this Hugo blog existed — instant preview, comments, and forks without deploying. These are **live CodePen embeds** I kept from the jQuery-and-vanilla-JS years (~2016–2017): small UI labs, then two bigger demos (Canvas and Three.js). Each card uses the **pen title from CodePen** so you know what you are opening—not just the slug in the URL. Fork anything directly on CodePen if you want to adapt it. **[Version française]({{< ref "/posts/codepen-demos-antoinebou13/index.fr.md" >}})**.

<!--more-->

## UI and form experiments

{{< codepen_grid >}}
{{< codepen_card user="antoinebou13" slug="BMdzwx" height="400" title="Sign-up form (Log in Page Style)" caption="Bootstrap-style signup layout: email, password, checkboxes, radio group, select, and textarea—mostly HTML/CSS practice." >}}
{{< codepen_card user="antoinebou13" slug="JxrqQx" height="400" title="Terminal-style console (Simple Console style)" caption="Three faux terminal rows with a blinking cursor; keystrokes from one input mirror into the prompt text." >}}
{{< codepen_card user="antoinebou13" slug="ZEENwWB" height="400" title="Sticky header with jump links" caption="Long placeholder page, black nav bar that sticks after the hero image, and anchor links that scroll to sections." >}}
{{< /codepen_grid >}}

## jQuery-era widgets

{{< codepen_grid >}}
{{< codepen_card user="antoinebou13" slug="byVQKJ" height="400" title="Step progress bar" caption="Four-step horizontal indicator with numbered nodes; jQuery marks completed steps and shortens the first label on narrow viewports (PASSENGER vs PASSENGER DETAILS)." >}}
{{< codepen_card user="antoinebou13" slug="jjzxER" height="400" title="Date range picker (double input)" caption="Custom element daterangepicker-two-input wrapping Moment.js and the Date Range Picker plugin—departure/return fields and night count." >}}
{{< codepen_card user="antoinebou13" slug="xMXNyy" height="400" title="Countdown timer (Bootstrap)" caption="Enter minutes, start with Enter, live min/sec display, reset button, and a short audio clip when the timer hits zero." >}}
{{< /codepen_grid >}}

## Browser APIs

{{< codepen_grid >}}
{{< codepen_card user="antoinebou13" slug="qzQpYg" height="420" title="Screen capture (ScreenShare)" caption="getDisplayMedia demo: start/stop capture, live video preview, red recording border, and a log panel for track settings and errors." >}}
{{< /codepen_grid >}}

## Larger demos

{{< codepen_grid >}}
{{< codepen_card user="antoinebou13" slug="MLEdxr" height="440" title="HTML5 Canvas blackboard (Blackboard Interactive)" caption="Full-screen drawing surface: pen color and size, drag imported images, save PNG, erase all paths and images." >}}
{{< codepen_card user="antoinebou13" slug="rNoqVOj" height="480" title="Three.js wave (3D Animation)" caption="Grid of green cubes animated with a sine-based wave; mouse drag, keyboard, scroll zoom, and optional gamepad camera nudges." >}}
{{< /codepen_grid >}}

## All pens (quick links)

| Pen | CodePen |
|-----|---------|
| Sign-up form | [BMdzwx](https://codepen.io/antoinebou13/pen/BMdzwx) |
| Terminal console | [JxrqQx](https://codepen.io/antoinebou13/pen/JxrqQx) |
| Sticky header + anchors | [ZEENwWB](https://codepen.io/antoinebou13/pen/ZEENwWB) |
| Step progress bar | [byVQKJ](https://codepen.io/antoinebou13/pen/byVQKJ) |
| Date range picker | [jjzxER](https://codepen.io/antoinebou13/pen/jjzxER) |
| Countdown timer | [xMXNyy](https://codepen.io/antoinebou13/pen/xMXNyy) |
| Screen capture | [qzQpYg](https://codepen.io/antoinebou13/pen/qzQpYg) |
| Canvas blackboard | [MLEdxr](https://codepen.io/antoinebou13/pen/MLEdxr) |
| Three.js wave | [rNoqVOj](https://codepen.io/antoinebou13/pen/rNoqVOj) |

## Why I still link these

CodePen was where I learned **feedback loops under 400 lines** — before this Hugo blog existed. The blackboard and Three.js pens are the ones I reopen when someone asks “can you prototype UI fast?” Everything else is historical context for how form-heavy web felt before component frameworks ate the world.

Older long-form write-ups for some of these ideas were merged here; the aliases in the site config still point to this page.

## Related posts

- [Software engineering journey]({{< ref "/posts/software-engineering-journey/index.md" >}}) — from Flash and web demos to platform work
- [Portfolio Hugo week 1]({{< ref "/posts/portfolio-hugo-week-1/index.md" >}}) — where demos became a real site
- [Kinectron + p5.js]({{< ref "/posts/kinectron-p5-sketch-gif/index.md" >}}) — another creative-coding thread
