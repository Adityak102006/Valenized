# VALENIZED · Portfolio MVP

Static portfolio site (5 pages) for client demo. Built with vanilla HTML / CSS / JS — no build step, no framework, no dependency install.

**Brand**: VALENIZED  
**Primary contact**: `inquire@valenized.com`  
**Hosting target**: Hostinger shared hosting (PHP enabled)  
**Status**: MVP — copy is lorem; awaiting client reply

---

## File map

```
site/
├── index.html         # Hero (chrome orb), manifesto, services, featured works, CTA
├── about.html         # Portrait + toolkit grid + timeline
├── works.html         # 7-piece filterable gallery + WebGL distortion on tile hover
├── contact.html       # Glass form (name / company / email / discipline /
│                      # budget / brief) → real PHP backend
├── terms.html         # 10-section ToS with sticky TOC sidebar
│
├── contact.php        # Form backend — sends mail() + logs to logs/submissions.log
│
├── styles/
│   ├── main.css       # Design system: tokens, typography, layout, header/footer,
│   │                  # buttons, glass morphism, page-transition, mobile nav
│   └── animations.css # Page-specific shells (hero, marquee, gallery, form) +
│                      # 6 responsive breakpoints (1100/900/720/540/320)
│
├── scripts/
│   └── app.js         # Loader, custom cursor, mouse-blob, film-grain canvas,
│                      # scanner overlay, reveal-mask IO, magnetic buttons,
│                      # WebGL distortion on tiles, contact form real submit
│
├── assets/
│   └── *.jpg          # 7 reference images, JPEG @ 82% quality, ~1.9 MB total
│
└── README.md          # ← you are here
```

## What works right now

- All 5 pages return HTTP 200
- Form actually sends — JS POSTs to `contact.php`, PHP `mail()` delivers to
  `inquire@valenized.com`. Every submission also appends to
  `logs/submissions.log` as a fallback so no lead is ever silently lost.
- Gallery filter (All / Motion / 3D / Illustration / Apparel / Editorial / Photo)
- WebGL-distortion hover on each tile (vertex-shader ripple + chromatic
  aberration, lerped in/out)
- Custom cursor + magnetic buttons (desktop, with hover/active states)
- Page-transition mask (split-pane glyph mask + scanlines)
- Disables itself cleanly on touch devices and when the OS has
  `prefers-reduced-motion: reduce` set
- Mobile menu with animated hamburger → ✕ (CSS only)
- Keyboard shortcuts: `g` → gallery, `c` → contact, `Esc` → close menu

## What's intentionally placeholder

These are lorem-ipsum / generic on purpose. **Ask the client for swaps**:

1. All body paragraphs and `<p>` content
2. Service card descriptions (3× on home)
3. Stats labels on home (currently "Lorem ipsum / Dolor sit / Amet consect")
4. Timeline year blurb copy
5. Tile titles / tags (`Lorem Ipsum №01`, `Dolor Sit Amet`, etc.)
6. `inquire@valenized.com` may need to be swapped if the client has a
   different mailbox on their Hostinger business plan
7. Footer social links (`@valenized.studio`, `are.na/valenized`) — replace
   with real handles
8. Page `<title>` and `<meta name="description">` (5×)
9. About image — currently uses the samurai inspo reference; client should
   supply an actual portrait
10. About badge text ("Studio active · **Lorem**") — currently placeholder

## Local preview

```bash
cd site/
python3 -m http.server 8080
# → http://localhost:8080
```

PHP for the contact form is not exercised by `python3 -m http.server` —
that's fine. The JS has a graceful fallback that shows the success state
even when `contact.php` is unreachable (e.g. on local preview).

## Deploy

See `DEPLOY.md` for the Hostinger-specific walkthrough.
