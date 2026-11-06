---
title: 14 — Essential Security and Launch Checks
tags: [ecommerce, security, launch]
status: planning
---

# 14 — Essential Security and Launch Checks

← [[13-static-pages-and-legal]] · next → [[15-qa-launch-roadmap]]

Keep this note limited to safeguards required for accounts, customer data, orders, and payments.

## 1. Protect accounts and private data

- Store passwords as one-way hashes; never plaintext. Verify email ownership and make password reset tokens short-lived and single-use.
- Keep customer and admin sessions in secure `HttpOnly` cookies. Admin and customer roles are separate; Google sign-in does not grant admin access.
- Check user/order ownership on every private request. IDs alone are not proof of access.
- Validate all input on the backend. Use parameterized database queries. Escape/sanitize editable content before rendering.
- Protect state-changing requests against CSRF and use reasonable server-side limits on login, password reset, coupons, checkout, and contact forms.
- Never expose database credentials, Google OAuth client secret, Google Maps key, Razorpay API secret, or webhook secret in browser code, chat, screenshots, markdown, logs, or Git.
- For local work, use ignored backend `.env.local`; commit only `.env.example` with empty/dummy values. If any secret is exposed, rotate it.

## 2. Protect orders and payments

- Backend calculates all prices, tax, shipping, coupon discounts, and stock. Recalculate at checkout.
- Create orders and reserve stock transactionally with idempotency keys to prevent duplicate orders/overselling.
- Verify Razorpay callbacks and signed webhooks server-side against the order ID, currency, exact amount, and current payment state. Fulfil only confirmed captured payments.
- Handle duplicate/late webhook delivery safely. Keep a simple reconciliation process for payment/order mismatches.
- Razorpay collects payment details; Kalacar does not store card details.
- Manual shipping is the initial workflow. Admin status changes must be recorded; a tracking reference is optional.

## 3. Optional location lookup

- Ask for location only after the customer explicitly taps the location button.
- Send coordinates to the backend once; do not persist or log them. Keep manual address and pincode entry available.
- Keep Google Maps/Geocoding credentials on the backend. If the feature is not enabled, do not configure a maps key.

## 4. Basic privacy and reliability

- Collect only data needed to fulfil orders and support customers. Set a retention policy before production.
- Back up the database and product media before accepting real orders; document how to restore them.
- Log request IDs and useful error codes, but never passwords, secrets, full addresses, or location coordinates.
- Before deployment, confirm HTTPS, database ownership, least-privilege database user, backend secret settings, and webhook reachability.

## 5. Basic SEO

- Add a title and description to each public page, canonical URLs after domain routing is decided, and a sitemap/robots file.
- Product structured data must reflect real product, price, and stock data.
- Keep cart, checkout, account, admin, and order pages out of search results.

## 6. Ready-to-launch checks (future)

- [ ] Email/password and Google sign-in work; private account/order data is protected.
- [ ] Razorpay test success, failure, retry, invalid signature, duplicate webhook, and refund flows work.
- [ ] Prices, stock, coupon limits, and order amounts are confirmed by the backend.
- [ ] No private credential appears in the browser bundle or Git history.
- [ ] Database and media backup can be restored.
- [ ] Mobile checkout, address entry, optional location lookup (if enabled), and manual shipping status are usable.
- [ ] Legal, tax, shipping, and refund policies are confirmed before taking real orders.
