"""Simple FastAPI app with a Redis-backed visit counter."""

import os

import redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = FastAPI(title="DevOps Intern Demo", version="0.1.0")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


### Backend API endpoints
@app.get("/health")
def health() -> dict:
    try:
        r.ping()
        redis_ok = True
    except redis.RedisError:
        redis_ok = False
    return {"status": "ok", "redis": redis_ok}

@app.get("/visits")
def visits() -> dict:
    count = r.incr("visits")
    return {"visits": count}

@app.get("/visits/count")
def visits_count() -> dict:
    val = r.get("visits")
    count = int(val) if val is not None else 0
    return {"visits": count}

@app.post("/visits/reset")
def visits_reset() -> dict:
    r.set("visits", 0)
    return {"visits": 0}

@app.get("/index", response_class=HTMLResponse)
def index() -> HTMLResponse:
    html_content = """<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Dashboard — Visit Counter</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-color: #818cf8;
            --accent-glow: rgba(129, 140, 248, 0.3);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --btn-bg: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            --btn-hover: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
            --btn-shadow: rgba(239, 68, 68, 0.3);
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }

        body::before {
            content: '';
            position: absolute;
            width: 400px;
            height: 400px;
            background: rgba(99, 102, 241, 0.15);
            border-radius: 50%;
            top: -100px;
            left: -100px;
            filter: blur(100px);
            z-index: 0;
        }

        body::after {
            content: '';
            position: absolute;
            width: 300px;
            height: 300px;
            background: rgba(236, 72, 153, 0.1);
            border-radius: 50%;
            bottom: -50px;
            right: -50px;
            filter: blur(80px);
            z-index: 0;
        }

        .container {
            position: relative;
            z-index: 10;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 48px;
            width: 90%;
            max-width: 480px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3),
                        0 0 50px rgba(99, 102, 241, 0.05);
            transform: translateY(0);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .container:hover {
            border-color: rgba(129, 140, 248, 0.2);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4),
                        0 0 80px rgba(99, 102, 241, 0.1);
        }

        h1 {
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #ffffff, #c7d2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin-bottom: 40px;
        }

        .counter-wrapper {
            margin-bottom: 40px;
            position: relative;
        }

        .counter-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--accent-color);
            font-weight: 600;
            margin-bottom: 12px;
        }

        .counter-value {
            font-size: 5rem;
            font-weight: 800;
            line-height: 1;
            font-feature-settings: "tnum";
            text-shadow: 0 0 30px var(--accent-glow);
            transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .counter-value.pulse {
            transform: scale(1.1);
        }

        .btn-reset {
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: white;
            background: var(--btn-bg);
            border: none;
            border-radius: 14px;
            padding: 16px 32px;
            cursor: pointer;
            width: 100%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 10px 20px var(--btn-shadow);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn-reset:hover {
            background: var(--btn-hover);
            transform: translateY(-2px);
            box-shadow: 0 15px 25px var(--btn-shadow);
        }

        .btn-reset:active {
            transform: translateY(0);
        }

        .btn-reset svg {
            width: 18px;
            height: 18px;
            fill: currentColor;
            transition: transform 0.4s ease;
        }

        .btn-reset:hover svg {
            transform: rotate(-180deg);
        }

        .footer {
            margin-top: 32px;
            font-size: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DevOps Intern Playbook</h1>
        <p class="subtitle">Sistem de Monitorizare Vizite</p>
        
        <div class="counter-wrapper">
            <p class="counter-label">Total Vizite</p>
            <div id="counter" class="counter-value">...</div>
        </div>
        
        <button id="reset-btn" class="btn-reset">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M19 8l-4 4h3c0 3.31-2.69 6-6 6-1.01 0-1.97-.25-2.8-.7l-1.46 1.46C8.97 19.54 10.43 20 12 20c4.42 0 8-3.58 8-8h3l-4-4zM6 12c0-3.31 2.69-6 6-6 1.01 0 1.97.25 2.8.7l1.46-1.46C15.03 4.46 13.57 4 12 4c-4.42 0-8 3.58-8 8H1l4 4 4-4H6z"/>
            </svg>
            Resetează Contorul
        </button>
        
        <div class="footer">
            <div class="status-dot"></div>
            <span>Conectat la backend & Redis</span>
        </div>
    </div>

    <script>
        const counterEl = document.getElementById('counter');
        const resetBtn = document.getElementById('reset-btn');

        async function fetchVisits() {
            try {
                const response = await fetch('/visits');
                if (response.ok) {
                    const data = await response.json();
                    updateCounter(data.visits);
                } else {
                    counterEl.textContent = 'Error';
                    counterEl.style.color = '#ef4444';
                }
            } catch (err) {
                console.error('Fetch error:', err);
                counterEl.textContent = 'Offline';
                counterEl.style.color = '#ef4444';
            }
        }

        function updateCounter(val) {
            counterEl.textContent = val;
            counterEl.style.color = '';
            counterEl.classList.add('pulse');
            setTimeout(() => counterEl.classList.remove('pulse'), 200);
        }

        resetBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/visits/reset', { method: 'POST' });
                if (response.ok) {
                    const data = await response.json();
                    updateCounter(data.visits);
                } else {
                    alert('Eroare la resetarea contorului.');
                }
            } catch (err) {
                console.error('Reset error:', err);
                alert('Eroare de rețea la conectarea cu backend-ul.');
            }
        });

        fetchVisits();
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)