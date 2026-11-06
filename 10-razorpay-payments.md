---
title: 10 — Razorpay Payments
tags: [ecom, payments, razorpay, security]
status: planning
---

# 10 — Razorpay Payments

← [[09-checkout-and-address]] · next → [[13-static-pages-and-legal]]

## Goal and non-negotiable rules

- Razorpay is the payment processor; the custom backend is the authority for prices, orders, payment state, inventory, and fulfilment.
- Use Razorpay Standard Checkout so card/payment credentials are collected by Razorpay, not by Kalacar.
- No secret values in chat, Obsidian, screenshots, source code, Git, browser bundles, or logs. A test account or separate Razorpay account does not make sharing a secret in chat safe.
- Local phase: test mode only, fake customer/product data, local webhook forwarding where required. Do not attempt live payments or deploy credentials.
- Store test credentials only in ignored `.env.local` after `.gitignore` is confirmed. `.env.example` contains variable names and dummy values only. On production, set secrets in the backend host's secret store.

## 1. Credential boundaries

| Value | May reach browser? | Storage |
|---|---:|---|
| Razorpay Key ID | Yes, only when initializing Checkout | Backend returns it for the configured mode |
| Razorpay API Key Secret | **Never** | Backend environment/secret store only |
| Webhook Secret | **Never** | Backend environment/secret store only; separate from API secret |
| Database credentials | **Never** | Backend environment/secret store only |

If any secret is pasted into chat, committed, added to an image, or exposed in a browser bundle, treat it as compromised: revoke/rotate it in Razorpay and update the backend configuration. Do not copy it into project documentation.

## 2. Create-order and checkout flow

1. Storefront calls backend quote endpoint with cart IDs/quantities, coupon, and delivery address/pincode.
2. Backend re-reads products, prices, promotions, inventory, coupon use, shipping, and tax. Reject invalid, unpublished, or unavailable lines.
3. Backend accepts only an unexpired quote token/hash, then uses a database transaction and idempotency key to create one pending local order and reserve stock.
4. Backend creates a Razorpay Order server-side using the exact amount in paise and `INR`; persist the Razorpay order ID linked to the local order.
5. Backend returns only the public Key ID, Razorpay order ID, amount, currency, and safe prefill details.
6. Storefront lazy-loads `checkout.js` and opens the hosted Razorpay Checkout. It does not accept or calculate the payable amount as authority.
7. On Checkout success, send Razorpay payment ID, order ID, and signature to the backend verify endpoint. Show a pending/processing state until the backend confirms.
8. On dismissal or failure, keep the local order pending during its reservation window and offer a safe retry; do not create another order accidentally.

## 3. Callback verification

Backend must:

- Look up the local order and expected Razorpay order ID; confirm the callback belongs to that order.
- Verify the Checkout signature with the Razorpay API Key Secret using the official documented formula/SDK.
- Fetch payment/order status from Razorpay when immediate confirmation is needed; compare exact amount, currency, provider order ID, and captured status.
- Be idempotent: repeated valid callbacks return the existing result and do not double-decrement stock, create duplicate fulfilment, or send duplicate emails.
- Never trust a client-supplied `success: true`, amount, currency, customer, or product price.

## 4. Webhooks

- Endpoint lives on the backend, e.g. `/api/v1/webhooks/razorpay`; configure it in the Razorpay dashboard only during deployment setup.
- Verify `X-Razorpay-Signature` using HMAC-SHA256 over the **raw, unchanged request body** and the dedicated Webhook Secret. Do not parse/re-serialize JSON before signature verification.
- Persist each provider event ID under a unique constraint before applying effects; duplicate deliveries must be safe.
- Handle the selected events for captured, failed, authorized, order paid, and refund updates. Use event payload identifiers to fetch current state if needed; do not assume event order.
- Return success only after durable event receipt. On transient processing errors, preserve retryability and alert; add reconciliation for events that never arrive.
- Keep webhook path reachable and exempt it from user-session CSRF while requiring valid provider signature, rate controls, payload limits, and logging hygiene.

## 5. Local test plan

- Use Razorpay Test Mode keys only; run a local backend with a local database and seeded products.
- Exercise success, failed payment, modal dismissal, network timeout, duplicate callback, duplicate webhook, invalid signature, wrong amount/currency, late payment after stock release, refund success/failure, and reconciliation.
- Verify exact paise amount consistency from quote → local order → Razorpay order → callback/webhook.
- Verify customer success page cannot reveal another customer's order; use an order ownership check or high-entropy guest access token.
- Verify an unpaid/failed order never triggers fulfilment and an unverified callback never clears the cart.
- Before production, repeat the end-to-end matrix in a private staging environment using test keys and a separate webhook endpoint.

## 6. Production activation checklist (future; not part of local work)

- [ ] Razorpay business/KYC approval and policy pages complete.
- [ ] Production backend and database verified, backups restored successfully, secrets configured without chat or Git.
- [ ] HTTPS storefront/backend origins and CORS configured; live webhook endpoint reachable.
- [ ] Live credentials generated in Razorpay Dashboard and entered directly into backend secret settings.
- [ ] Live/test mode guard is visible in admin, impossible to switch accidentally, and audited.
- [ ] Make one explicitly authorized low-value live test only after the launch plan is approved; refund/check settlement as appropriate.
- [ ] Confirm order/payment reconciliation, alerts, refund permissions, and support procedure.
