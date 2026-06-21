# Instagram Creator Analytics Dashboard

A full-stack analytics dashboard that analyzes public Instagram creator profiles and generates actionable insights for creator evaluation and campaign research.

---

## Features

- Creator profile analysis
- Engagement rate calculation
- Average likes and comments analysis
- Posting frequency insights
- Viral post identification
- Collaboration post detection
- Interactive analytics dashboard
- Real-time profile analysis

---

## Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python
- Playwright

---

## Project Structure

```text
Insta_Data_aggregator/
├── frontend/    # React dashboard
└── backend/     # FastAPI analytics service
```

---

## Setup

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create a `.env` file using the provided `.env.example` template.

Example:

```env
MONGODB_URL=
IG_USERNAME=
IG_PASSWORD=
```

---

## How It Works

1. Enter an Instagram creator username.
2. The backend collects public creator profile and post data.
3. Analytics are generated from the collected data.
4. Insights are displayed through an interactive dashboard.


