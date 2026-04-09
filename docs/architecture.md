# Architecture

## Current State

- Frontend: multi-page vanilla HTML/CSS/JS in `frontend/`
- Hosting: Cloudflare Pages
- Security headers: `frontend/_headers`
- External embeds: public Google Calendar and YouTube no-cookie

## Site Structure

- `index.html` for landing page and release callout
- `music.html` for embedded videos
- `tour.html` for public Google Calendar agenda view
- `contact.html` for mailto contact flow
- legal pages for imprint and privacy content

## Operating Model

- No backend runtime
- No database
- No server-side secrets required for deployment
