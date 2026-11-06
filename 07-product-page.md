---
title: 07 — Product Page & Detail Accordions Specification
tags: [kalacar, product, accordions, storefront, spec]
status: active
updated: 2026-11-03
---

# 07 — Product Page & Detail Accordions Specification

← [[04-frontend-foundation]] · next → [[08-cart-and-coupons]] · dashboard spec → [[18-woocommerce-parity-and-dashboard-spec]]

Route: `/products/[slug]`. Keep one consistent image ratio, fast-loading product photos, and a mobile-first devotional layout.

---

## 1. Amazon-Style Product Detail Accordions (Per-Product Controlled)

### Purpose & User Experience
Just like Amazon's product detail experience, deep product specifications and devotional information are presented in collapsible, mobile-optimized accordion cards ("See more details") below the primary buy box. This keeps the page clean and scannable while allowing buyers to inspect dimensions, materials, craftsmanship, and devotional care.

Crucially, **these accordions are dynamic and controlled per individual product through the owner dashboard.** Different murtis can have custom tabs, custom text, or specific puja instructions without writing new code.

### Data Model & Type Definitions
Stored as a `JSON` column in MySQL (`kalacar_products.accordions`):

```typescript
export interface ProductAccordion {
  id: string;              // e.g. "dimensions", "material", "care", "delivery", "story"
  title: string;           // e.g. "Dimensions & Weight", "Material & Finish"
  content: string;         // Paragraph text, or newline-separated `Label: value` rows
  format?: "rows" | "text"; // Older records infer the format from their content
  defaultOpen?: boolean;   // true if this accordion should be expanded by default (e.g. Dimensions)
  displayOrder: number;    // Numeric order (1, 2, 3...)
  isActive: boolean;       // Enable/disable toggle for this product
}
```

### Standard Default Sections (Configurable in Dashboard)
1. **Dimensions & Weight:**
   - Exact height, width, depth (cm), and weight (grams).
   - Placement suitability (e.g. "Perfect for car dashboards, Devghar, or study desks").
2. **Material & Finish:**
   - 3D precision printed devotional idol, premium resin / high-density biopolymer blend.
   - Antique matte gold, stone finish, or hand-painted details.
3. **Care & Puja Guidelines:**
   - Gently wipe with a soft, clean dry cloth.
   - Water / abhishek suitability notice.
4. **Packaging & Delivery:**
   - Safe, multi-layered shock-absorbing protective box.
   - Dispatched within 24–48 hours via India Post / standard courier.
5. **Devotional Significance / Iconography:**
   - Deity background, blessings, and traditional symbolism.

---

## 2. Implementation Blueprint

### A. Storefront Client Component (`kalacar-app/src/components/product-detail-accordions.tsx`)
```tsx
"use client";
import { useState } from "react";
import type { ProductAccordion } from "@/data/catalogue";

export function ProductDetailAccordions({ items }: { items?: ProductAccordion[] }) {
  if (!items || items.length === 0) return null;
  
  const activeItems = items.filter(item => item.isActive).sort((a, b) => a.displayOrder - b.displayOrder);
  const [openIds, setOpenIds] = useState<string[]>(
    () => activeItems.filter(item => item.defaultOpen).map(item => item.id)
  );

  const toggle = (id: string) => {
    setOpenIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  };

  return (
    <div className="product-accordions" aria-label="Product details and specifications">
      {activeItems.map(item => {
        const isOpen = openIds.includes(item.id);
        return (
          <div key={item.id} className={`accordion-item ${isOpen ? "open" : ""}`}>
            <button
              type="button"
              className="accordion-trigger"
              onClick={() => toggle(item.id)}
              aria-expanded={isOpen}
              aria-controls={`accordion-body-${item.id}`}
            >
              <span className="accordion-title">{item.title}</span>
              <span className="accordion-icon" aria-hidden="true">{isOpen ? "−" : "+"}</span>
            </button>
            {isOpen && (
              <div id={`accordion-body-${item.id}`} className="accordion-content">
                <p className="accordion-text">{item.content}</p>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
```

### B. Dashboard Product Editor Accordions Manager (`kalacar-dashboard`)
Inside `kalacar-dashboard/src/owner-dashboard.tsx` (Add/Edit Product form):
- **Accordion Row Controls:**
  - `Title` input (e.g. "Dimensions & Weight")
  - `Content` textarea (multiline specifications)
  - `Default Open` checkbox
  - `Active` toggle
  - `Reorder` up/down buttons
  - `Delete` button
- **Add Section Button:** `+ Add detail accordion`
- **One-click presets:** Pre-fill standard template (Dimensions, Material, Care, Packaging) with a single click.
- **Persistence:** Sent via `PATCH /api/admin/products/[id]` or `POST /api/admin/products` as a JSON string under the `accordions` key.

---

## 3. Supplementary High-Value Product Details (From Reference)

In addition to the Amazon-style accordions, the reference product detail architecture includes:

1. **Estimated Delivery / Pincode Checker:**
   - 6-digit Indian PIN code input with a "Check" button.
   - Validates format (`/^[1-9][0-9]{5}$/`) and displays estimated transit time (e.g., "Delivery in 3–5 business days to Maharashtra").
2. **Trust & Devotional Service Badges:**
   - Horizontal icon strip below CTA buttons:
     - 🚚 *Free Delivery Above ₹999*
     - 💵 *Cash on Delivery Available*
     - 💬 *Devotional Support via WhatsApp (+91 88306 46308)*
     - 🛡️ *Damage-Free Delivery Guarantee*
3. **Action Buttons:**
   - `Quantity` increment/decrement stepper (`- 1 +`).
   - `Add to Cart` (persists to cart drawer/bag).
   - `Buy Now` (adds to cart and navigates directly to `/cart` or checkout sheet).
4. **"Select Products to Add Together" (Cross-Sell Bundle):**
   - Recommended companion items (e.g., Ganpati Murti + Brass finish Diya or Velvet Aasan).
   - Checkbox selector with live combined price calculation and single-click "Add selected to bag".

---

## Acceptance Checks

- [x] Every individual product can store its own customized list of detail accordions.
- [x] Accordion items can be dynamically added, edited, reordered, toggled, and deleted in the dashboard; each section supports repeatable key/value rows or paragraph text.
- [x] Storefront renders active accordions with keyboard-accessible native disclosure controls.
- [x] No empty accordion items appear if none are configured.
- [ ] Mobile-first responsive styling with large touch-friendly trigger bars.
