---
title: Kalacar — Project Instructions
tags: [kalacar, nextjs, typescript, hostinger, razorpay]
status: planning
created: 2026-11-02
---

# Kalacar — Project Instructions

## Product and scope

Kalacar (K-A-L-A-C-A-R) is a small, owner-run shop for 3D-printed Hindu deity idols and related devotional decor, such as Ganpati, Shankar, and Krishna. Build a focused catalogue and checkout, not a general marketplace or apparel store. Use accurate product photos, dimensions, materials, finish, and care information; keep the visual style respectful, calm, warm, and product-led.

## Confirmed v1

- **Stack:** Next.js + TypeScript, developed locally first. No WordPress or WooCommerce.
- **Hosting direction:** Hostinger is the preferred first option for one Next.js app, its server-side API, and a dedicated Kalacar database, subject to confirming plan/runtime behavior before deployment. Netlify is a valid alternative for the Next.js app if preferred after the local prototype. No hosting or DNS changes now.
- **Domain:** `kalacar.in` is owned; use localhost until deployment is deliberately planned.
- **Store:** product list/details, cart, address and pincode, Razorpay checkout, confirmation, and customer order history.
- **Accounts:** email/password and Google sign-in; include verification and password reset.
- **Owner dashboard:** a small protected React + TypeScript app in the separate `kalacar-dashboard` repository. It calls the Next.js API in `kalacar-app`; it does not connect to MySQL from the browser. Keep hosting/deployment topology undecided until the local product is complete and a deployment proof is authorized.
- **Payments:** Razorpay, with order creation and verification on the server. Test credentials later go in ignored local `.env.local`; never paste secrets in chat or notes.
- **Address:** manual address and pincode always work. “Use my current location” is optional and only added if requested; if enabled, use Google Maps with the key kept server-side.

## Leave out of v1

No WordPress, WooCommerce, marketplace features, apparel, courier integrations, automated shipping, complex admin/content systems, Google Business Profile work, Instagram/reels integrations, social widgets, analytics dashboards, or location lookup unless the owner later asks.

## Local-first and Hostinger boundary

Develop locally with actual owner-entered product and order data and test-mode payments. Do not create fake product, inventory, customer, order, review, coupon, or other business records. When real records are absent or an API fails, show a truthful empty, loading, or unavailable state; never substitute in-code sample data. A clearly labeled local-only demo login is the sole exception while real Google/owner authentication credentials are unavailable. This exception grants no permission to generate demo business records. Any later Hostinger action is limited to `kalacar.in` and resources positively verified as dedicated to it. Follow the workspace-root `AGENTS.md` checks before every panel change; do not touch any other site, service, or database in the account.

## AI-assisted coding and installed skills

- Before attempting a code or configuration change, inspect the relevant repository's installed skills (including repository-local `.agents/skills`) and the available Codex skill catalog. Read and follow the applicable `SKILL.md`; when a task spans apps, check the skills for each app.
- Do not add hardcoded business fixtures or startup seeding for products, prices, stock, customers, orders, coupons, or reviews in either app. Read business data from the shared database/API. If there is no real data or a connection fails, show an honest empty/loading/error state. Demo data is prohibited except for a clearly labeled local-only login account or login gate while real auth credentials are unavailable; never use that exception to seed business records.
- Treat skill prerequisites and required verification steps as mandatory. Do not skip a skill because another workflow seems easier. If a tool name differs, inspect the live tool description and use a replacement only when it explicitly provides the same diagnostic; document the verified mapping in the project skill and this note. Do not silently replace a required check with a weaker alternative.
- For Next.js app work, use `kalacar-app/.agents/skills/next-dev-loop/SKILL.md`. Complete its version, bundler, CLI, and `/_next/mcp` preflight before editing Next.js code. If a hard prerequisite or equivalent MCP diagnostic is missing, follow the skill's prescribed install/upgrade remedy when authorized or stop and report the exact blocker.
- For React/Vite dashboard work, inspect and apply any relevant installed React/dashboard skills; verify the dashboard behavior in its local browser as well as running its production build.
- For each feature, implement and self-verify it, then give the owner concrete **Your check** steps for ad hoc human verification. Update [[16-progress-checklist]] truthfully. Commit and push the feature only after the owner's verification or a later explicit instruction to commit.

## Notes

Execution follows [[16-progress-checklist]] only. Treat the other notes as supporting reference; do not build extra features unless the owner updates the checklist.

| Note | Purpose |
|---|---|
| [[01-architecture]] | One-app architecture and hosting choice |
| [[02-backend-hostinger]] | Local backend/database and later Hostinger constraints |
| [[03-admin-and-api]] | Minimal owner dashboard and order flow |
| [[04-frontend-foundation]] | Next.js routes, account, and shared UI |
| [[07-product-page]] | Idol product detail behavior |
| [[08-cart-and-coupons]] | Cart and optional simple coupons |
| [[09-checkout-and-address]] | Checkout, address, optional location |
| [[10-razorpay-payments]] | Server-side Razorpay flow |
| [[13-static-pages-and-legal]] | Essential store information and policies |
| [[14-security-seo-performance]] | Essential security and launch basics |
| [[15-qa-launch-roadmap]] | Small build order and release checklist |
| [[16-progress-checklist]] | Single ordered execution checklist and progress log |
| [[17-local-accounts-and-payment-recovery]] | Local customer accounts, order status recovery, and support contact |
| [[18-woocommerce-parity-and-dashboard-spec]] | WooCommerce parity feature spec, dashboard UI modules, and API contracts |
| [[19-how-kalacar-works]] | Plain-language walkthrough of every working feature with flow diagrams (plus the Excalidraw drawing [[19-kalacar-flows.excalidraw]]) — for explaining the site to someone |
| [[Ui-instruction]] | Storefront visual direction |

## Decide before launch

Confirm product catalogue, price/tax display, shipping fee and estimate, cancellation/refund policy, support contact, and whether location lookup is wanted. Hosting provider and domain routing can be finalized after the local app works.
