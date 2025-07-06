# Omukk Python Software Engineer Recruitment Task

This repository contains my submission for the Omukk Python Software Engineer Recruitment Task.

The project is a FastAPI-based social media backend containerized with Docker Compose. It includes PostgreSQL and Redis services, with fixes and improvements per the task instructions.

---

## ✅ Changes Implemented

- 🛠️ **Fixed endpoints to follow REST principles**
  - `GET /posts/` — fetch all posts
  - `GET /posts/{post_id}` — fetch a single post
  - `POST /posts/` — create a new post
  - `PUT /posts/{post_id}` — edit a post
  - `DELETE /posts/{post_id}` — delete a post
  - `POST /posts/{post_id}/like` — toggle like

- ✨ **Validation**:
  - Prevent posting empty strings on creation or editing.
  - Returns 400 error if post content is empty.

- ✅ **Verification Process Implemented**:
  - `POST /auth/verify` — generates a 6-digit code, stores in Redis (expires in 10 minutes), returns code in response.
  - `GET /auth/verify/{code}` — verifies the code, sets `is_verified=True`, deletes Redis key.

- 🐳 **Docker Compose updated**:
  - Added Redis service with password protection.
  - Uses named volume for Redis data.

- ⚙️ **Settings updated**:
  - `.env` and `settings.py` include Redis connection details.

- 📈 **Version bump**:
  - Updated `main.py` version to `0.1.0`.

---

## 🐳 Project Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/R3dRum92/Omukk-task.git
cd Omukk-task
```

### 2️⃣ Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and fill in values:

### 3️⃣ Using Docker Compose
#### 🚀 Start the full stack

```bash
docker compose up --build
```
- FastAPI docs available at http://localhost:8000/docs

- PostgreSQL on port 5432

- Redis on port 6379

#### 🛑 Stop services
```
docker compose down
```

#### 🧹 Remove volumes too
```bash
docker compose down -v
```

### 4️⃣ Running without Docker (Optional)
You can run only the database and redis in Docker and use Poetry locally:
```bash
docker compose up db redis -d
```
Then install dependencies and run the app:
```bash
poetry install
poetry run alembic upgrade head
poetry run fastapi dev
```

Docs available at http://localhost:8000/docs.

## 🔖 Notes

- Make sure Redis is running for verification endpoints.

- Verification codes are returned in API responses for simplicity.
