---
post_kind: article
title: "Software lifecycle notes — GOALS, waterfall, and verification vs validation"
date: 2023-04-13T08:00:00-04:00
description: Study scans from a software engineering text — goal-oriented decomposition, classic and incremental waterfall, nine life-cycle subgoals, V&V, a collage of process advice, and an ethics case-study takeaway.
translationKey: software-engineering-textbook-figures
tags:
    - Software Engineering
    - SDLC
    - Waterfall
    - Verification
    - Validation
    - Education
images:
    - goals-approach.png
---

These pages are from a **software engineering** textbook I used in coursework. I grouped the figures here as a single reference: **goal-oriented planning**, how the **waterfall** model sequences activities (with **verification and validation** paired to each phase), an **incremental** variant, the textbook’s list of **life-cycle subgoals**, a reminder that **method advice depends on context**, and a short **ethics** passage about impact on people.

## GOALS approach (Figure 3-1)

The **GOALS** flowchart is a top-down pattern: set **overall life-cycle goals** (functions, constraints, schedule, usability, maintainability), **analyze** the problem and sketch solution structure, **separate concerns** into subgoals, **develop** solutions for each subgoal in parallel where possible, then **validate** those solutions against the other goals and **iterate** until the decision “all goals satisfied?” is yes.

![Flowchart titled The GOALS approach — establish goals, analyze, separate concerns into subgoals, develop solutions, validate and iterate until end](images/goals-approach.png)

It reads like an early articulation of what later methodologies still do: decompose, check consistency across concerns, loop rather than assume a single pass is enough.

## Sorting out software advice (Figure 3-4)

The “**sorting out software advice**” figure is a scatter of practices — top-down vs outside-in, walkthroughs, independent test teams, chief programmer teams, measurable milestones, configuration management, structured programming, “build it twice,” involve the user, and many more. The surrounding text stresses that **the same slogan can be right in one situation and wasteful in another** (for example, building a throwaway first version when the domain is unfamiliar vs when it is already well understood).

![Hand-drawn style word collage of software engineering practices and slogans](images/sorting-software-advice.png)

Useful as a checklist of ideas to consider, not as a single recipe to apply everywhere.

## Ethics: urban school attendance system (Chapter 2 case study)

The italic quote on this page is the line I underlined in the margin: individual engineers can **improve outcomes for society** by paying attention to **long-range human and social implications** of designs, not only to technical correctness.

![Text excerpt on software engineers’ opportunity to consider human relations implications of designs](images/ethics-urban-school-attendance.png)

It pairs naturally with requirements and validation — “the right product” includes who it serves and how it affects them.

## Waterfall life-cycle (Figure 4-1)

The classic **waterfall** diagram shows phases cascading in order. Each box is split diagonally: **development work** in one triangle and the matching **V&V** activity in the other — from **system feasibility** through **requirements**, **product design**, **detailed design**, **code**, **integration**, **implementation**, to **operations and maintenance**. **Backward arrows** express rework when a phase’s review finds problems.

![Waterfall model diagram with eight phases each paired with verification or validation](images/waterfall-lifecycle.png)

Even when a team does not ship “pure waterfall,” the diagram still names the kinds of artifacts and checks that keep showing up under other names.

## Incremental waterfall (Figure 4-4)

The **incremental** variant anchors a shared **product design**, then runs **parallel or staggered increments** through detailed design, coding, integration, and the rest — each increment still carrying the same **build / verify** pairing and **feedback** to earlier steps (including back toward product design).

![Waterfall model extended with multiple increments branching from product design](images/waterfall-incremental.png)

It is a structured way to picture **delivery in slices** without pretending that upstream decisions never change.

## Subgoals, verification, and validation (Chapter 4)

This page lists **nine engineering subgoals** in sequence: **feasibility**, **requirements**, **product design**, **detailed design**, **coding**, **integration**, **implementation**, **maintenance** (repeated per update), and **phaseout**. It then defines **verification** as correspondence to specification — “**Are we building the product right?**” — and **validation** as fitness for the mission — “**Are we building the right product?**” **Configuration management** appears alongside V&V as another cross-cutting obligation. A footnote admits the strict sequence is a **teaching simplification**; **prototyping**, **incremental development**, and overlapping work are called out as common adjustments.

![Text page listing nine software life-cycle subgoals and definitions of verification vs validation](images/lifecycle-subgoals-verification-validation.png)

---

These scans are for my own revision; **figures and wording belong to the original book and publisher**. For related notes on **compilers and grammars** from another text, see the companion post on [compiler pipeline, language genealogy, and parse trees]({{< ref "/posts/compiler-design-textbook-figures/index.md" >}}).
