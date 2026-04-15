# NeuralFlow API

A simple REST API for the NeuralFlow AI startup landing page. Built with Express.js.

## Prerequisites

- Node.js 18+
- npm

## Install

```
npm install
```

## Run

```
node src/server.js
```

The API starts on port 3000.

## Endpoints

### GET /api/features

Returns an array of 3 NeuralFlow AI feature objects.

**Response:**
```json
[
  { "id": 1, "name": "Neural Processing", "description": "...", "icon": "⚡" },
  { "id": 2, "name": "Real-time Analytics", "description": "...", "icon": "📊" },
  { "id": 3, "name": "Adaptive Learning", "description": "...", "icon": "🧠" }
]
```

**curl:**
```
curl http://localhost:3000/api/features
```

### GET /api/pricing

Returns an array of 3 pricing tier objects.

**Response:**
```json
[
  { "tier": "Starter", "price": 0, "currency": "USD", "period": "month", "features": [...] },
  { "tier": "Pro", "price": 49, "currency": "USD", "period": "month", "features": [...] },
  { "tier": "Enterprise", "price": null, "currency": null, "period": null, "features": [...] }
]
```

**curl:**
```
curl http://localhost:3000/api/pricing
```

### POST /api/contact

Accepts a contact form submission. Validates that name, email, and message are all present.

**Request body:**
```json
{ "name": "Jane Smith", "email": "jane@example.com", "message": "Hello!" }
```

**Success (200):**
```json
{ "success": true, "message": "Thank you, Jane Smith! We'll be in touch." }
```

**Error (400 — missing fields):**
```json
{ "success": false, "error": "Missing required fields: name, email, message" }
```

**curl:**
```
curl -X POST http://localhost:3000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@example.com","message":"Hello"}'
```

## Node.js Installation Note

Node.js was not detected in the environment at setup time. To install Node.js LTS on Windows, run:

```
winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
```

After installation, run `npm install` in the project root before starting the server.
