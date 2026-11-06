---
title: 04 — Next.js + TypeScript App
tags: [kalacar, nextjs, typescript, frontend]
status: planning
---

# 04 — Next.js + TypeScript App

← [[03-admin-and-api]] · next → [[07-product-page]]

## Stack

- Next.js App Router, React, TypeScript.
- Local development first. Hosting is undecided until a small deployment proof; see [[01-architecture]].
- Keep the storefront, account, and server routes in `kalacar-app`; keep the React + TypeScript owner dashboard in `kalacar-dashboard`. The dashboard calls the Next.js API and never opens a database connection from the browser.
- Prefer built-in Next.js features and a small dependency list. Add a service/package only when a required feature needs it.
- Server code is authoritative for product price, stock, customer/order access, and payment status.

## Essential routes

```text
Storefront routes currently implemented:
/
/products/[slug]
/cart          (currently contains cart and checkout form)
/account       (sign-in/register tabs and customer order history)

Dashboard:
separate Vite application; Overview, Products, and Orders are client-side sections

Server API:
/api/products, /api/auth/*, /api/account/orders/*,
/api/checkout/*, /api/admin/*, /api/webhooks/razorpay
```

The checkout note specifies a dedicated `/checkout` route. The progress checklist tracks the unresolved route decision; do not assume `/cart` and `/checkout` are interchangeable without recording that decision.

Add About, Contact, and policy pages when verified business content is available. Do not add content-management tools in v1; static content is enough.

## Sign-in

Support email/password and Google sign-in. Include email verification, password reset, secure server-managed sessions, and sign-out. Only the owner identity can access `/admin`; enforce this on every server action/route. Check that customers can access only their own orders and addresses.

## Store and checkout behavior

- Browser cart stores product IDs and quantities, not trusted prices.
- Server recalculates totals and stock before checkout.
- Manual address and pincode entry always work. Current location lookup is optional, requested only after a customer taps the button, and must not block manual checkout.
- Razorpay handles payment entry; server verifies the result before marking an order paid.
- Provide clear loading, validation, payment-failure, retry, and order-confirmation states. Prevent duplicate order creation on repeated taps.

## Local configuration

Keep private secrets in an ignored `.env.local`, and verify it is covered by `.gitignore`. Never expose private values through `NEXT_PUBLIC_*`, browser code, chat, notes, or Git. Keep `.env.example` to names and dummy values. See [[02-backend-hostinger]] and [[10-razorpay-payments]].

## UI direction

Follow [[Ui-instruction]]: focused, respectful storefront for small devotional idols, with factual size/material/finish details and calm product photography. Use a simple mobile-first product grid and checkout. The dashboard is a distinct local application in its own repository, sharing the Next.js API. See [[16-progress-checklist]] for the authoritative route and release tasks.
