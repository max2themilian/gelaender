# Deployment

## Website-Only Release Checklist

1. DNS and edge
   - Point domain to Cloudflare nameservers.
   - Proxy public records through Cloudflare.
   - Enable "Always Use HTTPS" and SSL/TLS mode "Full (strict)".

2. Origin hardening
   - Expose only required backend endpoints.
   - Restrict origin firewall access to Cloudflare egress ranges where possible.
   - Keep environment secrets in server-side environment variables only.

3. API safeguards
   - Run production mode with OpenAPI/docs disabled.
   - Keep CORS restricted to approved frontend origins.
   - Serve security headers (CSP, X-Frame-Options, Referrer-Policy, nosniff).

4. Validation before go-live
   - Verify `/health` returns 200.
   - Verify `/api/tour-dates` and `/api/social-links` return expected JSON.
   - Verify frontend pages render and mailto contact flow works.

5. Post-release monitoring
   - Watch Cloudflare security events and 4xx/5xx trends.
   - Add rate limits for `/api/*` if traffic spikes.

## Google Calendar Shows Sync

1. Create one dedicated Google Calendar for live dates.
2. Add and maintain shows only in this calendar.
3. Set calendar visibility to public.
4. Copy the public ICS link from Google Calendar settings.
5. Add backend environment variable:
   - `GOOGLE_CALENDAR_ICS_URL=<public_ics_url>`
6. Restart backend. `/api/tour-dates` will use Google events automatically.
7. Optional fallback method: `GOOGLE_CALENDAR_ID` + `GOOGLE_API_KEY`.
8. If all Google settings are missing or unavailable, backend falls back to local sample dates.

## Pre-Nameserver Launch Prep

Set these values on the production backend now (before DNS cutover):

1. `APP_ENV=production`
2. `ALLOWED_ORIGINS=["https://gelaender.net","https://www.gelaender.net"]`
3. `GOOGLE_CALENDAR_ICS_URL=https://calendar.google.com/calendar/ical/gelaender18065%40gmail.com/public/basic.ics`

After nameservers are active, run smoke checks:

1. `https://www.gelaender.net` loads over HTTPS.
2. `https://www.gelaender.net` shows the current tour dates.
3. Backend health endpoint returns 200.
4. Backend `/api/tour-dates` returns non-empty JSON and ticket links.

If tour dates fail, verify calendar is still public and the ICS URL is unchanged.
