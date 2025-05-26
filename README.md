# Document Q&A Backend (Django)

This is the backend API for the Document Q&A Portal. It is built with Django and Django REST Framework, supports JWT authentication, file uploads, and integrates with an AI model for Q&A.

## Features

- User registration and login (JWT-based)
- Document upload and listing
- AI-powered question-answering about uploaded documents
- PostgreSQL database support
- CORS support for frontend integration

---

## Requirements

- Python 3.8+
- pip
- [PostgreSQL database](https://render.com/docs/databases) (recommended for production)
- (Optional) [Render Persistent Disk](https://render.com/docs/persistent-disks) or S3 for file storage

---

## Local Development Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/ratinto/doc-backend.git
    cd doc-backend
    ```

2. **Create a virtual environment & activate**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables**
    - Create a `.env` file or export variables in your shell:
      ```
      DEBUG=True
      SECRET_KEY=your_secret_key
      DATABASE_URL=sqlite:///db.sqlite3
      GEMINI_API_KEY=your_gemini_api_key
      ```

5. **Run migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional)**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the backend**
    ```bash
    python manage.py runserver
    ```

---

## Production Deployment (Render)

1. **Push code to GitHub (or another Git provider).**
2. **Create a new Web Service on Render.**
3. **Add environment variables in Render dashboard:**
    - `SECRET_KEY`
    - `DEBUG=False`
    - `DATABASE_URL` (from your Render PostgreSQL instance)
    - `GEMINI_API_KEY`
4. **(Optional) Add a Persistent Disk for `/media` if storing files locally.**
5. **Set Build Command:**
    ```
    pip install -r requirements.txt && python manage.py collectstatic --noinput
    ```
6. **Set Start Command:**
    ```
    gunicorn your_project_name.wsgi
    ```
7. **After deploy, run migrations from the Render shell:**
    ```
    python manage.py migrate
    ```

---

## Important Django Settings

- `ALLOWED_HOSTS`: Should include your Render domain.
- `CORS_ALLOWED_ORIGINS`: Should include your Vercel frontend URL.
- `MEDIA_ROOT` and `MEDIA_URL`: Set up for file uploads.

---

## API Endpoints

- `POST /api/register/` – Register a user
- `POST /api/token/` – Obtain JWT token
- `GET/POST /api/documents/` – List/upload documents
- `DELETE /api/documents/<id>/` – Delete a document
- `POST /api/ask-question/` – Ask a question about a document

---
