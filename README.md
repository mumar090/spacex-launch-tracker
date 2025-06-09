---
# SpaceX Launch Tracker

A fullstack application for tracking and visualizing SpaceX launches using data from the SpaceX API v4.
It includes a FastAPI backend and a React + Chart.js frontend.
---

## Features

- Fetch real-time launch data from SpaceX API
- Filter launches by date, rocket name, success status, or launch site (only in backend)
- Visualize statistics such as success rates, launch counts, and frequency using Chart.js
- FastAPI backend with Pydantic models and service-layer architecture
- Unit tests using `pytest` and `pytest-asyncio`
- Caching with `fastapi-cache` for improved performance
- Frontend built with React, Vite, Axios, and Chart.js
- Modern tooling: FastAPI, Poetry, Vite, React, Pydantic

## Project Structure

```
├── backend/                   # Backend directory
│   ├── api/                   # FastAPI routes
│   ├── config/                # Configuration
│   ├── models/                # Pydantic models
│   ├── services/              # Business logic layer
│   ├── tests/                 # Pytest-based tests
├── frontend/                  # Frontend directory (React)
│   ├── src/                   # React components
│   └── index.html             # Entry HTML
├── package.json               # Frontend configuration (Vite)
├── pyproject.toml             # Poetry configuration
```

---

## Installation Instructions

### Prerequisites

- Python 3.12
- Node.js 23.1.0
- [Poetry](https://python-poetry.org/docs/#installation) or using pip
- [Vite](https://vitejs.dev)

---

### Backend Setup (Python + Poetry)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mumar090/spacex-launch-tracker.git
   cd spacex_launch_tracker
   ```

2. **Install Python dependencies:**

   ```bash
   poetry install
   ```

3. **Activate Poetry virtual environment:**

   ```bash
   poetry shell
   ```

---

### Frontend Setup (React + Vite)

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**

   ```bash
   npm install
   ```

---

### Running Both Backend and Frontend Concurrently

Start both the backend and frontend concurrently using `npm run dev:all`:

```bash
npm run dev:all
```

- **Backend** will run at: `http://localhost:8000`
- **Frontend** will run at: `http://localhost:5173`

---

## Testing

1. **Run the tests:**

   From the root directory, run the following command to execute tests:

   ```bash
   poetry run pytest
   ```

---

## Author

**Muhammad Umar**

---
