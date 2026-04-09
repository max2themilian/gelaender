# Gelaender Project Guidelines

## Project Overview
This project is a static band website for Gelaender with a vanilla multi-page frontend hosted on Cloudflare Pages.

## Architecture
- Keep frontend code in frontend/
- Keep docs in docs/
- Do not reintroduce backend or database code unless explicitly requested.

## Frontend Conventions
- Use semantic HTML structure and accessible landmarks.
- Use modular CSS with tokens in variables.css.
- Use progressive enhancement JavaScript.
- Build mobile-first and preserve a restrained DDR-inspired visual language.

## Security Rules
- Never commit secrets.
- Keep the site static unless explicitly scoped otherwise.
- Use Cloudflare Pages headers via frontend/_headers.
- Prefer public embeds and outbound links over custom server logic.

## Review Expectations
- Prioritize findings first: bugs, risks, regressions, and missing tests.
- If no findings exist, state that and mention residual risks.
