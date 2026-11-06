---
title: 08 — Cart, Coupons, and Order Quote
tags: [kalacar, cart, checkout, coupons]
status: active
updated: 2026-11-03
---

# 08 — Cart, Coupons, and Order Quote

← [[07-product-page]] · next → [[09-checkout-and-address]] · admin spec → [[18-woocommerce-parity-and-dashboard-spec]]

## Cart

Keep the cart focused and uncluttered: murti photo/name, deity category, quantity increment/decrement, line price, remove button, and order subtotal. On mobile, use a clean full-height drawer or dedicated bag page. Provide an empty-state screen with a link back to the devotional catalogue.

Store only product IDs, quantities, and applied coupon code in client state. The server fetches authoritative prices and stock levels directly from the database to compute the final order quote.

## Promotional Coupons (WooCommerce Parity)

Promotions are managed in the Owner Dashboard and validated authoritatively on the server during cart calculation and checkout:

1. **Discount Types:**
   - **Percentage Discount:** Deducts a percentage (e.g. 10%) from the eligible item subtotal.
   - **Fixed Cart Discount:** Deducts a flat rupee amount (e.g. ₹100) from the cart total.
2. **Validation Rules (Enforced by Server API):**
   - Active status check (`is_active = 1`).
   - Expiration date verification (`expiry_date >= CURDATE()`).
   - Minimum spend requirement (e.g. valid only for orders above ₹999).
   - Usage limits (maximum total redemptions or per-user redemptions).
3. **Truthful Pricing:**
   - Discounts apply against actual regular/sale prices.
   - Transparently show `Subtotal`, `Discount (-₹...)`, `Delivery`, and `Final Total` before payment.

## Quote Rules

- Money is handled in integer paise and rendered in Indian Rupee format (`₹`, comma separated).
- Re-check stock and recalculate discounts on the server at the moment of checkout.
- Free shipping applies automatically when the subtotal meets the threshold set in Store Settings (e.g. ₹999).
- Idempotent checkout prevents duplicate Razorpay orders from repeated clicks.
