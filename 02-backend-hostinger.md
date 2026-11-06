---
title: 02 — Backend and Database
tags: [kalacar, backend, hostinger, nextjs, database]
status: planning
---

# 02 — Backend and Database

← [[01-architecture]] · next → [[03-admin-and-api]]

## Local phase

Use Next.js server routes/actions for the small custom backend. Run the apps locally and connect only to the owner-created temporary database verified for `kalacar.in`. Product data must be entered by the owner through the dashboard; never seed sample products or create fake orders. The dashboard is a separate local React app but does not own a database connection; do not create a separate API service unless a real limitation appears.

## Later Hostinger phase

Hostinger is the preferred deployment candidate, not yet a verified account-specific decision. Before deploying, prove that the selected plan runs the Next.js server app reliably, can access a database dedicated to `kalacar.in`, preserves product media, and receives Razorpay webhooks reliably despite idle startup behavior. If the proof fails, compare Netlify for the app plus a compatible backend/database host.

For any Hostinger setup, follow workspace-root `AGENTS.md`: confirm the current panel visibly selects `kalacar.in`; verify each database/resource belongs exclusively to it; stop if anything is shared or ambiguous. Do not access or modify other sites or account resources.

## Minimum data

- Products: title, description, price, stock, active status, dimensions/material/care, and image references.
- Customers and sign-in identities: email/password hash or Google identity; never store plaintext passwords.
- Addresses: customer-owned address fields and pincode.
- Orders and order-item snapshots: quoted amounts and status retained at purchase time.
- Payment events: Razorpay IDs/status and unique webhook event IDs for safe retries.
- Coupons only if the shop is ready to offer them.

Store money as integer paise. Use database constraints/transactions to prevent overselling and duplicate payment processing. Keep customer/order access scoped to the signed-in customer and owner dashboard.

## Secrets and payment boundary

Keep database credentials, OAuth secrets, Razorpay API/webhook secrets, and any Maps key on the server in ignored local `.env.local` during development and secure host settings after deployment. Never put values in chat, markdown, Git, browser code, or logs. Only public OAuth client configuration and Razorpay Key ID may be exposed where required. Use Razorpay test mode until launch is explicitly planned.

## File and image handling

Product images must live in storage that persists across deployments. During local work, local files are fine; before launch choose a persistent upload/storage option and verify backups. Do not store uploads in an ephemeral runtime directory.
