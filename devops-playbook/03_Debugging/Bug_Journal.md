# 🐛 Jurnal de Debugging (Debugging Journal)

Utilizează acest jurnal pentru a înțelege și documenta bug-urile din proiect. Acesta este materialul perfect de studiu pentru a înțelege exact cum funcționează sistemul și de a completa ulterior secțiunea de debugging din `NOTES.md`.

---

## 🐞 Bug 1: Containerul `web` nu se poate conecta la Redis

### 🚨 Simptom
Aplicația dă erori de conexiune în loguri la pornire sau endpoint-ul `/health` întoarce status fals pentru Redis (după rezolvarea logicii din `/health`).
*Mesaj de eroare în terminal:* `redis.exceptions.ConnectionError: Error -2 connecting to localhost:6379. Name or service not known.`

### 🔍 Investigație (cu GitNexus & logs)
Analizând [docker-compose.yml](../../docker-compose.yml), vedem la secțiunea de variabile de mediu pentru serviciul `web`:
```yaml
environment:
  - REDIS_HOST=localhost #redis
```
Într-un mediu Docker multi-container implicit, fiecare container își rulează propriul network namespace. `localhost` indică loopback interface-ul containerului `web` însuși, NU al hostului sau al altui container.

### 💡 Cauză Principală
Containerul `web` încearcă să caute serviciul Redis pe localhost-ul său local, unde nu rulează niciun proces Redis. Comunicarea inter-container în Docker Compose folosește rezoluția DNS internă, unde numele serviciului este folosit ca hostname.

### 🛠️ Soluție
Schimbă variabila de mediu în [docker-compose.yml](../../docker-compose.yml) din `localhost` în numele serviciului definit în compose, adică `redis`:
```diff
 environment:
-  - REDIS_HOST=localhost #redis
+  - REDIS_HOST=redis
   - REDIS_PORT=6379
```

---

## 🐞 Bug 2: Portul greșit mapat pe Host

### 🚨 Simptom
În `README.md` ni se cere ca aplicația locală să răspundă la `http://localhost:8000/health`, dar după rularea `docker compose up`, portul `8000` pe host dă `Connection Refused` sau eroare, în timp ce pe portul `8080` funcționează.

### 🔍 Investigație
Maparea porturilor din [docker-compose.yml](../../docker-compose.yml) este definită astfel:
```yaml
ports:
  - "8080:8000"
```
Formatul este `"port_host:port_container"`. Asta înseamnă că portul intern `8000` al containerului este expus pe portul `8080` al mașinii tale fizice (host).

### 💡 Cauză Principală
Cerințele din Definition of Done cer explicit accesarea aplicației la portul `8000`.

### 🛠️ Soluție
Modifică maparea porturilor în [docker-compose.yml](../../docker-compose.yml):
```diff
 ports:
-  - "8080:8000"
+  - "8000:8000"
```

---

## 🐞 Bug 3: Endpoint-ul `/health` raportează Redis ca `True` chiar dacă conexiunea eșuează

### 🚨 Simptom
Dacă oprești serviciul Redis cu `docker compose stop redis`, apelul către endpoint-ul `/health` returnează în continuare `{"status": "ok", "redis": true}` în loc de `{"status": "ok", "redis": false}`.

### 🔍 Investigație
Codul din [app/main.py](../../app/main.py) arată așa la linia 19:
```python
@app.get("/health")
def health() -> dict:
    try:
        r.ping()
        redis_ok = True
    except redis.RedisError:
        redis_ok = True
    return {"status": "ok", "redis": redis_ok}
```

### 💡 Cauză Principală
În blocul `except redis.RedisError:`, variabila `redis_ok` este setată greșit tot pe `True` în loc de `False`. Este o eroare logică simplă (typo/bug).

### 🛠️ Soluție
Corectează blocul except pentru a raporta corect starea conexiunii:
```diff
     try:
         r.ping()
         redis_ok = True
     except redis.RedisError:
-        redis_ok = True
+        redis_ok = False
     return {"status": "ok", "redis": redis_ok}
```

---

## 🐞 Bug 4: Pipeline-ul CI/CD eșuează instantaneu (Python 2.7 & pytest Lipsă)

### 🚨 Simptom
La rularea pipeline-ului GitHub Actions în [.github/workflows/ci.yml](../../.github/workflows/ci.yml), jobul de testare eșuează imediat cu o eroare de tip: `pytest: command not found` sau erori de sintaxă Python deoarece codul FastAPI nu este compatibil cu Python 2.7.

### 🔍 Investigație
Configurația workflow-ului conține:
```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "2.7"

      - name: Run tests
        run: pytest -v
```

### 💡 Cauză Principală
1. FastAPI, Pydantic și modulele moderne de Python 3.11 folosite în proiect nu pot rula sub Python 2.7 (care a ajuns la end-of-life din 2020).
2. Deși `pytest` este definit în `requirements.txt`, workflow-ul rulează direct comanda `pytest -v` fără să fi instalat dependințele în runner-ul virtual (care vine inițial complet curat).

### 🛠️ Soluție
Actualizează versiunea de Python la `3.11` și adaugă pasul de instalare a dependințelor înainte de teste:
```diff
       - name: Set up Python
         uses: actions/setup-python@v5
         with:
-          python-version: "2.7"
+          python-version: "3.11"
+
+      - name: Install dependencies
+        run: |
+          python -m pip install --upgrade pip
+          pip install -r app/requirements.txt
 
       - name: Run tests
         run: pytest -v
```

---

> [!TIP]
> După ce corectezi aceste bug-uri local, poți rula `pytest -v` pentru a te asigura că testele unitare trec cu succes. Vezi progresul complet pe secțiunea [[02_Tasks/DOD_Tracker.md|DOD Tracker]].
