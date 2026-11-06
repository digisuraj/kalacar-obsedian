#!/usr/bin/env python3
"""
Kalacar flow drawings — the single source for every flow diagram in this vault.

Each flow below is plain data: nodes on a grid and arrows between them. Running this script
rebuilds every `flows/*.excalidraw.md` file (opened by the Obsidian Excalidraw plugin) and a
plain `.excalidraw` copy in `flows/excalidraw/` (opens on excalidraw.com).

    python3 flows/build_flows.py        # run from the vault folder

When a feature's flow is added or changed: edit its FLOWS entry here, rebuild, and update
[[19-how-kalacar-works]]. Do not hand-edit the generated files — they are overwritten.

Node kinds: start, step, server, decision, good, bad, owner, data, note.
Node: (key, col, row, label, kind).  Edge: (from, to, label, style)  style: "" | "dashed".
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = {  # background, stroke
    "start": ("#d0ebff", "#1971c2"), "step": ("#ffffff", "#1e1e1e"), "server": ("#fff3bf", "#e67700"),
    "decision": ("#fff9db", "#e67700"), "good": ("#d3f9d8", "#2b8a3e"), "bad": ("#ffe3e3", "#c92a2a"),
    "owner": ("#e6fcf5", "#0c8599"), "data": ("#f3f0ff", "#5f3dc4"), "note": ("transparent", "#868e96"),
}
CELL_W, CELL_H, BOX_W, BOX_H = 280, 170, 220, 104

FLOWS = [
 {"file": "01-customer-journey", "title": "Customer journey — from browsing to the order in Account",
  "intro": "What a customer does while the shop is Live. On Coming soon, customers see a simple page and can't place new orders; Account and policy pages stay open.",
  "nodes": [
   ("home", 0, 0, "Home / catalogue: photo,\nbadge, colours, 'from ₹';\nfooter links to 5 policies", "start"),
   ("product", 1, 0, "Product page\nphotos · tagline · Save %\nhighlights · spec cards", "step"),
   ("colour", 2, 0, "Choose colour\nphotos + price + stock\nswap; link ?colour=…", "step"),
   ("stock", 3, 0, "In stock?", "decision"),
   ("soldout", 3, 1, "'Sold out — try\nanother colour'\nbuttons disabled", "bad"),
   ("add", 4, 0, "Add to bag opens the\nquick drawer; Buy now\ngoes to the bag page.\nOff when bag holds all stock", "step"),
   ("bag", 5, 0, "Bag (kept in browser):\ndrawer and bag page show\nthe same items; change\ncolour / qty up to stock", "step"),
   ("extras", 5, 1, "Proceed to the big bag\npage: gift packaging tick,\ncoupon preview", "step"),
   ("signed", 5, 2, "Signed in?", "decision"),
   ("signin", 4, 2, "Sign in: Google first,\nemail if chosen; returns\nto the bag page", "step"),
   ("address", 5, 3, "Delivery address: saved\nor new; PIN fills city +\nstate; policy links by Pay", "step"),
   ("pay", 4, 3, "Pay → server checks\neverything again\n(see Checkout flow)", "server"),
   ("rzp", 3, 3, "Razorpay window\n(test mode)", "start"),
   ("done", 2, 3, "Order confirmed: items,\ntotal, address, next steps;\nbag cleared", "good"),
   ("account", 1, 3, "Account & orders\nstatus · colour · gift\ncoupon · tracking · refund", "good"),
   ("recs", 1, 1, "Recommended murtis\n(same category first, max 4)", "note"),
  ],
  "edges": [("home","product",""),("product","colour",""),("colour","stock",""),("stock","soldout","no"),("stock","add","yes"),
            ("add","bag",""),("bag","extras",""),("extras","signed",""),("signed","signin","no"),
            ("signed","address","yes"),("address","pay",""),("pay","rzp",""),("rzp","done","paid"),("done","account",""),
            ("product","recs","","dashed")]},

 {"file": "02-checkout-and-payment", "title": "Checkout and payment — what the server does when Pay is pressed",
  "intro": "The browser's prices are only a preview; the server decides the total. All of steps 2–6 are one locked step.",
  "nodes": [
   ("pay", 0, 0, "1 · Customer presses Pay\nitems + colours, gift?,\ncoupon?, address", "start"),
   ("gate", 1, 0, "Signed in? not too many\ntries? items and\naddress valid?", "decision"),
   ("refuse", 1, 1, "Refused with a reason\nnothing reserved", "bad"),
   ("lock", 2, 0, "2 · Lock each colour\n(fixed order, so two\ncheckouts can't deadlock)", "server"),
   ("enough", 3, 0, "3 · Enough stock\nfor every line?", "decision"),
   ("nostock", 3, 1, "'Not enough stock'\nnothing charged", "bad"),
   ("coupon", 4, 0, "4 · Coupon? lock + check\n(dates, min spend,\nuses, once each)", "server"),
   ("badcoupon", 4, 1, "Coupon no longer valid\nnothing reserved; bag\nremoves it + explains", "bad"),
   ("total", 5, 0, "5 · Total = murtis\n− discount + gift\n(never below ₹1)", "server"),
   ("save", 5, 1, "6 · Save order\n'Awaiting payment'\ntake the stock", "server"),
   ("rzporder", 5, 2, "7 · Ask Razorpay to\ncreate a payment for\nthe server's total", "server"),
   ("setupfail", 4, 2, "Razorpay failed →\n'Payment setup failed'\nstock + coupon returned", "bad"),
   ("window", 5, 3, "8 · Razorpay window\ncustomer pays", "start"),
   ("verify", 4, 3, "9 · Browser sends payment\nproof → server checks the\nRazorpay signature", "server"),
   ("paid", 3, 3, "Order PAID\n(never marked paid\nby hand)", "good"),
   ("webhook", 2, 3, "Razorpay webhook: confirms\nor fails (inactive until\nits secret is set)", "server"),
   ("failed", 3, 4, "Payment failed\n→ can retry\n(see Retry flow)", "bad"),
   ("closed", 4, 4, "Window closed →\nserver asks Razorpay\nfor the real status", "server"),
  ],
  "edges": [("pay","gate",""),("gate","refuse","no"),("gate","lock","yes"),("lock","enough",""),("enough","nostock","no"),
            ("enough","coupon","yes"),("coupon","badcoupon","invalid"),("coupon","total","ok / none"),("total","save",""),
            ("save","rzporder",""),("rzporder","setupfail","error"),("rzporder","window","ok"),("window","verify","paid"),
            ("verify","paid","valid"),("webhook","paid","captured","dashed"),("webhook","failed","failed","dashed"),
            ("window","closed","closed","dashed"),("closed","paid","if paid","dashed")]},

 {"file": "03-payment-retry-and-recovery", "title": "Payment retry and recovery — failed, abandoned, cancelled, late",
  "intro": "Every unpaid order ends in one of these paths. Stock and coupon uses always return exactly once.",
  "nodes": [
   ("pending", 0, 1, "Awaiting payment\n(stock + coupon held)", "start"),
   ("failedp", 1, 0, "Payment failed\n(card declined etc.)", "bad"),
   ("retry", 2, 0, "Retry (bag or Account)\nServer asks Razorpay first:\nreopens only if failed or\nno payment attempt", "server"),
   ("reopen", 3, 0, "Razorpay window\nopens again\n(same order, same total)", "start"),
   ("paid", 4, 0, "Paid", "good"),
   ("retrystop", 3, 1, "Not reopened if already\npaid, still processing,\nor status unreachable", "bad"),
   ("bagmem", 1, 1, "Bag page shows the unpaid\norder: Retry or Check,\nnot a second order", "step"),
   ("sync", 2, 1, "Server asks Razorpay\nfor the real status", "server"),
   ("cancel", 1, 2, "Owner cancels unpaid\norder (reason)", "owner"),
   ("cancelled", 2, 2, "Cancelled\nstock returned once\ncoupon use returned", "bad"),
   ("late", 3, 2, "Payment arrives after\ncancel → 'Paid after\ncancel' (On hold)", "bad"),
   ("refund", 4, 2, "Owner refunds in\nRazorpay, then records\nthe refund here", "owner"),
   ("refunded", 4, 1, "Refunded\n(never becomes\npaid again)", "good"),
  ],
  "edges": [("pending","failedp","fails"),("failedp","retry",""),("retry","reopen","ok"),("retry","retrystop","stop"),("reopen","paid","pays"),
            ("pending","bagmem","window closed"),("bagmem","sync",""),("sync","paid","already paid","dashed"),
            ("pending","cancel",""),("cancel","cancelled",""),("cancelled","late","money arrives"),("late","refund",""),
            ("refund","refunded","")]},

 {"file": "04-order-lifecycle-owner", "title": "Order lifecycle — what the owner does in Dashboard → Orders",
  "intro": "Paid orders have a delivery status dropdown: nothing changes until Save. The customer sees saved changes in Account & orders.",
  "nodes": [
   ("paid", 0, 0, "New PAID order\n(inbox: awaiting\nfulfilment)", "start"),
   ("open", 1, 0, "Open order details\nitems + colours, gift,\ncoupon, address", "owner"),
   ("prepare", 2, 0, "Preparing\n(packing)", "owner"),
   ("dispatch", 3, 0, "Dispatched\n(handed to courier)", "owner"),
   ("complete", 4, 0, "Completed\n(delivered)", "good"),
   ("print", 1, 1, "Print label: browser print\nwindow, top half of A4;\nwording set in Settings", "note"),
   ("rule", 3, 1, "Any status can be chosen,\nincluding going back. Highlighted\nuntil Save; refused if the\norder changed meanwhile", "note"),
   ("tracking", 2, 1, "Courier + tracking ID\n(Trackon or India Post),\noptional note; customer\nsees it and can track", "owner"),
   ("message", 0, 1, "After Save: WhatsApp, SMS,\nEmail open from the status's\nSettings template; owner\npresses Send. Call dials", "note"),
   ("refundq", 1, 2, "Need to refund?", "decision"),
   ("refundform", 2, 2, "Record refund: amount\n≤ paid, reason, Razorpay\nreference", "owner"),
   ("restock", 3, 2, "Return stock?\nonly allowed before\ndispatch", "decision"),
   ("refunded", 4, 2, "Refunded\ncustomer sees amount", "good"),
   ("customer", 4, 1, "Customer: Account &\norders shows progress,\ntracking, refund", "step"),
  ],
  "edges": [("paid","open",""),("open","prepare",""),("prepare","dispatch",""),("dispatch","complete",""),
            ("open","tracking","","dashed"),("tracking","customer","","dashed"),("open","refundq",""),("refundq","refundform","yes"),
            ("refundform","restock",""),("restock","refunded",""),("complete","customer","","dashed")]},

 {"file": "05-product-create-and-edit", "title": "Products — creating, editing, quick stock/price saves, deleting",
  "intro": "Everything the shop shows about a murti comes from here. Each colour has its own photos, price and stock.",
  "nodes": [
   ("new", 0, 0, "Add product\n(or Edit details)", "start"),
   ("basics", 1, 0, "Basics: name, category\n(from Settings),\nbadge (≤ 40), tagline\n(≤ 120), placement", "owner"),
   ("colours", 2, 0, "Colours (1–8): name,\nswatch, price, regular\nprice, stock, ≤ 5 photos", "owner"),
   ("facts", 3, 0, "Specs (≤ 8, 'Add common')\nhighlights (≤ 6)\ninfo sections", "owner"),
   ("save", 4, 0, "Save → server checks\nlimits, real image bytes,\nprice ≥ ₹1", "server"),
   ("bad", 4, 1, "Clear error\nnothing saved", "bad"),
   ("shop", 5, 1, "Live in the shop\n(if a colour is visible)", "good"),
   ("quick", 0, 2, "Quick edit in list:\nchange price / stock\n(stepper)", "owner"),
   ("dirty", 1, 2, "Row highlighted,\nunsaved count in menu;\nUndo available", "step"),
   ("rowsave", 2, 2, "Save this row only", "owner"),
   ("same", 3, 2, "Still the value you\nsaw? (no sale or other\nedit meanwhile)", "decision"),
   ("conflict", 3, 3, "Shows the new value;\nyour typed value kept\n— no lost sales", "bad"),
   ("saved", 4, 2, "Saved for that\ncolour only", "good"),
   ("delete", 0, 4, "Delete product\n(danger zone, confirm)", "owner"),
   ("openorders", 1, 4, "Unfinished orders\nuse it?", "decision"),
   ("refuse", 2, 4, "Refused — finish or\ncancel those first", "bad"),
   ("deleted", 1, 5, "Deleted with its\ncolours (old orders keep\nname + colour + price)", "good"),
  ],
  "edges": [("new","basics",""),("basics","colours",""),("colours","facts",""),("facts","save",""),("save","bad","invalid"),
            ("save","shop","ok"),("quick","dirty",""),("dirty","rowsave",""),("rowsave","same",""),("same","conflict","no"),
            ("same","saved","yes"),("saved","shop","","dashed"),("delete","openorders",""),("openorders","refuse","yes"),("openorders","deleted","no")]},

 {"file": "06-coupons", "title": "Coupons — owner creates, customer applies, server decides",
  "intro": "Discount applies to murtis only. An unpaid order reserves a use; it counts as used only when payment succeeds. Cancel or setup failure releases it; refunds don't return it.",
  "nodes": [
   ("create", 0, 0, "Owner: New coupon\ncode (Generate), % or ₹,\nmax, min spend", "owner"),
   ("limits", 1, 0, "Total uses, once per\ncustomer (default on),\nstart / expiry (IST)", "owner"),
   ("switch", 2, 0, "Coupon on / off\n(used coupons can't be\ndeleted — switch off)", "owner"),
   ("type", 0, 1, "Customer: 'Have a\ncoupon?' types code", "start"),
   ("preview", 1, 1, "Server preview check\n(rate-limited against\nguessing)", "server"),
   ("why", 1, 2, "Says why: invalid · starts\n· expired · add ₹X more ·\nfully used · already used", "bad"),
   ("shown", 2, 1, "Discount line +\nnew total in bag", "good"),
   ("pay", 3, 1, "Pay → coupon locked +\nchecked again inside\nthe stock reservation", "server"),
   ("gone", 3, 2, "No longer valid →\nnothing charged,\ncoupon removed", "bad"),
   ("order", 4, 1, "Order saves coupon id,\ncode and discount;\nuse reserved, counted\nwhen payment succeeds", "good"),
   ("back", 4, 2, "Cancelled / setup failed\n→ reservation released\n(refund → not returned)", "note"),
  ],
  "edges": [("create","limits",""),("limits","switch",""),("type","preview",""),("preview","why","no"),("preview","shown","ok"),
            ("shown","pay",""),("pay","gone","no"),("pay","order","ok"),("order","back","","dashed"),("switch","preview","rules","dashed")]},

 {"file": "07-sign-in-and-account", "title": "Sign-in and account — two separate doors, saved addresses",
  "intro": "Separate websites, separate tickets. The dashboard's small server passes requests to the shop's server, so sign-in stays on the dashboard's own address.",
  "nodes": [
   ("shop", 0, 0, "Shop: Continue with Google\n(main) or 'Use email and\npassword instead'", "start"),
   ("google", 1, 0, "Google confirms a\nverified email\n(state + PKCE checked)", "server"),
   ("cticket", 2, 0, "Shop ticket\nkalacar_customer_session\n(7 days)", "data"),
   ("account", 3, 0, "Account: orders,\nsaved addresses,\nsign out (shop only)", "good"),
   ("addr", 4, 0, "Addresses: add / edit /\ndelete / default; PIN\nautofill; checkout can save", "step"),
   ("dash", 0, 2, "Dashboard: Continue\nwith Google\n(scope=owner)", "start"),
   ("google2", 1, 2, "Google confirms a\nverified email", "server"),
   ("owner", 2, 2, "Email on the owner\nlist (KALACAR_\nOWNER_EMAILS)?", "decision"),
   ("oticket", 3, 2, "Dashboard ticket\nkalacar_owner_session", "data"),
   ("dashboard", 4, 2, "Dashboard opens\nsign out (dashboard only)", "good"),
   ("no", 2, 3, "Refused: 'not a shop\nowner' — shop sign-in\nunchanged", "bad"),
   ("rule", 0, 1, "Only listed addresses can sign in with Google · shop ticket never opens the dashboard · separate state cookies and limits per site", "note"),
  ],
  "edges": [("shop","google",""),("google","cticket",""),("cticket","account",""),("account","addr",""),
            ("dash","google2",""),("google2","owner",""),("owner","oticket","yes"),("owner","no","no"),("oticket","dashboard","")]},

 {"file": "08-data-entities", "title": "What Kalacar stores — the main records and how they connect",
  "intro": "Database tables (MySQL). Arrows read 'has many'. Money is stored in whole rupees.",
  "nodes": [
   ("users", 0, 0, "USERS\nname · email · phone\nGoogle id · password hash", "data"),
   ("sessions", 0, 1, "SESSIONS\nscrambled ticket · expiry\n(shop or dashboard)", "data"),
   ("addresses", 1, 1, "ADDRESSES\nlabel · name · phone · PIN\ncity · state · default", "data"),
   ("orders", 2, 0, "ORDERS\nstatus · delivery status ·\ntotal · gift · coupon ·\ndiscount · refund · tracking", "data"),
   ("items", 3, 0, "ORDER ITEMS\nmurti + colour name\nprice paid · quantity", "data"),
   ("products", 4, 1, "PRODUCTS\nname · category · badge ·\ntagline · specs ·\nhighlights · info sections", "data"),
   ("variants", 3, 1, "COLOURS (variants)\nname · swatch · photos ·\nprice · regular price · stock", "data"),
   ("coupons", 2, 2, "COUPONS\ncode · % or ₹ · max ·\nmin spend · uses · dates", "data"),
   ("photos", 4, 0, "PHOTOS\nfile name · type · image\n(survive redeploys)", "data"),
   ("settings", 4, 2, "SETTINGS\ngift packaging:\non/off · price · text", "data"),
   ("webhooks", 3, 2, "PAYMENT EVENTS\nRazorpay webhook log\n(each event once)", "data"),
  ],
  "edges": [("users","sessions",""),("users","addresses",""),("users","orders",""),("orders","items",""),
            ("products","variants",""),("variants","photos","shows","dashed"),("variants","items","bought as","dashed"),("coupons","orders","used on","dashed"),
            ("webhooks","orders","updates","dashed")]},
]

def build(flow):
    random.seed(flow["file"])
    els, ids = [], {}
    counter = [0]
    def nid():
        counter[0] += 1
        return f"{flow['file'][:2]}e{counter[0]}"
    def base(kind, x, y, w, h, bg="transparent", stroke="#1e1e1e", **extra):
        e = {"id": nid(), "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": stroke,
             "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": extra.get("sw", 1), "strokeStyle": extra.get("style", "solid"),
             "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None, "roundness": extra.get("round", {"type": 3}),
             "seed": random.randint(1, 2**31), "version": 1, "versionNonce": random.randint(1, 2**31), "isDeleted": False,
             "boundElements": [], "updated": 1, "link": None, "locked": False}
        els.append(e)
        return e
    def text(x, y, w, h, s, size=15, container=None, align="center", color="#1e1e1e"):
        t = base("text", x, y, w, h, stroke=color, round=None)
        t.update({"text": s, "fontSize": size, "fontFamily": 1, "textAlign": align, "verticalAlign": "middle",
                  "containerId": container, "originalText": s, "lineHeight": 1.25, "baseline": int(size * .9), "autoResize": True})
        return t

    text(0, -130, 1600, 40, flow["title"], 28, align="left")
    text(0, -84, 1600, 24, flow["intro"], 16, align="left", color="#495057")
    for key, col, row, label, kind in flow["nodes"]:
        x, y = col * CELL_W, row * CELL_H
        bg, stroke = STYLE[kind]
        if kind == "note":
            ids[key] = text(x, y + 20, CELL_W * 3 if len(label) > 70 else BOX_W, 60, label, 13, align="left", color=stroke)
            continue
        shape = "diamond" if kind == "decision" else "ellipse" if kind == "start" and False else "rectangle"
        w, h = (BOX_W, BOX_H + 20) if shape == "diamond" else (BOX_W, BOX_H)
        b = base(shape, x, y, w, h, bg=bg, stroke=stroke, sw=2 if kind in ("server", "good", "bad") else 1)
        lines = label.count("\n") + 1
        t = text(x + 10, y + h / 2 - lines * 9.5, w - 20, lines * 19, label, 14 if shape == "diamond" else 15, container=b["id"])
        b["boundElements"].append({"id": t["id"], "type": "text"})
        ids[key] = b

    def side(a, b):
        ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
        bx, by = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
        if abs(by - ay) >= abs(bx - ax):
            return (ax, a["y"] + a["height"], bx, b["y"]) if by > ay else (ax, a["y"], bx, b["y"] + b["height"])
        return (a["x"] + a["width"], ay, b["x"], by) if bx > ax else (a["x"], ay, b["x"] + b["width"], by)

    for edge in flow["edges"]:
        src, dst, label = edge[0], edge[1], edge[2]
        dashed = len(edge) > 3 and edge[3] == "dashed"
        a, b = ids[src], ids[dst]
        x1, y1, x2, y2 = side(a, b)
        ar = base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1), stroke="#495057" if dashed else "#1e1e1e",
                  style="dashed" if dashed else "solid", round={"type": 2}, sw=2)
        ar.update({"points": [[0, 0], [x2 - x1, y2 - y1]], "lastCommittedPoint": None, "startArrowhead": None,
                   "endArrowhead": "arrow", "elbowed": False,
                   "startBinding": {"elementId": a["id"], "focus": 0, "gap": 4} if a["type"] != "text" else None,
                   "endBinding": {"elementId": b["id"], "focus": 0, "gap": 4} if b["type"] != "text" else None})
        if a["type"] != "text": a["boundElements"].append({"id": ar["id"], "type": "arrow"})
        if b["type"] != "text": b["boundElements"].append({"id": ar["id"], "type": "arrow"})
        if label:
            text((x1 + x2) / 2 + 6, (y1 + y2) / 2 - 20, 120, 18, label, 13, align="left", color="#846358")

    # Legend
    rows = max(n[2] for n in flow["nodes"]) + 1
    ly = rows * CELL_H + 10
    for i, (kind, name) in enumerate([("start", "customer / outside service"), ("step", "screen or step"), ("server", "server does this"),
                                      ("decision", "check / decision"), ("owner", "owner action"), ("good", "good outcome"), ("bad", "stopped / problem"), ("data", "stored record")]):
        bg, stroke = STYLE[kind]
        base("rectangle", i * 250, ly, 22, 22, bg=bg, stroke=stroke)
        text(i * 250 + 30, ly, 210, 22, name, 12, align="left", color="#495057")
    return {"type": "excalidraw", "version": 2, "source": "kalacar-flows", "elements": els,
            "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": {}}

def main():
    os.makedirs(os.path.join(HERE, "excalidraw"), exist_ok=True)
    for flow in FLOWS:
        scene = build(flow)
        with open(os.path.join(HERE, "excalidraw", flow["file"] + ".excalidraw"), "w") as f:
            json.dump(scene, f, ensure_ascii=False, indent=1)
        texts = "\n".join(f"{e['text'].replace(chr(10), ' ')} ^{e['id']}\n" for e in scene["elements"] if e["type"] == "text")
        md = ("---\nexcalidraw-plugin: parsed\ntags: [excalidraw, kalacar, flow]\n---\n"
              "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==\n\n"
              f"Generated by `flows/build_flows.py` — edit the flow there, not here. ← [[19-how-kalacar-works]]\n\n"
              f"# Excalidraw Data\n\n## Text Elements\n{texts}\n%%\n## Drawing\n```json\n{json.dumps(scene, ensure_ascii=False)}\n```\n%%\n")
        with open(os.path.join(HERE, flow["file"] + ".excalidraw.md"), "w") as f:
            f.write(md)
        print(f"built {flow['file']}: {len(flow['nodes'])} steps, {len(flow['edges'])} arrows")

if __name__ == "__main__":
    main()
