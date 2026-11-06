---
title: 21 — Production Settings
tags: [kalacar, deployment, environment, checklist]
status: active
updated: 2026-11-06
---

# 21 — Production Settings

Everything that must be set on Hostinger when code reaches `main`. **Add new settings before merging**, so the first deploy already has them. Values never go in chat, notes, Git or screenshots.

Confirm the selected site in hPanel before saving. See `AGENTS.md`.

## Add now: customer shop site

Currently `firebrick-squid-218523.hostingersite.com`.

| Variable | Value | Where to get it | If missing |
|---|---|---|---|
| `PUSHER_APP_ID` | Your app ID | `kalacar-app/.env.local` or Pusher > App Keys | Live updates off; pages use slower timers |
| `PUSHER_KEY` | Your key | Same | Same |
| `PUSHER_SECRET` | **Secret** | Same | Same |
| `PUSHER_CLUSTER` | `ap2` | Same | Same |
| `VAPID_PUBLIC_KEY` | Production key | `kalacar-app/.env.production-values.local` | Pop-up alerts stay off |
| `VAPID_PRIVATE_KEY` | **Secret**, production key | Same | Same |
| `VAPID_SUBJECT` | `https://kalacar.in` | Same | Same |

To open the private file, use VS Code, or show hidden files in Finder with `Cmd + Shift + .`. It isn't uploaded to GitHub. Production has its own VAPID keys, separate from the ones on your Mac.

The dashboard site needs no Pusher or VAPID settings, because it gets what it needs from the shop.

**Steps:**
1. In hPanel, open the shop site and confirm the selected site is correct.
2. Add the seven variables above.
3. Save and redeploy, or merge to `main` so it deploys.
4. Check `/api/realtime/config` on the shop. It should show a key and cluster `ap2`.
5. In the dashboard, open **Settings > Order alerts**, click **Turn on**, then **Send test alert**.

## Every setting at a glance

Each setting is also explained in `kalacar-app/.env.example` and `kalacar-dashboard/.env.example`. Real values go in `.env.local` on a computer and in Hostinger for production. Those two places are never uploaded to GitHub.

| Setting | What it's for | Development and production | Secret? | If missing |
|---|---|---|---|---|
| `DB_HOST` | Database address | Different: `srv2210.hstgr.io` on a computer, `localhost` on Hostinger | No | Shop can't load data |
| `DB_PORT` | Database port | Same, usually 3306 | No | Uses 3306 |
| `DB_NAME`, `DB_USER` | Which database and user | Different at launch | No | Shop can't load data |
| `DB_PASSWORD` | Database password | Different at launch | **Yes** | Shop can't load data |
| `QA_DB_NAME` | Separate database for `npm run qa` | Development only | No | `npm run qa` refuses to run |
| `RAZORPAY_KEY_ID` | Payment account | Different: test until launch, then live | No | Customers can't pay |
| `RAZORPAY_KEY_SECRET` | Proves requests to Razorpay | Different | **Yes** | Customers can't pay |
| `RAZORPAY_WEBHOOK_SECRET` | Lets Razorpay confirm payments directly | Different | **Yes** | Webhook off |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google sign-in | Same while testing; new at launch recommended | Secret: **Yes** | Google sign-in off |
| `KALACAR_OWNER_EMAILS` | Who can open the dashboard | Same | No | Nobody can open it |
| `NEXT_PUBLIC_SITE_URL` | The shop's own address | Different | No | Some links use the wrong address |
| `NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY` | Shows the checkout map | Different | Visible in browsers; restrict it | Map off; typing an address still works |
| `GOOGLE_MAPS_SERVER_KEY` | Turns a map pin into an address | Different | **Yes** | Map lookup off |
| `PUSHER_APP_ID`, `PUSHER_KEY`, `PUSHER_CLUSTER` | Live updates | Same while testing; separate app at launch recommended | No | Slower timers; no viewer count |
| `PUSHER_SECRET` | Sends signals | As above | **Yes** | As above |
| `VAPID_PUBLIC_KEY` | Pop-up alerts | Different | No | Pop-ups off |
| `VAPID_PRIVATE_KEY` | Proves pop-ups come from your server | Different | **Yes** | Pop-ups off |
| `VAPID_SUBJECT` | Shop's contact address | Same | No | Pop-ups off |
| `KALACAR_LOW_STOCK_THRESHOLD` | Low stock count on the dashboard Overview | Same | No | Uses 3 |
| `KALACAR_ALLOW_SEARCH` | Lets Google list the shop | Production only, at launch: `true`, then rebuild | No | Google is told not to list it |
| `VITE_API_BASE_URL` (dashboard) | Where the local shop runs | Development only | No | Uses `http://127.0.0.1:3000` |
| `KALACAR_SHOP_URL` (dashboard) | The shop's address | Production only | No | Uses the test shop address |

