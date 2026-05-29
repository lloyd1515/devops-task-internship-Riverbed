# 📋 Urmărire Progres / Definition of Done (DOD)

Urmărește implementarea cerințelor din [README.md](../../README.md) folosind acest checklist interactiv.

---

## 🔧 1. Fix Docker & Local Run
- [ ] Corectează configurarea rețelei în [docker-compose.yml](../../docker-compose.yml) (astfel încât FastAPI să se poată conecta la containerul Redis).
- [ ] Modifică maparea porturilor în [docker-compose.yml](../../docker-compose.yml) de la `8080:8000` la `8000:8000` conform cerinței specifice de a răspunde la `http://localhost:8000`.
- [ ] Adaugă o secțiune de `healthcheck` pentru serviciul `web` în compose folosind utilitarul `/health` și asigură-te că `docker compose ps` raportează serviciul ca fiind **healthy**.
- [ ] rulează `docker compose up --build` local fără nicio eroare în terminal.

---

## 🌐 2. Fix Backend Bugs & Endpoints
- [ ] Corectează bug-ul logic din funcția de status a bazei de date din [app/main.py](../../app/main.py) (în prezent returnează `redis: True` chiar și atunci când Redis nu este pornit sau aruncă erori).
- [ ] Extinde API-ul cu două endpoint-uri noi:
  - [ ] **`GET /visits/count`** — întoarce valoarea curentă a contorului din Redis fără a o incrementa.
  - [ ] **`POST /visits/reset`** — resetează contorul la `0` și întoarce `{"visits": 0}`.
- [ ] Adaugă teste unitare corespunzătoare pentru noile endpoint-uri în [tests/test_main.py](../../tests/test_main.py) (urmărește structura celor existente folosind Mock).

---

## 🎨 3. Minimal Frontend UI
- [ ] Implementează un UI minimal pe path-ul `/index` în [app/main.py](../../app/main.py):
  - [ ] Returnează un `HTMLResponse` care afișează numărul de vizite obținut prin apelarea backend-ului.
  - [ ] Adaugă un buton de **Reset** pe pagină care să declanșeze un call POST către `/visits/reset` și să actualizeze contorul.

---

## ⚙️ 4. Docker & Environement Optimizations
- [ ] Creează un fișier [.env.example](../../.env.example) cu variabilele de mediu utilizate (`REDIS_HOST`, `REDIS_PORT`).
- [ ] Mută valorile hardcodate din cod în variabile de mediu citite cu `os.getenv`.
- [ ] Optimizează [Dockerfile](../../Dockerfile):
  - [ ] Structurează straturile (layers) pentru a maximiza cache-ul (ex: copie requirements prima dată și rulează `pip install`, apoi restul codului).
  - [ ] Opțional: Asigură-te că imaginea rulează ca non-root user (`non-root` pentru securitate) și folosește o versiune slim/alpine pentru a reduce dimensiunea.

---

## 🤖 5. CI Pipeline (GitHub Actions)
- [ ] Actualizează versiunea de Python din [.github/workflows/ci.yml](../../.github/workflows/ci.yml) de la `2.7` la `3.11`.
- [ ] Adaugă pașii de instalare a dependințelor înainte de rularea `pytest` (în prezent rulează `pytest` direct, fără instalarea pachetelor, ceea ce eșuează instantaneu).
- [ ] Adaugă un step dedicat de linting în pipeline (ex: rulează `flake8`, `black --check`, sau `ruff`).

---

## ✍️ 6. Livrare & Finalizare
- [ ] Copiază [NOTES.md.template](../../NOTES.md.template) în `NOTES.md` în root.
- [ ] Completează onest secțiunile din `NOTES.md`: deciziile de networking/Docker luate, cum ai debuguit problemele, unde te-a ajutat AI-ul.
- [ ] Asigură-te că istoric-ul Git este curat și folosește mesaje clare de commit.
