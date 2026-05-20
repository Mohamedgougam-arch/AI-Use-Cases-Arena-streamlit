# AI Use Cases Arena (Streamlit)

A gamified collaborative platform for Invest-NL business users to submit, browse, vote on, and prioritize AI use cases. Rebuilt in **Python** with **Streamlit** for easy internal hosting.

## Tech Stack

- **Python 3.10+**
- **Streamlit**
- **Pandas** and **Plotly** for insights charts
- JSON file persistence (`data/arena_state.json`) — shared across users on the same server instance

The original Next.js app remains in `src/` for reference; the active app is the Streamlit entry point.

## Getting Started

### Prerequisites

- Python 3.10 or later

### Install dependencies

```bash
cd "C:\AI Use Cases Arena - In Python"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, use `source .venv/bin/activate`.

### Run locally

```bash
streamlit run app.py
```

Open the URL shown in the terminal (typically http://localhost:8501).

### Deploy to Streamlit Cloud

1. Push this repository to GitHub.
2. Create an app at [share.streamlit.io](https://share.streamlit.io) pointing to `app.py`.
3. Python version 3.10+ is recommended.

## Sign in

- **Participants:** work email (e.g. `you@invest-nl.nl`)
- **Administrators:** type `Admin` on the login screen

## Features

| Page | Description |
|------|-------------|
| **Dashboard** | Stats, trending ideas, quick wins, department heatmap |
| **Submit Use Case** | Form with scoring on submit (participants only) |
| **Gallery** | Search, filters, sorting, voting |
| **Use Case Detail** | Full view, comments, private creator messages, AI summary placeholder |
| **Insights** | Charts, impact/effort matrix, executive summary |
| **Admin Leaderboard** | All signed-in users and scores (admin only) |
| **Department Battle** | Department rankings |

## Scoring

| Action | Points |
|--------|--------|
| Submit a use case | +10 |
| Each vote your idea receives | +2 |
| Vote on someone else's idea | +1 |
| Leave a comment | +1 |

## Innovation Score

```
Score = votes × 3 + impact × 20 − effort × 10 + comments × 5 + trendiness bonus
```

## Project Structure

```
├── app.py                 # Streamlit entry point
├── arena/
│   ├── auth.py            # Login helpers
│   ├── constants.py       # Departments, categories
│   ├── scoring.py         # Innovation score formula
│   ├── analytics.py       # Dashboard aggregations
│   ├── participants.py    # Leaderboard scoring
│   ├── store.py           # State mutations
│   ├── storage.py         # JSON persistence
│   └── ui/                # Pages and components
├── data/                  # Runtime state (gitignored)
├── requirements.txt
└── .streamlit/config.toml # Invest-NL theme colors
```

## Data & Privacy

Arena data is stored in `data/arena_state.json` on the server. For production, replace file storage with Supabase or another database using the same schema as the TypeScript types in `src/types/index.ts`.

## License

Private — Invest-NL internal use.
