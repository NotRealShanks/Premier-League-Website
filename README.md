# PremierZone

PremierZone is a Premier League stats web app where you can browse and search player and squad data for the 2025-26 season — filter by team, nation, or position, or search for a specific player directly. The project is split into two main parts: a Spring Boot backend and a React frontend, backed by a Postgres database.

🔗 **Live site:** https://premier-zone-ivory.vercel.app/

<img width="1786" height="998" alt="image" src="https://github.com/user-attachments/assets/c24c924f-8aaf-49f9-ba7f-a629a9e306b0" />

<img width="1848" height="1035" alt="image" src="https://github.com/user-attachments/assets/5a82babb-6297-4182-b310-8778d9d1d613" />


## Features

- **Frontend**: A React interface with dedicated pages for browsing Teams, Nations, and Positions (each searchable), plus a player search bar and a dynamic data table that renders whichever filter is selected — team, nation, position, or player name.
- **Backend**: A Spring Boot REST API (`/api/v1/player`) with full CRUD support. The `GET` endpoint supports optional query parameters for filtering by team, name, position, or nation (including combined filters like team + position), so the frontend can request exactly the slice of data it needs.
- **Database**: A Postgres database hosted on Supabase, storing per-player season stats — goals, assists, cards, minutes played, expected goals/assists, and more — with constraints in place to keep the data clean and consistent.

## Tech Stack

- **Frontend:** React (deployed on Vercel)
- **Backend:** Spring Boot (Java)
- **Database:** Supabase (PostgreSQL)

## Getting Started

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd PremierZone
```

### 2. Backend
```bash
cd backend
# add your Supabase/Postgres connection details to application.properties
mvn spring-boot:run
```

### 3. Frontend
```bash
cd frontend
npm install
npm start
```

## License

MIT
