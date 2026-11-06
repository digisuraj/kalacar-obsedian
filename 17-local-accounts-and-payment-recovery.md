---
title: Kalacar — Local Accounts and Payment Recovery
tags: [kalacar, accounts, payments, local-development]
status: active
---

# Local accounts and payment recovery

This note describes current local-only account and payment behavior. Work remains governed by [[16-progress-checklist]]. No deployment, live payment, or Hostinger panel change is authorized by this note.

## Customer accounts

There are no seeded test accounts. The three `@example.test` demo accounts, their startup seeding, and `KALACAR_DEMO_PASSWORD` were removed on 2026-11-04, and the database started with no users.

Customers sign in at `/account` with **Continue with Google** (Google-verified email only) or by registering with email and password. A Google sign-in links to an existing account with the same email.

Customers may also register another local account at `/account`. Passwords are stored as scrypt hashes. Session tokens are random, stored in the browser as HttpOnly, SameSite=Lax cookies, and persisted in the database only as SHA-256 hashes with a seven-day expiry. Authentication and local Razorpay test checkout fail closed outside development.

## Owner dashboard sign-in

The dashboard uses **Google sign-in** through the Next.js API. Only Google accounts whose email is listed in `KALACAR_OWNER_EMAILS` (comma-separated, in the ignored `kalacar-app/.env.local`) can open it. The server enforces this on every `/api/admin/*` route, answering 401 when signed out and 403 for non-owners; the screens only mirror that check. To change access, edit the list and restart `npm run dev`. While the Google app is in Testing mode, each owner must also be listed under **Test users** in Google Cloud Console. All login still fails closed outside development.

## Checkout and recovery

1. A customer signs in before checkout. Name, email, and phone come from the account; delivery address and PIN are captured at checkout.
2. The server checks current product stock and prices, then reserves stock and stores the order and item snapshot transactionally before opening Razorpay.
3. The server verifies the signed checkout response and confirms captured payment against Razorpay before marking the order paid.
4. The cart saves the idempotency key and payment order in browser storage before opening Razorpay. The outer Checkout sheet confirms before closing and disables backdrop, Escape, and browser-back dismissal. Razorpay controls navigation inside its OTP/payment subviews; going back to payment options does not cancel the saved order or establish whether payment was captured. Leaving the sheet never erases the local order; the app checks status after dismissal, when the customer returns to the tab, and when they open account orders. The same idempotency key/provider order is reused after reload so a retry does not make a duplicate order.
5. The order stays visible in `/account` if the browser closes or callback is lost. The customer can check payment status against Razorpay's payment records or retry payment against the saved Razorpay order.
6. A verified signed webhook route is available at `/api/webhooks/razorpay`. It needs a secret stored only in ignored environment settings and a public, reachable server URL before it can receive events. Localhost is not a public webhook target.

If Razorpay cannot be reached during a status check, the order stays saved as pending; do not tell the customer that payment failed or ask them to create another order. Use the order-specific WhatsApp contact so the owner can reconcile the payment.

## Support contact

Owner-provided WhatsApp contact: `+91 88306 46308`. Store and order help links open WhatsApp with an order reference prefilled where available. The customer must tap Send; the app does not send messages automatically.

## Not configured yet

- Email verification, password reset, and a mail provider. (Google sign-in works locally; production enablement and owner end-to-end verification are pending in [[16-progress-checklist]].)
- Production-grade account lifecycle, rate limiting, and public deployment.
- Razorpay webhook secret and publicly reachable webhook URL.
- Production database, production payment credentials, and release QA.
