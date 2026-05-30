# NOTES — [Numele tău]

Copiază acest fișier ca `NOTES.md` și completează-l.

Vrem să fie scurt — maxim 1 pagină. Mai mult contează claritatea decât lungimea.

---

## 1. Probleme găsite și fixate

Pentru fiecare problemă, scrie 2-3 propoziții:

### Problemă #1 (docker-compose.yml - Porturi)
- **Simptom (ce eroare ai văzut?):** Încercarea de a accesa endpoint-urile pe portul `8000` pe mașina gazdă (de ex. `http://localhost:8000/health`) eșua cu eroarea:
  ```
  curl: (7) Failed to connect to localhost port 8000: Connection refused
  ```
- **Cum am diagnosticat-o:** Am analizat `docker-compose.yml` și am văzut că porturile erau mapate ca `"8080:8000"`, ceea ce însemna că aplicația asculta de fapt pe portul `8080` pe mașina gazdă.
- **Cum am fixat-o și de ce:** Am modificat maparea porturilor în `"8000:8000"` în `docker-compose.yml` pentru a respecta cerința din enunț.

### Problemă #2 (docker-compose.yml - Configurare rețea / Redis)
- **Simptom:** Endpoint-ul `/visits` returna eroare HTTP `500 Internal Server Error`, iar în logurile containerului `web` (folosind `docker compose logs web`) apărea excepția de conexiune:
  ```
  redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
  ```
- **Cum am diagnosticat-o:** Am observat în `docker-compose.yml` că variabila `REDIS_HOST` era setată la `localhost`. Din interiorul containerului `web`, conexiunea la `localhost` se face în propriul namespace de rețea, unde Redis nu rulează.
- **Cum am fixat-o și de ce:** Am schimbat `REDIS_HOST` în `redis`, corespunzător numelui serviciului Redis din compose, folosind astfel rezoluția DNS internă oferită de Docker.

