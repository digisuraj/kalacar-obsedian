---
title: 18 — WooCommerce Parity and Dashboard Specification
tags: [kalacar, woocommerce, parity, dashboard, admin, spec]
status: active
created: 2026-11-03
---

# 18 — WooCommerce Parity and Dashboard Specification

## Purpose & Strategy

This document establishes the exact feature parity specification between the previous WooCommerce store (`kalacar.in` on WooCommerce 11.2.1 / Hostinger) and the custom Next.js + React dashboard (`kalacar-dashboard` + `kalacar-app`).

### Work-Reduction Strategy ("Build Less, Achieve Parity")
To avoid hundreds of hours of redundant development:
1. **Unified Component Architecture:** All dashboard sections (Orders, Products, Customers, Coupons, Settings) share a single reusable `DataTable`, `StatusChip`, `ModalDrawer`, and `FormControls` design system matching WooCommerce's clean light-canvas aesthetic (`#f0f0f1` canvas, `#1d2327` sidebar, `#3858e9` blue actions).
2. **Derived Database Queries:** Customers and Overview KPIs require no new database tables; they are dynamically derived via SQL aggregations from the existing `kalacar_orders` and `kalacar_products` tables.
3. **Key-Value Store for Settings:** A single lightweight `kalacar_settings` key-value table powers Store Address, Currency, Shipping thresholds, Store Announcement banner, and Site Visibility.
4. **Ruthless De-bloating:** Dropped all WordPress/WooCommerce plugin bloat: LiteSpeed cache controls, Hostinger AI text generators, Printful marketplace ads, and third-party extension upsells.

---

## Module Breakdown & Parity Mapping

### 0. Global Shell & Navigation
| WooCommerce Feature | Kalacar React Implementation | Status / Phase |
|---|---|---|
| Left sidebar navigation | Persistent dark sidebar (`#1d2327`) with active blue indicator (`#3858e9`), badges for unread orders/alerts, and collapsible icon rail. Nav items: **Overview (Home)**, **Orders**, **Products**, **Customers**, **Coupons**, **Settings**. | **Phase 1 (Core)** |
| Top admin bar | Slim top bar with store title, quick search (`Ctrl+K` command palette), and **Store Visibility Status Pill** (`Coming soon` / `Live`). | **Phase 1 (Core)** |
| Onboarding / Launch banner | Dismissable top banner highlighting pending launch tasks (e.g. "Connect Razorpay webhook", "Set store address"). | **Phase 2 (Enhancement)** |
| Floating assistant | **DROPPED** (WooCommerce/Hostinger AI bloat; not needed for store operations). | *Dropped* |

---

### 1. Home (Store Overview)
| WooCommerce Feature | Kalacar React Implementation | Status / Phase |
|---|---|---|
| Sales Summary / KPI Cards | 4 key metric cards: **Today's / Monthly Revenue (₹)**, **Total Orders**, **Average Order Value (AOV)**, and **Low Stock Murti Count**. Computed via `GET /api/admin/metrics`. | **Phase 1 (Core)** |
| Operations Inbox / Alerts | Notification panel showing actionable operational alerts: *New unfulfilled orders*, *Out-of-stock / low-stock murtis*, *Failed payment recovery events*. | **Phase 1 (Core)** |
| "Things to do next" Checklist | Interactive owner task list showing daily packing and fulfillment tasks. | **Phase 2 (Enhancement)** |

---

### 2. Orders (Operations Center)
> *"Daily operations center for idol packing, verification, and dispatch"*

| WooCommerce Feature | Kalacar React Implementation | Status / Phase |
|---|---|---|
| Orders List Table | Responsive table with columns: `Order ID`, `Date/Time`, `Customer`, `Items & Qty`, `Total (₹)`, `Payment Status`, `Fulfillment Status`. Stacked card view on mobile. | **Phase 1 (Core)** |
| Status Filter Tabs | Status tabs with live count pills: `All`, `Pending payment`, `Processing`, `On hold`, `Completed`, `Cancelled`, `Refunded`. | **Phase 1 (Core)** |
| Order Detail & Address View | Customer name, phone (+91), email, complete delivery address, PIN code, and customer-provided notes. Helper button: "Copy address" for courier slips. | **Phase 1 (Core)** |
| Status Actions & Transitions | Status selector updating order lifecycle: `Pending Payment` → `Processing` (Paid & packing) → `Dispatched` (Shipped) → `Completed` (Delivered) / `Cancelled` / `Refunded`. | **Phase 1 (Core)** |
| Tracking & Order Notes | Private admin fulfillment note (e.g. India Post / courier tracking ID) saved to the order and accessible to the customer order status screen. | **Phase 1 (Core)** |
| Manual / Admin Order Creation | Admin modal to create offline/phone orders (select customer, pick products, calculate total). | **Phase 2 (Enhancement)** |
| Refund Flow | Process partial or full refunds with recorded reason, automatic status update to `Refunded`, and optional inventory restock. | **Phase 2 (Enhancement)** |

