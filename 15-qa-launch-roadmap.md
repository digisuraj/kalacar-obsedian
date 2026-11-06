---
title: 15 — Build and Release Checklist
tags: [kalacar, roadmap, release]
status: planning
---

# 15 — Build and Release Checklist

← [[14-security-seo-performance]] · back → [[00-index]]

## Build in this order

1. Create the local Next.js + TypeScript storefront/API, the separate React + TypeScript owner dashboard, and connect only to the dedicated Kalacar development database.
2. Build the product list/detail pages and a respectful, product-focused mobile layout.
3. Add cart, server-calculated totals, address/pincode, and optional location lookup only if requested.
4. Add customer email/password and Google sign-in, order history, and Razorpay test checkout.
5. Add the protected owner dashboard against the Next.js API for incoming paid orders and manual preparation/dispatch updates.
6. Check core mobile and desktop flows, payment failure/retry, access controls, and secret handling.
7. Only when requested, validate hosting with a deployment proof, then plan DNS and live payments.

Keep scope notes in [[00-index]]. Do not build features simply because a large e-commerce checklist suggests them.

## Essential acceptance checklist

- [ ] Products show accurate photos, price, stock, dimensions/material, and care information.
- [ ] Customer can create an account or sign in with email/password or Google, browse, add to cart, enter an address, and check out.
- [ ] Server rechecks prices and stock; payment state is verified with Razorpay before an order is treated as paid.
- [ ] Customer can see their own order history; one customer cannot read another's orders.
- [ ] Owner can securely see new paid orders, prepare them, mark dispatch/delivery, and add optional tracking details.
- [ ] Manual shipping works without courier integration. Order status and customer notifications are clear.
- [ ] Address works without geolocation. If location lookup is included, test allowed/denied/unavailable cases and keep manual entry available.
- [ ] Razorpay/database/OAuth secrets stay server-side and out of Git, chat, notes, and browser assets.
- [ ] Essential policy/contact details are present before real payments.
- [ ] The verified Hostinger plan, `kalacar.in` target context, persistent images/database, and webhook behavior are checked before any deployment.

## Launch decisions

Before accepting real orders, confirm catalogue and photos, tax presentation, delivery fees/estimate, refund/cancellation terms, customer support details, persistent image storage, backup approach, and whether Hostinger's app behavior meets payment/webhook needs. Use workspace-root `AGENTS.md` for any Hostinger panel work. Domain mapping and live Razorpay are later owner decisions.
