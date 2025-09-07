# Kaushalya Swap – Backend

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python server.py
```
Now open: http://127.0.0.1:8000/api/health

### Test signup (example)
```bash
curl -X POST http://127.0.0.1:8000/api/signup   -H "Content-Type: application/json"   -d '{
    "name":"Nishant",
    "email":"nishant@example.com",
    "password":"12345678",
    "teach":"Web Dev",
    "learn":"Guitar"
  }'
```

## Deploy to Render (one-time)
1. Push this folder to a **new GitHub repo** (e.g., `kaushalyaswap-backend`).
2. In Render: **New + → Web Service → Connect your repo**.
3. Set **Build Command**: `pip install -r requirements.txt`.
4. Set **Start Command**: `gunicorn server:app`.
5. Create service → copy the public URL (e.g., `https://your-backend.onrender.com`).
6. Update your frontend `BACKEND_URL` in `get-started.html`.