---

### 3. Customers & Buyer History
> *"Saare buyers ki detail list, unki lifetime value, aur purchase history"*

| WooCommerce Feature | Kalacar React Implementation | Status / Phase |
|---|---|---|
| Customers Table | Columns: `Customer Name`, `Email`, `Phone`, `Date Registered`, `Total Orders`, `Lifetime Spend (₹)`, `AOV (₹)`, `City & PIN`. Sortable and searchable. | **Phase 1 (Core)** |
| Customer Aggregate Stats | Summary bar: Total customers, average order count, average customer lifetime value. | **Phase 1 (Core)** |
| Customer Purchase History | Detail drawer showing customer profile, saved addresses, and all historical orders with clickable links to Order details. | **Phase 2 (Enhancement)** |

---

### 4. Coupons & Promotions
> *"Marketing aur sales boost karne ke liye"*

| WooCommerce Feature | Kalacar React Implementation | Status / Phase |
|---|---|---|
| Coupons Table | Columns: `Coupon Code`, `Type`, `Amount (₹ or %)`, `Min Spend`, `Usage / Limit`, `Expiry Date`, `Status`. | **Phase 1 (Core)** |
| Coupon Creator / Editor | Form with **Coupon Code** (with "Generate Code" button), **Discount Type** (`Percentage discount` or `Fixed cart discount`), **Amount**, **Expiry Date**, and **Active Toggle**. | **Phase 1 (Core)** |
| Usage Restrictions & Limits | Optional rules: `Minimum Spend (₹)`, `Maximum Spend (₹)`, `Individual use only` (cannot combine), `Usage limit per coupon`, `Usage limit per customer`. | **Phase 2 (Enhancement)** |
| Storefront Integration | Cart & checkout quote endpoint validates coupon code against `kalacar_coupons`, recalculates line items, and deducts discount before Razorpay order creation. | **Phase 1 (Core)** |

---

### 5. Products (Catalog & Inventory)
> *"Tumhari current inventory ki puri list aur murti catalog"*

| WooCommerce Feature | Kalacar React Implementation | Status / Phase |
|---|---|---|
| All Products List | Table with thumbnail image, Murti Name, Deity, SKU, Stock status badge (`In stock`, `Low stock`, `Out of stock`), Regular Price (₹), Sale Price (₹), and Edit/Trash actions. Search and deity filters. | **Phase 1 (Core)** |
| Price & Stock Quick-Edit | Inline price and inventory editing with immediate sync to storefront catalogue (already partially implemented). | **Phase 1 (Core)** |
| Product Editor — Core Info | Murti title, deity category, detailed description, dimensions (H x W x D in cm), weight (kg/grams), material (e.g. Resin, Brass finish, PLA), care instructions. | **Phase 1 (Core)** |
| Multiple Product Images | Multi-image gallery (1–5 photos) with primary featured image selection (already implemented). | **Phase 1 (Core)** |
| Amazon-style Detail Accordions | Per-product dynamic builder in dashboard editor: owner can add, edit, reorder, or toggle collapsible accordions (Dimensions, Material & Craftsmanship, Care & Puja Guidelines, Packaging & Delivery, Devotional Story). Rendered on storefront with smooth expand/collapse and full keyboard/mobile accessibility. Stored as JSON array. | **Phase 1 (Core)** |
| Linked Products & Cross-sells | "Select below products to add together" bundle picker on product page; configured in dashboard product editor via companion product multi-select. | **Phase 1 (Core)** |
| Regular vs. Sale Price | Separate `regular_price` and `sale_price` inputs to ensure truthful discount presentation (no fake compare-at prices). | **Phase 1 (Core)** |
| Attributes & Variations | Murti variations for size (e.g. 6 inch, 9 inch, 12 inch) and finish (e.g. Matte Antique, Gold Bronze), with independent SKU and price. | **Phase 2 (Enhancement)** |
| Categories & Taxonomies | Deity categories (Ganpati, Krishna, Swami Samarth, Shiva, etc.) with dedicated category filter on storefront. | **Phase 1 (Core)** |
| CSV Catalog Import/Export | Bulk upload / export of product catalogue. | **Phase 2 (Enhancement)** |
| Dropped Bloat | **DROPPED:** Hostinger AI product generator, Printful print-on-demand cards, external image plugins. | *Dropped* |