### Problemă #3 (app/main.py - Bug logic în `/health`)
- **Simptom:** Când serviciul Redis era oprit (de ex. `docker compose stop redis`), o interogare pe `/health` (pe portul `8080` înainte de a fixa problema #1) continua să returneze cu succes `200 OK` și:
  ```json
  {"status": "ok", "redis": true}
  ```
- **Cum am diagnosticat-o:** Am inspectat codul din `app/main.py` și am văzut că pe blocul de `except redis.RedisError:` variabila `redis_ok` era setată tot ca `True`.
- **Cum am fixat-o și de ce:** Am schimbat linia în `redis_ok = False` în blocul `except` din `app/main.py` pentru a reflecta starea reală a conexiunii la Redis.

### Problemă #4 (docker-compose.yml - Lipsă `curl` pentru Healthcheck)
- **Simptom:** Containerul web rămânea blocat în starea `starting` și devenea ulterior `unhealthy`.
- **Cum am diagnosticat-o:** Am interogat starea de sănătate din Docker cu comanda `docker inspect --format='{{json .State.Health}}' devops-task-internship1-web-1` și am văzut eroarea în loguri:
  ```
  OCI runtime exec failed: exec failed: unable to start container process: exec: "curl": executable file not found in $PATH
  ```
- **Cum am fixat-o și de ce:** Am înlocuit comanda de test bazată pe `curl` în `docker-compose.yml` cu un script inline Python care folosește modulul nativ `urllib.request`. Python este deja garantat prezent în imaginea `python:3.11-slim`, astfel evitându-se încărcarea imaginii prin instalarea pachetului `curl`.

### Problemă #5 (CI - Pipeline-ul de GitHub Actions)
- **Simptom:** Jobul `test` din GitHub Actions eșua la rularea `pytest -v` din cauza lipsei comenzii `pytest`.
- **Cum am diagnosticat-o:** Am analizat fișierul `.github/workflows/ci.yml` și am constatat că se utiliza o versiune învechită de Python (`2.7`) și lipseau pașii de instalare a dependințelor înainte de rularea testelor.
- **Cum am fixat-o și de ce:** Am actualizat Python la versiunea `3.11` în `.github/workflows/ci.yml`, am configurat memoria cache pentru pip bazată pe `app/requirements.txt` (folosind ca sursă de adevăr documentația oficială [actions/setup-python](https://github.com/actions/setup-python)) pentru o execuție mai rapidă. Am adăugat pasul de instalare a dependințelor, precum și un step dedicat de linting cu `ruff` (fără reguli ignorate), pe baza ghidului oficial GitHub [Building and Testing Python](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python).

### Problemă #6 (app/main.py - Lipsă import HTMLResponse)
- **Simptom:** Rularea testelor sau accesarea endpoint-ului `/index` eșua cu eroarea în consolă:
  ```
  NameError: name 'HTMLResponse' is not defined
  ```
- **Cum am diagnosticat-o:** În timpul curățării importurilor nefolosite din commit-urile anterioare, am eliminat `HTMLResponse` crezând că este folosit doar în codul mort/comentat. La implementarea noului endpoint `/index`, acesta a generat excepția de mai sus.
- **Cum am fixat-o și de ce:** Am re-importat `HTMLResponse` prin adăugarea liniei `from fastapi.responses import HTMLResponse` în `app/main.py`.

---

## 2. Healthcheck-ul adăugat

- **Cum funcționează:** Deoarece imaginea de bază `python:3.11-slim` nu include `curl` sau `wget` în mod implicit, am implementat un healthcheck nativ prin intermediul unei comenzi inline în Python care folosește biblioteca standard `urllib.request`. Aceasta accesează local endpoint-ul `/health` expus de FastAPI și verifică dacă răspunde cu succes.
- **De ce ai ales configurarea asta (interval, retries, timeout):**
  - `interval: 10s`: Oferă un echilibru bun între detectarea rapidă a downtime-ului și evitarea încărcării inutile a serverului de backend local.
  - `timeout: 5s`: Oferă o fereastră generoasă pentru ca apelul local să răspundă, chiar și sub încărcare temporară.
  - `retries: 3`: Toleranță la erori tranzitorii (flapping), semnalând containerul ca `unhealthy` doar după 3 eșecuri consecutive.
  - `start_period: 5s`: Perioada de grație inițială acordată procesului Uvicorn și FastAPI pentru pornire și inițializarea conexiunii la Redis.

---

## 3. Folosirea AI-ului

Fii cinstit. Nu pierzi puncte dacă spui adevărul, dimpotrivă.

- **Ce ai folosit:** Antigravity CLI Gemini 3.5 Flash
- **Unde te-a ajutat cel mai mult:** A ajutat la corectarea rapidă a porturilor și a hostname-ului Redis în docker-compose, la remedierea bug-ului logic din `/health` și la implementarea structurii securizate non-root în Dockerfile. De asemenea, a simplificat procesul de generare a testelor unitare și a testelor monkey pentru noul API. (pe scurt, la tot, nu am facut nimic manual, doar am verifica ce a facut)
- **Unde te-a încurcat sau ți-a dat un răspuns greșit:** La prima adăugare a healthcheck-ului, a recomandat utilizarea `curl`, eșuând deoarece imaginea slim nu îl conține (eroare: `exec: "curl": executable file not found in $PATH`). De asemenea, în timpul optimizării importurilor din `app/main.py`, a sugerat eliminarea `HTMLResponse` ca import nefolosit înainte ca endpoint-ul `/index` să fie implementat, ducând la eroarea `NameError: name 'HTMLResponse' is not defined`.
- **Cum ai verificat ce-a generat:** Am observat testele rulate, provenienta si rezolvarea erorilor respectiv verificarea vizuala din cod.

---

## 4. Ce-ai face cu mai mult timp

Următoarele optimizări sunt evidențiate pe baza logurilor de rulare actuale ale serviciilor:

- **Rezolvarea Condiției de Cursă (Race Condition) la Startup**:
  * *Dovadă în loguri:* Aplicația web declară pornirea completă (`web-1 | INFO: Application startup complete.`) și începe să primească health check-uri (`127.0.0.1 - "GET /health"`) înainte ca Redis să fie complet inițializat și pregătit să accepte conexiuni pe portul TCP (`redis-1 | Server initialized ... Ready to accept connections tcp`).
  * *Soluție:* Definirea unui block de `healthcheck` pentru Redis în `docker-compose.yml` și utilizarea `depends_on.redis.condition: service_healthy` sub serviciul `web`.
- **Rularea aplicației fără PID 1 (Gestionare semnale OS)**:
  * *Dovadă în loguri:* Procesul Uvicorn rulează ca PID 1 în container (`web-1 | INFO: Started server process [1]`), ceea ce înseamnă că nu gestionează corect semnalele de terminare standard (`SIGTERM`). La oprirea containerelor, Docker așteaptă 10 secunde în gol înainte de a omorî containerul abuziv prin `SIGKILL`.
  * *Soluție:* Adăugarea directivei `init: true` sub serviciul `web` în `docker-compose.yml` pentru a folosi `tini` ca manager de init în container.
- **Evitarea Poluării Logurilor (Log Noise)**:
  * *Dovadă în loguri:* Logurile standard sunt inundate la fiecare 10 secunde cu mesaje de tipul `127.0.0.1 - "GET /health HTTP/1.1" 200 OK` generate de testele automate de healthcheck local.
  * *Soluție:* Configurat logger-ul din FastAPI / Uvicorn sau implementat un middleware dedicat pentru a exclude cererile spre `/health` din access logs.
- **Configurare securizată pentru Redis în Producție**:
  * *Dovadă în loguri:* Redis pornește cu avertismentul `# Warning: no config file specified, using the default config.`.
  * *Soluție:* Adăugarea unui fișier `redis.conf` montat ca volum în container pentru a configura limite de memorie (`maxmemory`), politici de evacuare a datelor (ex: `allkeys-lru`) și autentificare.
- **Evitarea erorilor 404 pe Root (Polite Redirect)**:
  * *Dovadă în loguri:* Accesarea rădăcinii `/` sau favicon generează `GET / HTTP/1.1" 404 Not Found`.
  * *Soluție:* Adăugarea unui handler pe ruta `/` în `app/main.py` care redirecționează automat (`RedirectResponse`) traficul spre `/index`.

---

## 5. Întrebări / observații

(Orice nu a fost clar, orice ai vrea să discuți cu noi.)
