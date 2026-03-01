# Study Tracker

A streamlined, data-driven application designed to help candidates track, analyze, and optimize their study routines for public exams (*concursos*). Built with **Python** and **Streamlit**, this tool provides a visual dashboard to monitor progress against goals, manage study sessions, and visualize performance metrics.

---

## Purpose

Preparing for public exams requires discipline and consistent tracking. This project serves as a personal "Study Command Center," allowing users to:
- **Quantify Effort**: Move beyond "feeling" productive to seeing actual hours spent on specific subjects.
- **Track Goals**: Set weekly targets and visualize progress in real-time.
- **Data-Driven Decisions**: Identify which subjects need more attention based on historical data.

---

## Key Features

- **Real-time Dashboard**: Visual metrics for total hours, daily averages, and session intensity.
- **Interactive Timer**: Start and stop study sessions directly from the interface.
- **Weekly Goal Management**: Set study hour targets for each week and track fulfillment percentages.
- **Detailed History**: Review past sessions and manage records.
- **Exercise Tracking**: Log quantity and accuracy of solved questions.
- **Data Persistence**: Local SQLite database ensuring your data stays private and accessible.

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (for a fast, interactive UI)
- **Data Analysis**: [Pandas](https://pandas.pydata.org/)
- **Visualizations**: [Matplotlib](https://matplotlib.org/)
- **Database**: [SQLite](https://www.sqlite.org/index.html)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## Running with Docker

This is the recommended way to run the project, as it handles all dependencies automatically.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/mello-pedro/webapp_concursos.git
   cd app_concursos
   ```

2. **Spin up the container**:
   ```bash
   docker-compose up -d
   ```

3. **Access the app**:
   Open your browser and go to: `http://localhost:8501`

---

## Local Setup (Alternative)

If you prefer to run it directly with Python:

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run src/home.py
   ```

---

## Project Structure

```text
├── src/               # Application source code
│   ├── home.py        # Landing page & Main metrics
│   ├── db.py          # Database operations
│   └── pages/         # Specialized views (Stats, Goals, etc.)
├── db/                # Local SQLite database (persisted via Docker volumes)
├── data/              # Reference files and external data
├── Dockerfile         # Docker build instructions
└── docker-compose.yml # Service orchestration
```
