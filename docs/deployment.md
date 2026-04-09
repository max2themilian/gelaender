# Deployment

## Recommended Now: Static-Only on Cloudflare (No Backend)

This is the best launch path for the current project goals:

- No extra hosting cost for API/runtime.
- Smaller attack surface and lower maintenance overhead.
- Fast global delivery through Cloudflare.
- Shows can still auto-update via embedded public Google Calendar.

## Hosting Choice

Use Cloudflare Pages on the free plan and deploy the `frontend/` folder as a static site.

Recommended setup:

1. Cloudflare Dashboard
2. `Workers & Pages`
3. `Create application`
4. `Pages`
5. Connect GitHub repo or use direct upload
6. Project root / output: `frontend`
7. No build command required for the current site

## Cloudflare Go-Live Checklist

1. Domain and DNS
   - Nameservers already point to Cloudflare.
   - Ensure `www` and root domain resolve to your static site origin.
   - Keep mail records (`MX`, SPF/TXT) as DNS-only.

2. SSL/TLS and transport
   - Enable "Always Use HTTPS".
   - Enable "Automatic HTTPS Rewrites".
   - Enable HSTS after verifying everything works over HTTPS.

3. Baseline edge security
   - Enable WAF managed rules.
   - Enable Bot Fight Mode.
   - Keep Development Mode disabled in normal operation.
   - Keep the `frontend/_headers` file in the deploy so Pages serves security headers.

4. Static site checks
   - `https://gelaender.net` loads.
   - `https://www.gelaender.net` loads.
   - Navigation works across all pages.
   - Contact form triggers mail client correctly.

5. Shows page checks
   - `tour.html` displays the embedded Google Calendar.
   - "Open full calendar" opens the public calendar in a new tab.
   - New Google Calendar events appear on site after Google refresh.

## Custom Domain Setup in Pages

1. Add `gelaender.net` as a custom domain.
2. Add `www.gelaender.net` as a custom domain.
3. Set one hostname as canonical.
4. Redirect the secondary hostname to the canonical hostname.

If you want the public-facing domain to be `www.gelaender.net`, make `www` canonical and redirect root to `www`.

## Google Calendar Without Backend

Use a public calendar and embed it directly in the shows page.

1. Keep calendar visibility set to public.
2. Add or edit shows in Google Calendar.
3. Site updates automatically through the embedded agenda view.

No Google Cloud billing, no API key, and no backend runtime required.

## Optional Phase 2 (Later)

If you later need custom event cards, ticket-link parsing, or stricter control over output format, re-enable the FastAPI backend and use the ICS ingestion route.
