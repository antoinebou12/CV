---
post_kind: article
title: Creating a professional résumé with JSON Resume
date: 2022-09-10T10:00:00-04:00
description: Use the JSON Resume schema and npm tooling to publish HTML, PDF, or embedded CV data.
tags:
    - JSON Resume
    - npm
    - Career
    - HTML
    - PDF
---

## Introduction

In today's digital world, having an online resume is crucial for showcasing your professional profile. One effective way to create an online resume is by using the JSON Resume npm package. This package allows you to write your resume in JSON and then export it to various formats such as HTML, PDF, or even integrate it into your personal website.

## JSON Resume Format

JSON Resume is a community-driven open-source initiative to create a JSON-based standard for resumes. The format is lightweight and easy to use, making it perfect for building tools around it.

Here's a breakdown of the key sections in a typical JSON Resume:

### The Basics Section

This section contains your basic information like name, job title, contact information, and a brief summary. It also includes your location and links to your professional profiles.

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

### Work Experience

This section details your professional experience. You can include the company name, your position, the period of employment, and a summary of your role and achievements.

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

### Education

List your academic qualifications, the institution, the degree or course, and the period of study.

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

### Skills

Mention your skills along with the proficiency level and relevant keywords.

```json
"skills": [
  {
    "name": "Programming",
    "level": "Intermediate",
    "keywords": ["Python", "JavaScript"]
  }
]
```

### Projects

Highlight significant projects you've worked on, including the project name, duration, a brief description, and a URL if available.

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

## Using the npm Package

1. **Install resume-cli globally**: This command line tool allows you to export your resume in different formats.
   ```
   npm install -g resume-cli
   ```

2. **Create your resume.json**: Follow the JSON Resume schema to create your resume.

3. **Export your resume**: Use the CLI to export your resume to different formats.
   ```
   resume export resume.html
   resume export resume.pdf
   ```

4. **Hosting**: You can host your JSON resume for free using the JSON Resume Registry.

The JSON Resume npm package provides a standardized, flexible, and easy way to create and share your professional profile. By following the JSON schema and using the CLI tool, you can generate a modern and attractive resume that can be shared with potential employers and contacts.

## Additional Resources for Enhancing Your Online Resume with Hugo and JSON Resume

When creating a dynamic and engaging online resume using Hugo and the JSON Resume module, there are additional resources that can enhance your experience and provide more customization options. Here's a list of valuable resources you might find helpful:

### Profile Studio

**Profile Studio** is an online tool that allows you to preview and customize your JSON Resume in real-time. It's a great way to see how your resume will look and make adjustments on the fly.

- Preview your resume: [Profile Studio Preview](https://profile-studio.netlify.app/#/preview)

### SkillSet Visualization

**SkillSet** is an innovative tool that visualizes the skills section of your JSON Resume. It uses D3.js to create an intuitive and interactive display of your abilities and expertise.

- Visualize your skills: [SkillSet](https://jac21.github.io/SkillSet/)

### LinkedIn to JSON Resume Exporter

This handy tool allows you to export your LinkedIn profile into the JSON Resume format. It's a quick way to transfer your professional data into a structured resume format.

- Export LinkedIn profile: [LinkedIn to JSON Resume Exporter](https://joshuatz.com/projects/web-stuff/linkedin-profile-to-json-resume-exporter/)

### Hugo-Mod-JSON-Resume

This Hugo module is essential for integrating JSON Resume into your Hugo site. It supports multilingual data and offers templates for various sections of your resume.

- Integrate JSON Resume with Hugo: [Hugo-Mod-JSON-Resume](https://github.com/schnerring/hugo-mod-json-resume)

Utilizing these resources, you can effectively create a visually appealing and interactive online resume that showcases your professional journey in the best light possible.