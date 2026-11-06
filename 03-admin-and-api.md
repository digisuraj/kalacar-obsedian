---
title: 03 — Owner Dashboard & Administration
tags: [kalacar, admin, orders, woocommerce, parity]
status: active
updated: 2026-11-03
---

# 03 — Owner Dashboard & Administration

← [[02-backend-hostinger]] · next → [[04-frontend-foundation]] · specification → [[18-woocommerce-parity-and-dashboard-spec]]

## Purpose

A dedicated, lightweight owner workspace providing full operational feature parity with the previously used WooCommerce store (`kalacar.in`), built as a high-performance React + TypeScript application (`kalacar-dashboard`) that interfaces with the Next.js API backend (`kalacar-app`).

The owner dashboard acts as the daily operations center for inventory management, customer order verification, fulfillment/dispatch tracking, promotional coupons, customer purchase insights, and store settings.

## Core Modules & Parity Scope

### 1. Global Shell & Navigation
- **Persistent Sidebar:** Overview, Orders (with pending badge count), Products, Customers, Coupons, Settings.
- **Top Bar:** Quick search (`Ctrl+K`), Admin identity profile, and **Store Visibility Status Pill** (`Coming soon` / `Live`).
- **UI Tokens:** Clean dark sidebar (`#1d2327`), light workspace canvas (`#f0f0f1`), white cards, and WooCommerce-inspired action blue (`#3858e9`).

### 2. Overview (Store Home)
- **KPI Metrics:** Today's / monthly sales revenue (₹), total orders, average order value (AOV), and low-stock murti alerts.
- **Operational Alerts:** Actionable items requiring owner attention (new unfulfilled orders, low stock, payment recovery).

### 3. Orders (Operations Center)
- **Order Queue:** Filterable list by status (`All`, `Pending payment`, `Processing`, `On hold`, `Dispatched`, `Completed`, `Cancelled`, `Refunded`), date range, and customer search.
- **Order Detail Drawer:** Complete item list, line prices, customer phone (+91), delivery address, PIN code, payment verification ID, and customer notes.
- **Status Lifecycle:** `Pending Payment` → `Processing` (Paid & packing) → `Dispatched` (Shipped) → `Completed` (Delivered) or `Cancelled` / `Refunded`.
- **Fulfillment & Tracking:** Private admin note for India Post / courier tracking number, visible on the customer's order tracking screen.

### 4. Products & Catalog
- **Murti Inventory Table:** Thumbnail, deity category, SKU, stock quantity with status pills (`In stock`, `Low stock`, `Out of stock`), regular price, and sale price.
- **Quick Price & Stock Edits:** Immediate inline changes synced to storefront via shared MySQL API.
- **Murti Product Editor:** Deity classification, description, idol dimensions (cm), weight (kg/g), material/finish, care guidelines, and 1–5 photo uploads.
- **Per-Product Detail Accordions (Amazon style):** Dynamic control to add, edit, reorder, or toggle collapsible sections (Dimensions, Craftsmanship, Care & Puja Guidelines, Shipping, Devotional Significance) per individual murti.
- **Truthful Pricing:** Enforces separate regular price and sale price (no artificial markups).

### 5. Customers & Purchase History
- **Customer Table:** Buyer name, email, phone, registered date, total orders, lifetime value (LTV in ₹), and city/pincode.
- **Aggregates:** Total customer count, average orders per buyer, and average customer spend.
- **Purchase History:** Drill-down into all previous orders placed by a specific customer.

### 6. Coupons & Discounts
- **Coupon Manager:** Coupon code generation, discount type (`Percentage` or `Fixed cart discount`), discount value (₹ or %), and expiry date.
- **Validation Rules:** Minimum order spend, active/inactive toggle, and usage limits.
- **Storefront Checkout Sync:** Instant calculation and deduction during checkout quote.

### 7. Store Settings & Controls
- **Store Identity:** Legal business name, Maharashtra address, support WhatsApp (+91 88306 46308).
- **Site Visibility:** One-click toggle between "Store Coming Soon" and "Store Live".
- **Shipping Rules:** Free shipping threshold (e.g. above ₹999) and flat-rate delivery charges.
- **Store Announcement Bar:** Configurable banner text displayed at the top of the storefront.

---

## Access & Security Rules

- **Server-Enforced Authorization:** Every `/api/admin/*` route requires a secret `X-Admin-Token` header matching the server's `ADMIN_SECRET`.
- **Closed by Default:** Outside local development, unauthorized requests receive 403 Forbidden.
- **Payment Integrity:** Payment status is driven by server-verified Razorpay callbacks; the dashboard never allows manually falsifying payment verification.
- **Data Privacy:** Customer data visible only to the authenticated store owner for fulfillment purposes.

---

## Admin API Route Contracts (`kalacar-app`)

- `GET /api/admin/metrics` — Dashboard KPI summaries
- `GET /api/admin/orders` — Filtered order list
- `PATCH /api/admin/orders/[id]` — Order status and tracking note updates
- `GET /api/admin/customers` — Aggregated customer list and metrics
- `GET /api/admin/coupons` & `POST /api/admin/coupons` — Coupon CRUD
- `GET /api/admin/settings` & `PUT /api/admin/settings` — Store configuration
