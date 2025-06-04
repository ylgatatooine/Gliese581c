# 🐳 Running YouTube Transcripter in Docker

This guide shows you how to build and run the YouTube Transcript Downloader using Docker Desktop.

---

## 📁 Project Structure

```
youtube-transcripter/
├── Dockerfile
├── .dockerignore
├── main.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
```

---

## 🔧 Step 1: Create Dockerfile

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🙈 Step 2: Create .dockerignore

```plaintext
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
*.log
.env
```

---

## 🏗 Step 3: Build Docker Image

```bash
docker build -t yt-transcript-app .
```

---

## 🚀 Step 4: Run the Container

```bash
docker run -d -p 8000:8000 yt-transcript-app
```

Then open your browser and visit:

👉 [http://localhost:8000](http://localhost:8000)

---

## 🧹 Optional: Stop & Remove the Container

```bash
docker ps         # to get container ID
docker stop <ID>
docker rm <ID>
```

---

Happy hacking! 🎉