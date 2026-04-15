# NeuralFlow QA Test Plan

**Prepared by:** QA Agent  
**Date:** 2026-04-15

## Frontend Checks (src/index.html + src/styles.css)

- [ ] src/index.html exists
- [ ] Hero section present with "NeuralFlow" brand name
- [ ] Hero has tagline "Intelligence, Amplified" and CTA button
- [ ] Features grid has exactly 3 feature cards
- [ ] Feature cards include: "Neural Processing", "Real-time Analytics", "Adaptive Learning"
- [ ] Pricing table has exactly 3 tiers: Starter, Pro, Enterprise
- [ ] Pro tier is marked as "Most Popular" or featured
- [ ] Contact form is present with name, email, and message fields
- [ ] Contact form uses fetch() — NOT HTML form action attribute
- [ ] fetch() call targets `http://localhost:3000/api/contact` with POST method
- [ ] src/styles.css is linked via `<link rel="stylesheet" href="styles.css">`
- [ ] CSS custom properties defined: --bg-primary, --accent (dark theme)
- [ ] Responsive breakpoint at 768px present in CSS

## Backend Checks (src/server.js)

- [ ] src/server.js exists
- [ ] GET /api/features is defined
- [ ] GET /api/pricing is defined
- [ ] POST /api/contact is defined
- [ ] POST /api/contact validates required fields (returns 400 if missing)
- [ ] POST /api/contact returns success:true on valid input
- [ ] CORS header Access-Control-Allow-Origin: * is present
- [ ] Server listens on port 3000

## Cross-Reference Checks

- [ ] HTML fetch() URL `http://localhost:3000/api/contact` matches server route `/api/contact` on port 3000
- [ ] Feature names in HTML match feature names in server.js features array
- [ ] README.md exists
- [ ] README.md documents all 3 endpoints
- [ ] README.md has install and run instructions

## Status

Awaiting completion messages from frontend-dev and backend-dev before running checks.
