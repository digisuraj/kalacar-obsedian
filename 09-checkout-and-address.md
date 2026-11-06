---
title: 09 — Checkout & Address (incl. current-location pick)
tags: [ecom, checkout, address, geolocation]
status: planning
---

# 09 — Checkout & Address

← [[08-cart-and-coupons]] · next → [[10-razorpay-payments]]

Layout `(checkout)`: minimal header (logo, "🔒 Secure checkout", back-to-cart link), no nav/footer clutter, no announcement bar, no WhatsApp float over the pay bar.

## 1. Entry & guards

- Entry: `/checkout` (from cart) or `/checkout?mode=buynow` (single line from `sessionStorage buynow:v1`).
- Guards: empty source → redirect `/cart`; unavailable lines → block with "Remove unavailable items"; Backend API unavailable → "Checkout temporarily unavailable".
- Logged-in → prefill name/email/phone + **saved addresses**; guest → optional "Have an account? Log in" (returns to checkout with state preserved).
- **One page, accordion steps** (mobile) / two columns (desktop: form left, sticky summary right):
  1. Contact  2. Shipping address  3. Delivery  4. Review & Pay
- Mobile: collapsed **order summary** at top ("Show order summary ▾ ₹3,597"), and a **sticky pay bar** at bottom (total + "Pay ₹3,597").

## 2. Contact

| Field | Rules | Attributes |
|---|---|---|
| Email | required, RFC-lite regex, trim, lowercase; typo hints (gmial.com → "Did you mean gmail.com?") | `type=email`, `autocomplete=email`, `inputmode=email` |
| Mobile | required; strip spaces/`+91`/leading 0; must match `^[6-9]\d{9}$`; fixed "+91" prefix chip | `type=tel`, `inputmode=numeric`, `autocomplete=tel-national`, `maxlength=10` |
| WhatsApp/SMS updates opt-in | checkbox (v1.1) | — |

Email is mandatory (order emails). Phone mandatory (couriers need it).

## 3. Shipping address — field by field

Order matters: **Pincode first** (drives autofill), then the rest.

| # | Field | Rules | HTML attrs |
|---|---|---|---|
| 1 | Full name | required, 2–60 chars, letters/space/`.'-`; trim; auto-capitalise | `autocomplete=name` |
| 2 | **Pincode** | 6 digits, first digit 1–9; on 6th digit → `/api/pincode/{pin}` | `inputmode=numeric`, `autocomplete=postal-code`, `maxlength=6` |
| 3 | City / District | autofilled from pincode dataset; editable; required | `autocomplete=address-level2` |
| 4 | State | `<select>` of India states (from the backend state dataset/API, single source of truth); autofilled; required | `autocomplete=address-level1` |
| 5 | House / Flat / Building | required, ≤ 120 | `autocomplete=address-line1` |
| 6 | Area / Street / Locality | required, ≤ 120 | `autocomplete=address-line2` |
| 7 | Landmark | optional, ≤ 80 ("Near Shivaji Chowk") | `autocomplete=off` |
| 8 | Address type | chips Home / Work / Other (default Home) — helps couriers with delivery timing | — |
| 9 | Country | fixed "India" (read-only) | — |
| 10 | Delivery instructions / gift note | optional ≤ 200; "This is a gift" toggle adds gift-message ≤ 150 & hides prices in packing slip (v1.1) | — |