---

### 6. Store Settings & Controls
> *"Store ka core engine"*

| WooCommerce Feature               | Kalacar React Implementation                                                                                                                                | Status / Phase            |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| General Store Details             | Shop legal name, business address (Maharashtra, India), owner WhatsApp/email, currency formatting (`₹`, INR, 2 decimals).                                   | **Phase 1 (Core)**        |
| Site Visibility Switch            | Global toggle: **Store Coming Soon / Maintenance Mode** vs. **Store Live**. When "Coming Soon", storefront displays a devotional teaser with launch signup. | **Phase 1 (Core)**        |
| Shipping Rules                    | Base delivery flat rate (₹), Free shipping threshold (e.g. "Free shipping on orders above ₹999"), and manual dispatch note.                                 | **Phase 1 (Core)**        |
| Payment Gateways                  | Razorpay status indicator (Test mode / Live mode), Cash on Delivery (COD) enable/disable toggle with min/max order limits.                                  | **Phase 1 (Core)**        |
| Store Announcement Topbar         | Storefront announcement strip (e.g. "Devotional festival offer — Free shipping on orders above ₹999") with enable toggle and customizable text.             | **Phase 1 (Core)**        |
| Customer Privacy & Guest Checkout | Allow guest checkout toggle, customer account policy, terms/privacy page links.                                                                             | **Phase 2 (Enhancement)** |
| Transactional Email Notifications | Order status update emails (New order confirmation, Dispatched with tracking, Cancelled/Refunded) via server mail provider.                                 | **Phase 2 (Enhancement)** |

---

## Technical Architecture & Database Contracts

### 1. Unified MySQL Schema Extensions
```sql
-- Store Settings Key-Value Store
CREATE TABLE IF NOT EXISTS kalacar_settings (
  setting_key VARCHAR(64) PRIMARY KEY,
  setting_value TEXT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Coupons Table
CREATE TABLE IF NOT EXISTS kalacar_coupons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(32) NOT NULL UNIQUE,
  discount_type ENUM('percentage', 'fixed_cart') NOT NULL DEFAULT 'percentage',
  amount DECIMAL(10, 2) NOT NULL,
  min_spend DECIMAL(10, 2) DEFAULT 0,
  max_spend DECIMAL(10, 2) DEFAULT NULL,
  usage_limit INT DEFAULT NULL,
  usage_count INT DEFAULT 0,
  expiry_date DATE DEFAULT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Table Parity Fields (added to kalacar_products)
-- regular_price DECIMAL(10, 2), sale_price DECIMAL(10, 2), sku VARCHAR(64),
-- category VARCHAR(64), weight_kg DECIMAL(5, 2), dimensions_cm VARCHAR(64),
-- accordions JSON DEFAULT NULL, -- Array of { id, title, content, is_default_open }
-- is_published BOOLEAN DEFAULT TRUE;

-- Order Table Parity Fields (in kalacar_orders)
-- status ENUM('pending', 'processing', 'on_hold', 'dispatched', 'completed', 'cancelled', 'refunded'),
-- coupon_code VARCHAR(32), discount_amount DECIMAL(10, 2), tracking_number VARCHAR(128),
-- admin_notes TEXT, refund_reason TEXT;
```

### 2. Core API Endpoints (`kalacar-app/src/app/api/admin/*`)
- `GET /api/admin/metrics` — Dashboard KPI numbers (Revenue, Orders, AOV, Low stock)
- `GET /api/admin/orders` — Orders list with filters (`status`, `search`, `page`)
- `PATCH /api/admin/orders/[id]` — Update fulfillment status, tracking note, or refund status
- `GET /api/admin/customers` — Derived customer list with order counts and lifetime spend
- `GET /api/admin/coupons` & `POST /api/admin/coupons` — Coupon CRUD
- `GET /api/admin/settings` & `PUT /api/admin/settings` — Get and update store settings