## Already set: customer shop site

Keep these. Don't paste values here.

`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_MAPS_SERVER_KEY`, `NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY`, `KALACAR_OWNER_EMAILS`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `NEXT_PUBLIC_SITE_URL`.

Compare this list with hPanel and `kalacar-app/.env.local`, as it was written from the notes, not read from Hostinger.

## Already set: dashboard site

Currently `sienna-herring-231344.hostingersite.com`, Express preset, entry `server.cjs`. `KALACAR_SHOP_URL` is optional until launch, when it must point to the real shop address.

## Still to add

| Variable | When | Why |
|---|---|---|
| `RAZORPAY_WEBHOOK_SECRET` | When the webhook is set up | Confirms payments when a customer closes the page |
| Cron job for the payment recheck | With the webhook | Covers times when no dashboard is open; the route is still to be built |

## Connecting kalacar.in

Do this in order. The shop must be set to Coming soon first, and the shop's code must include the `kalacar.in` addresses.

1. Dashboard: **Settings > Shop > Shop status > Coming soon**.
2. hPanel: free `kalacar.in` from the WordPress site, confirming it's the right site first.
3. hPanel: **Websites > `firebrick-squid-218523` > ⋮ > Connect domain**, enter `kalacar.in`.
4. hPanel: connect `admin.kalacar.in` to the dashboard site, `sienna-herring-231344`.
5. Shop site: set `NEXT_PUBLIC_SITE_URL=https://kalacar.in`. Dashboard site: set `KALACAR_SHOP_URL=https://kalacar.in`. Redeploy both.
6. Google Cloud: add origins `https://kalacar.in` and `https://admin.kalacar.in`, redirect URIs `https://kalacar.in/api/auth/google/callback` and `https://admin.kalacar.in/api/auth/google/callback`, and `https://kalacar.in/*` on the Maps browser key.
7. Dashboard: **Settings > Shop > Website link** to `https://kalacar.in`.
8. Test sign-in on both sites, Pages, live updates and a test payment.

## At launch

See [[16-progress-checklist]] Stages 8, 8A and 8B. These change at launch:

- `DB_*`: a production database dedicated to `kalacar.in`, also allowed in `catalogue-db.ts`.
- `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`: live keys, after explicit approval. Checkout code must also allow them.
- `NEXT_PUBLIC_SITE_URL` and the dashboard's `KALACAR_SHOP_URL`: real addresses, also added to `public-origin.ts`.
- `VAPID_SUBJECT`: already `https://kalacar.in`.
- `PUSHER_*`: consider a separate Pusher app for the real shop.

## Rotate before launch

- Database password: exposed in a screenshot.
- Google client secret: exposed in chat.

## Database changes

Tables and columns are added automatically when the shop first connects. Nothing to do by hand. Recent additions: `kalacar_push_devices`, and `updated_at` on `kalacar_orders`.

See also [[20-live-updates-architecture]].
