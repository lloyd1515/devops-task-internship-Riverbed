# 📝 Draft NOTES.md (Pregătire Livrare)

> [!IMPORTANT]
> Copiază conținutul acestei note în fișierul `NOTES.md` din root-ul proiectului după ce ai finalizat implementarea tuturor task-urilor.

---

# DevOps Intern Task - Rezolvare și Note de Debugging

Acest fișier documentează investigațiile mele, deciziile tehnice de arhitectură și optimizările implementate pentru rezolvarea temei de DevOps Intern.

---

## 🔍 1. Cum am debuguit și izolat problemele

Pentru rezolvarea problemelor, m-am bazat pe următoarea metodologie:
1. **Analiza Logurilor Docker:** Rularea `docker compose up --build` a expus imediat problemele de networking ale serviciului FastAPI. Mesajul `redis.exceptions.ConnectionError` a indicat o problemă de rezoluție DNS internă.
2. **Utilizarea GitNexus:** Am analizat fluxurile de execuție din cod și am observat bug-ul de logica din `health()` din [app/main.py](../../app/main.py) și lipsa instalării pachetelor din workflow.
3. **Izolarea Serviciilor:** Am verificat rularea individuală a containerelor pentru a asigura că dependințele de rețea funcționează.

---

## 🛠️ 2. Probleme Identificate și Corectate

### A. Docker Compose & Networking ([docker-compose.yml](../../docker-compose.yml))
* **Host Redis Greșit:** `REDIS_HOST` era configurat pe `localhost`. L-am schimbat în `redis` (numele serviciului din Compose) pentru ca Docker DNS să facă rezoluția IP corectă.
* **Mapare Porturi:** Porturile au fost mapate la `8000:8000` (în loc de `8080:8000`) pentru a expune corect aplicația la portul cerut pe host.
* **Adăugare Healthcheck:** Am integrat o secțiune de `healthcheck` pentru a asigura că serviciul `web` pornește complet și este considerat `healthy` doar când endpoint-ul `/health` returnează succes.

### B. Modificări de Cod ([app/main.py](../../app/main.py))
* **Corectare `/health`:** Am remediat eroarea logică în care `redis_ok` era setat pe `True` chiar dacă ping-ul către Redis arunca o eroare.
* **Noi Endpoint-uri:**
  * `GET /visits/count` pentru citire valoare fără incrementare.
  * `POST /visits/reset` pentru resetarea contorului la 0.
* **Interfață UI minimală (`/index`):** Am implementat o pagină HTML simplă care apelează endpoint-urile de backend și oferă posibilitatea de resetare interactivă din browser.

### C. Pipeline-ul de CI/CD ([.github/workflows/ci.yml](../../.github/workflows/ci.yml))
* **Actualizare Python:** Am modificat versiunea din Actions de la `2.7` la `3.11` pentru compatibilitate cu FastAPI.
* **Instalare Dependențe:** Am adăugat pasul `pip install -r app/requirements.txt` înainte de rularea pytest.
* **Linting:** Am adăugat un pas de verificare a calității codului folosind `flake8` sau `black`.

---

## 🚀 3. Optimizări Aduse Imaginei Docker ([Dockerfile](../../Dockerfile))

1. **Layer Caching:** Am asigurat că fișierul `requirements.txt` este copiat și instalat separat înaintea codului sursă. Astfel, Docker va folosi cache-ul pentru pachete și nu le va reinstala la fiecare modificare minoră a codului Python.
2. **Utilizare non-root:** Am configurat un user de sistem cu permisiuni limitate în interiorul containerului pentru a spori securitatea.
3. **Variabile de mediu:** Am creat [.env.example](../../.env.example) și am externalizat valorile hardcodate.

---

## 🤖 4. Utilizarea Asistentului AI

Pentru a rezolva acest task eficient, am folosit asistentul AI în următoarele moduri:
* Generarea structurii și a diagramelor Mermaid din acest Obsidian Vault.
* Sugerarea sintaxei precise pentru configurarea `healthcheck`-ului din Docker Compose.
* *Notă de Transparență:* AI-ul a oferit promptitudinea necesară pentru vizualizări, însă testarea, configurarea locală și identificarea bug-urilor din cod au fost validate și optimizate manual.
