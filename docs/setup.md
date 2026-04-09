# Setup

## Local frontend

1. Open a terminal in the repository root.
2. Run:

```powershell
Set-Location frontend
python -m http.server 5500
```

3. Open `http://127.0.0.1:5500` in the browser.

## Google Calendar for Shows

1. Create a dedicated Google Calendar for shows.
2. Set calendar visibility to public.
3. Add and maintain shows in that calendar.
4. Verify the embed on `tour.html` shows the current dates.

## Cloudflare Pages

1. Deploy the `frontend/` folder with Cloudflare Pages.
2. Keep `frontend/_headers` in the published output.
3. Use custom domains for `gelaender.net` and `www.gelaender.net`.
