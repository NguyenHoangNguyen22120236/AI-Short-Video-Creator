# AI-Short-Video-Creator

## Getting Started

These instructions will help you set up and run the project locally for development and testing purposes.

### Prerequisites

Make sure you have the following installed on your machine:

- Node.js (v16+ recommended) — for frontend  
  [Download Node.js](https://nodejs.org/)

- Python 3.8+ — for backend  
  [Download Python](https://www.python.org/downloads/)

- Docker & Docker Compose — for containerizing PostgreSQL  
  [Docker Installation Guide](https://docs.docker.com/get-docker/)

- Git — for cloning the repository  
  [Git Download](https://git-scm.com/downloads)

### ✅ Backend Setup (FastAPI)

1. **Clone the repo and navigate to backend/ directory:**

   ```bash
   git clone https://github.com/NguyenHoangNguyen22120236/AI-Short-Video-Creator.git
   cd AI-Short-Video-Creator/backend
2. **Create and activate a Python virtual environment:**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
4. **Configure environment variables**

   Create a **.env** file in **backend/** directory:
   ```bash
   # DeepSeek AI Key
   DEEPSEEK_API_KEY=your_deepseek_api_key

   # SERP (Search API) Key
   SERP_API_KEY=your_serp_api_key

   #Stability AI Key
   STABILITY_API_KEY=your_stability_ai_key

   # Cloudflare
   CLOUDFLARE_API_KEY=your_cloudflare_api_key
   CLOUDFLARE_API_SECRET=your_cloudflare_api_secret

   # PostgreSQL Database
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=aishortvideocreator

   # SQLAlchemy URLs
   DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5433/aishortvideocreator
   DATABASE_URL_ALEMBIC=postgresql://postgres:your_password@localhost:5433/aishortvideocreator

   # JWT Auth Secret
   JWT_SECRET_KEY=your_jwt_secret_key

   # Google OAuth
   GOOGLE_CLIENT_ID=your_google_client_id

   # Frontend URL
   FRONTEND_URL=http://localhost:3000

5. **Add your Google Cloud service account key**

   Place the `gcp_key.json` file inside the **backend/** directory. This file will be used for authentication with the Google Text-to-Speech API.

6. **Start PostgreSQL using Docker**

   Make sure Docker is installed and running. Then run database container
   ```bash
   docker-compose up -d
7. **Run Alembic migrations**

   ```bash
   alembic upgrade head
8. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

### ✅ Frontend Setup (ReactJS)
1. **Navigate to the frontend/ directory**
   ```bash
   cd frontend
2. **Install dependencies**
   ```bash
   npm install
3. **Configure environment variables**
   Create a **.env** file in the **frontend/** directory:
   ```bash
   # Google OAuth Client ID
   REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id_here

   # Backend URL
   REACT_APP_BACKEND_URL=http://127.0.0.1:8000
4. **Start the development server**
   ```bash
   npm start