Form UX details
- [ ] Mobile font-size ≥ 16 px (prevents iOS zoom); numeric keypads for pincode/phone; `enterkeyhint="next"` and last field `done`
- [ ] Inline validation on **blur** (not on every keystroke); error text under field; on submit → scroll to & focus first invalid field + error summary for screen readers
- [ ] Never clear fields on error; trim & normalise on blur
- [ ] Paste handling: strip non-digits in pincode/phone
- [ ] Browser autofill works (correct `autocomplete` tokens); Chrome "Save address" prompt not blocked
- [ ] Draft persisted to `sessionStorage` (`checkout-draft:v1`, **no payment data exists anyway**) and restored on refresh/back
- [ ] Prevent accidental double submit (disable button + spinner; `isSubmitting` lock)
- [ ] Tab order logical; labels visible (no placeholder-only labels)
- [ ] Spell-check off for name/pincode/phone (`spellCheck={false}`)
- [ ] Transliteration friendliness: allow Devanagari/other Unicode letters in name & address (don't over-restrict to ASCII); courier label text is handled by admin
- [ ] "Use shipping address as billing" checked by default; unchecking reveals billing form (same fields). GSTIN field under "Business purchase? (GST invoice)" (optional): regex `^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$`, uppercase, + Legal/Business name

## 4. Pincode → autofill & serviceability

1. On valid pincode: `GET /api/pincode/{pin}` (debounced; cached).
2. Result `serviceable:true` → fill City + State (only if empty or previously autofilled — **never overwrite user edits**), show "✓ Delivery by Thu 6 Nov – Sat 8 Nov".
3. `serviceable:false` → inline "We don't deliver to this pincode yet"; block submission until changed.
4. Unknown pincode (not in dataset) → allow manual city/state, warn "We couldn't verify this pincode", and flag order for manual check.
5. Changing pincode later re-runs quote (ETA/shipping) and clears autofilled city/state if they no longer match.
6. Save valid pincode to `pin:v1` (shared with PDP checker).

## 5. Saved addresses (logged-in)

- Card list (radio): name, full address, phone, type chip, **Default** badge; selected card highlighted. First load: default address preselected.
- Actions: Edit (sheet), Delete (confirm), "Add new address" (sheet with same form), "Set as default".
- Limit 10 addresses. Stored in the backend address table via `/api/me/addresses`.
- "Save this address for next time" checkbox on new address (default on for logged-in).
- Editing an address used by an old order never alters that order (orders store a snapshot).
- Guests: no saved list; offer **"Create account after payment"** on success page.

## 6. "Use my current location" — full flow

**Where:** button at top of address section (crosshair icon): "📍 Use my current location". Also on PDP pincode checker (pincode only), and in the add/edit address sheet.

**Pre-checks (render-time)**
- Hide/disable if `!('geolocation' in navigator)` or `!window.isSecureContext` (needs HTTPS).
- If browser location permission is unavailable or denied, show a short message and keep manual address/pincode entry usable.

**Click handler**
1. If `navigator.permissions?.query({name:'geolocation'})` supported and state is `denied` → don't call the API; show help sheet (how to re-enable in Chrome/Safari settings: site settings → Location → Allow; iOS: Settings → Privacy → Location Services → Safari Websites). Wrap `permissions.query` in try/catch (older Safari throws).
2. Show inline loading "Finding your location…" with **Cancel**; button disabled.
3. `navigator.geolocation.getCurrentPosition(ok, err, { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 })`.
4. **Validate**: lat 6–38, lng 68–98 (India box) else "We deliver within India only — enter your address manually". Capture `coords.accuracy` (metres).
5. `POST /api/geo/reverse { lat, lng }` → server:
   - validates numeric ranges, rate-limits (10/min/IP), checks `Origin`.
   - calls Google **Geocoding API** reverse (`latlng`, `result_type=street_address|premise|route|sublocality|locality|postal_code`, `language=en`, `region=in`) using server key restricted to Geocoding API; sets timeout 6 s.
   - parses best result's `address_components` → `{ pincode: postal_code, city: locality || administrative_area_level_3 || administrative_area_level_2, stateName: administrative_area_level_1, area: [sublocality_level_2, sublocality_level_1, neighborhood, route].join(', '), premise: premise/street_number/subpremise, formatted }`, maps `stateName` → the project’s standard Indian state code.
   - returns `{ok, data:{pincode, city, stateCode, area, formatted, accuracyHint}}`; **does not log or store coordinates**.
6. **Fill** pincode, city, state, area (only empty or previously-autofilled fields). Leave **House/Flat blank** and **focus it** — GPS can't know flat numbers. Show dismissible banner: "We found: *{formatted}*. Please add your house/flat number."
7. Autofilled fields get a subtle highlight + small "from location" tag that disappears on edit.
8. Run the **pincode serviceability** check (§4) on the geocoded pincode.
9. If `coords.accuracy > 1000` → warning chip "Approximate location — please verify your pincode and area".
10. Do not add analytics tracking for the location lookup.

**Error matrix**
| Cause | UX |
|---|---|
| `PERMISSION_DENIED (1)` | Help sheet (above) + "Enter pincode instead" |
| `POSITION_UNAVAILABLE (2)` | "Couldn't detect your location. Check GPS/Wi-Fi or enter manually." |
| `TIMEOUT (3)` | "Taking too long. Try again or enter manually." + Retry |
| Geocode 4xx/5xx/ZERO_RESULTS | "Couldn't fetch your address. Enter pincode—we'll fill the rest." (pincode from coords is a bonus; manual path always works) |
| Outside India | message above; fields untouched |
| Rate limited | "Please wait a moment and try again" |

**Privacy & compliance**
- Location read **only on explicit tap**, never on page load.
- Coordinates exist only in memory and the single server request; do not persist or log them.
- Helper text under button: "Used only to fill your address."
- Privacy Policy lists geolocation + Google Geocoding as a processor ([[13-static-pages-and-legal]]).
- Google Maps Platform ToS: don't cache/store geocoding results beyond permitted limits; storing the *user-confirmed address* in the order is fine `[verify current terms]`.

**v1.1 enhancements**
- **Confirm on map**: small Google Map with **draggable pin** (Maps JS, referrer-restricted browser key, lazy-loaded) → on drag end re-geocode → refill. Keep optional (cost + JS weight).
- **Places Autocomplete (New)** for address line search, `includedRegionCodes:['in']`, **session tokens**, fields limited to `addressComponents,formattedAddress` (cost control). Behind flag `placesAutocomplete` with daily quota + budget alerts; fallback to manual entry if quota exceeded. Alternatives if cost matters: Ola Maps / Mappls APIs.

## 7. Delivery step
- Shows method "Free shipping" + ETA range from pincode result + dispatch-cutoff text.
- (v1.1) multiple methods (Standard/Express) from quote `shipping.options`.

## 8. Review & Pay

- Order summary (lines, coupon, totals — from latest quote; **re-quoted** after address/pincode change).
- Coupon field (collapsed) — same component as cart.
- Consent line: "By placing your order you agree to our Terms, Refund Policy & Privacy Policy" (links, `target=_blank`). Not a pre-ticked marketing opt-in (DPDP-friendly).
- **Pay ₹3,597** button (primary, full width), lock icon, "Secured by Razorpay · UPI, Cards, Netbanking, Wallets". No fake "only X left" elements here.
- Payment methods are chosen **inside Razorpay's modal** (nothing sensitive in our DOM).

## 9. Submit sequence (client)

1. Validate form (zod) → focus first error.
2. `POST /api/checkout` `{ lines, coupon, quote_hash, contact, shipping, billing, gstin?, notes, idempotency_key }` → custom backend re-quotes; if total ≠ `quote_hash` total → `409 PRICE_CHANGED` (show diff dialog, require re-confirm).
3. Response `{order_id, order_key, total_paise}` (order `pending`, stock reduced).
4. `POST /api/checkout/intent {order_id, order_key}` → `{key_id, rzp_order_id, amount, prefill}`.
5. Lazy-load Razorpay `checkout.js` (only on this page) and open modal ([[10-razorpay-payments]]).
6. Success handler → `POST /api/checkout/verify` → navigate `/order/{id}/success?key=…`.
7. Dismiss/failure → stay on page; show "Payment not completed — your items are reserved for 30 minutes" + **Retry payment** (re-uses same order/intent).

`idempotency_key` = SHA-256(cart lines + email + pincode) → same key within 15 min reuses the pending order (prevents duplicates from double taps/refreshes).

## 10. Edge cases

| Case | Handling |
|---|---|
| Refresh mid-checkout | Draft restored; if a pending order exists for the idempotency key → reuse |
| User changes cart in another tab | `storage` event → banner "Your cart changed" + re-quote; Pay disabled until reviewed |
| Item sells out during checkout | `/checkout` returns `409 OUT_OF_STOCK` with line detail → UI removes/adjusts and asks to review |
| Back button from Razorpay | Modal closes, page intact |
| Slow network | Pay button shows progress; requests have 15 s timeout + retry guidance |
| Autofill filled wrong state | Pincode wins; mismatch warning "Pincode 412403 belongs to Maharashtra" |
| Very long address | Truncation rules for courier label handled admin-side; storefront keeps full text |
| Guest with existing account email | Soft prompt "You have an account — log in to use saved addresses" (don't block) |
| Autofill & select state mismatch | Normalise state names (case-insensitive, handle "Orissa/Odisha", "Pondicherry/Puducherry", "Uttaranchal/Uttarakhand") |
| Screen reader | Errors announced via `role="alert"`; step headings are buttons with `aria-expanded` |

## 11. Acceptance criteria
- [ ] Typing a valid Maharashtra pincode fills city+state and shows ETA within 500 ms (cached)
- [ ] "Use my location" (Chrome Android, Safari iOS) fills pincode/city/state/area and focuses House/Flat; denial path shows help, not a dead end
- [ ] Location permission failure leaves the manual address path usable
- [ ] Double-tap Pay creates exactly one WC order
- [ ] Totals shown on Pay button == amount in Razorpay modal
- [ ] Form passes keyboard-only and screen-reader walkthrough
