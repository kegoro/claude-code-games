const express = require('express');
const app = express();
const PORT = 3000;

// CORS middleware — allows frontend from file:// or any origin
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

app.use(express.json());

const features = [
  { id: 1, name: "Neural Processing", description: "Real-time neural network inference at scale", icon: "⚡" },
  { id: 2, name: "Real-time Analytics", description: "Live dashboards powered by streaming data pipelines", icon: "📊" },
  { id: 3, name: "Adaptive Learning", description: "Models that improve continuously from user feedback", icon: "🧠" }
];

const pricing = [
  {
    tier: "Starter",
    price: 0,
    currency: "USD",
    period: "month",
    features: ["5 API calls/day", "Basic analytics", "Community support"]
  },
  {
    tier: "Pro",
    price: 49,
    currency: "USD",
    period: "month",
    features: ["10,000 API calls/day", "Advanced analytics", "Priority support", "Custom models", "Team access", "Export tools"]
  },
  {
    tier: "Enterprise",
    price: null,
    currency: null,
    period: null,
    features: ["Unlimited API calls", "Dedicated infrastructure", "SLA guarantee", "Custom integrations", "24/7 support", "On-premise option"]
  }
];

app.get('/api/features', (req, res) => {
  res.json(features);
});

app.get('/api/pricing', (req, res) => {
  res.json(pricing);
});

app.post('/api/contact', (req, res) => {
  const { name, email, message } = req.body;
  if (!name || !email || !message) {
    return res.status(400).json({
      success: false,
      error: 'Missing required fields: name, email, message'
    });
  }
  console.log(`[Contact] ${name} <${email}>: ${message}`);
  res.json({
    success: true,
    message: `Thank you, ${name}! We'll be in touch.`
  });
});

app.listen(PORT, () => {
  console.log(`NeuralFlow API running on port ${PORT}`);
});
