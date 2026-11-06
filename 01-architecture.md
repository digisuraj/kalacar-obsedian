---
title: 01 — Kalacar Architecture
tags: [kalacar, architecture, nextjs, typescript, hostinger]
status: planning
---

# 01 — Kalacar Architecture

← [[00-index]] · next → [[02-backend-hostinger]]

## Simple starting architecture

```text
Customer browser ──► Next.js + TypeScript app (`kalacar-app`)
                         ├─ storefront and customer account
                         ├─ server routes for catalogue, auth, orders, checkout, webhooks
                         └─ database access (server only)
                              ├─ dedicated Kalacar database
                              └─ Razorpay APIs / verified webhook

Owner browser ─────► React + TypeScript dashboard (`kalacar-dashboard`)
                         └─ calls the Next.js API; never connects to MySQL directly
```

Develop and run both projects locally first. The owner dashboard is a separate repository and application, but shares the Next.js API and dedicated Kalacar database. Decide whether the two projects share or use separate production deployments only after the owner authorizes and reviews a deployment proof.

## Hosting recommendation

**Preferred first deployment candidate: Hostinger, subject to a small deployment proof.** Current Hostinger documentation says its Node.js hosting supports Next.js on eligible Business/Cloud plans. Its apps run on demand and can stop after inactivity, so test first-request behavior, Razorpay webhooks, and database connections before accepting real orders. Do not infer that the account's current plan or a specific website resource is suitable until verified.

**Netlify remains a good alternative** for the Next.js app and supports Next.js server-rendered features through its adapter. It would mean keeping the API/database elsewhere and adds a cross-host connection to configure. Because the user already has Hostinger and wants a small system, one Hostinger app is the lower-complexity starting plan if the proof works. Netlify is managed hosting; its adapter being open source does not make the hosted service itself open source.

No deployment, DNS change, live payment, or Hostinger panel mutation is part of the current local phase. Before later Hostinger changes, follow workspace-root `AGENTS.md` and verify the selected site is exactly `kalacar.in` and all affected resources belong only to it.

## Responsibilities and trust boundaries

- Next.js server code owns authentication, authorization, prices, stock, order records, quote calculations, and Razorpay verification.
- The browser may submit product IDs, quantities, address fields, and coupon code. It never decides trusted price or order total.
- Customer routes can read only that customer's account/orders. Every `/api/admin/*` request requires server-side owner authorization; hiding dashboard controls is not security.
- Razorpay secrets and database credentials stay server-side in environment settings. Never expose them through browser code, `NEXT_PUBLIC_*`, logs, chat, or notes.
- The database is dedicated to Kalacar. Do not connect to a shared or ambiguously associated Hostinger database.
- The owner updates packing/dispatch status manually. No courier API is required.

## Core purchase flow

1. Customer adds items to cart and enters a delivery pincode/address.
2. Server re-reads current prices and stock and calculates the quote.
3. Server creates a pending order and Razorpay order; client opens Razorpay Checkout using only the public Key ID.
4. Server verifies payment signature and amount; a signed webhook confirms/reconciles final payment state.
5. The owner sees the paid order in the separate dashboard, prepares it, and records dispatched/delivered status and optional tracking details.

## Keep the implementation small

Keep one Next.js server/API project, one lightweight dashboard project, one dedicated SQL database, and a small set of tables: products, customers/auth identities, addresses, orders, order items, payment events, and optional coupons. Add tables only when a real feature requires them. Use migrations and fake local seed data. Avoid a separate API service, content-management system, analytics stack, or microservices unless the prototype shows a clear need.

## Official hosting references

- [Hostinger Node.js hosting overview](https://docs.hostinger.com/node.js/overview)
- [Hostinger Node.js deployment guide](https://www.hostinger.com/support/how-to-deploy-a-nodejs-website-in-hostinger/)
- [Netlify Next.js support](https://docs.netlify.com/build/frameworks/framework-setup-guides/nextjs/overview/)

These describe provider support in general, not the user's account-specific eligibility. Verify the active plan and the Kalacar resource context before deployment.
