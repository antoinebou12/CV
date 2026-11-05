# AuthLaravel: Sessions, roles and Inertia pages

> AuthLaravel is an access-control learning project with a Laravel backend and Vue pages delivered through Inertia. The route definitions show how…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/authlaravel/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/authlaravel/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/AuthLaravel
- Inspected revision: 2ec4e5d4367341fa789c0027d17ecd43ba80cf01

## Summary

AuthLaravel is an access-control learning project with a Laravel backend and Vue pages delivered through Inertia. The route definitions show how authenticated users reach their dashboard and how administrators receive a different view.

**Why it exists:** Clean Laravel authentication template implementing JWT, session management, and role-based policies.

**Best fit:** Secure boilerplate foundation for Laravel API and web applications.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| PHP | 53.63 |
| TypeScript | 35.05 |
| Blade | 10.93 |
| JavaScript | 0.37 |
| CSS | 0.02 |

## Getting started (repository commands, not run here)

### AuthLaravel/README.md · Steps

```bash
./vendor/bin/sail up -d
npm build
./vendor/bin/sail artisan migrate
./vendor/bin/sail artisan db:seed
http://localhost/login
email: http://localhost:8025
```

### README.md · Steps

```bash
./vendor/bin/sail up -d
npm build
./vendor/bin/sail artisan migrate
./vendor/bin/sail artisan db:seed
http://localhost/login
email: http://localhost:8025
```


## Features and components

- **Routes and middleware** — The dashboard route uses auth and verified middleware, then tests the user’s admin role. The admin branch loads users and renders AdminDashboard; other users receive Dashboard. The /admin route has its own middleware declaration.
- **Pages and account actions** — Inertia connects server-side route decisions to frontend pages. Profile editing delegates to ProfileController, while password-reset routes use Laravel’s password broker. Authentication and page selection are related but separate operations.

## Architecture

Components and connections verified in the repository.

- Browser request → Laravel middleware
- Laravel middleware → Role and route logic
- Role and route logic → Inertia response
- Inertia response → Vue page

```mermaid
flowchart LR
  n0["Browser request"]
  n1["Laravel middleware"]
  n2["Role and route logic"]
  n3["Inertia response"]
  n4["Vue page"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**One path through the code:** Compare /dashboard with /admin in routes/web.php. Both select an administrative page, but their middleware differs. Authorization should be checked on the underlying data operations as well as on page navigation.

## Constraints and checks

This is coursework, not a security certification. The routes alone do not prove that every controller operation enforces the intended role model.

## Files to read

- [AuthLaravel/routes/web.php](https://github.com/antoinebou12/AuthLaravel/blob/main/AuthLaravel/routes/web.php)
- [AuthLaravel/composer.json](https://github.com/antoinebou12/AuthLaravel/blob/main/AuthLaravel/composer.json)
- [AuthLaravel/package.json](https://github.com/antoinebou12/AuthLaravel/blob/main/AuthLaravel/package.json)

