# PrimeTradeAI

PrimeTradeAI is a comprehensive task management application featuring a robust FastAPI backend and a modern React frontend. It provides secure authentication, task lifecycle management, and administrative tools for user and task oversight.

## 🚀 Features

- **Authentication**: Secure JWT-based authentication using HTTP-only cookies.
- **Task Management**: Create, read, update, and delete tasks with priority, status, and due dates.
- **Admin Dashboard**: Specialized endpoints for administrators to manage all users and tasks across the platform.
- **Responsive UI**: Built with React 19, Tailwind CSS 4, and Shadcn UI for a premium user experience.

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) with [Alembic](https://alembic.sqlalchemy.org/) for migrations.
- **Authentication**: JWT (JSON Web Tokens) with secure cookie storage.

### Frontend
- **Framework**: [React 19](https://react.dev/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/) & [Shadcn UI](https://ui.shadcn.com/)
- **State Management**: [TanStack Query (React Query)](https://tanstack.com/query/latest)
- **Routing**: [TanStack Router](https://tanstack.com/router/latest)

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose

### 1. Database Setup
The easiest way to start the database is using Docker:
```bash
docker-compose up -d
```
This will start a PostgreSQL instance on port `5432`.

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   - **Using pip**:
     ```bash
     pip install -e .
     ```
   - **Using uv (Recommended)**:
     ```bash
     uv sync
     ```
3. Configure environment variables:
   Copy `.env.example` to `.env` and update values if necessary.
4. Run migrations:
   ```bash
   # Using pip/python
   alembic upgrade head
   
   # Using uv
   uv run alembic upgrade head
   ```
5. Start the server:
   ```bash
   # Using pip/python
   python app/main.py

   # Using uv
   uv run python app/main.py
   ```
   The API will be available at `http://localhost:8080`.

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:3000`.

---

## 📖 API Documentation

Detailed API documentation and test data can be found in [test_data.md](./test_data.md).

### Main Endpoint Groups
- `/api/v1/auth`: Registration, Login, Logout, and Token Refresh.
- `/api/v1/tasks`: User-specific task CRUD and Admin task management.
- `/api/v1/users`: User profile management and Admin user oversight.

---

## 🧪 Testing
- **Backend**: Run tests using `pytest` from the `backend` directory.
- **Frontend**: Run tests using `npm test` from the `frontend` directory.
