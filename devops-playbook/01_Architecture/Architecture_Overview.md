# 📐 Arhitectură & Diagrame Mermaid

Acest document descrie arhitectura sistemului FastAPI + Redis și fluxul pipeline-ului de CI/CD.

---

## 🖥️ Topologia Aplicației (Docker Compose)

Aplicația este formată din două containere care rulează pe aceeași rețea Docker implicită (bridge network):
1. **`web`**: FastAPI rulat pe portul `8000`. Expune portul `8000` către exterior.
2. **`redis`**: Instanță de Redis Cache care stochează vizitele în memorie.

```mermaid
graph LR
    User([Utilizator / Host]) -- localhost:8000 --> Web[FastAPI Container: web]
    Web -- REDIS_HOST=redis:6379 --> Redis[(Redis Database: redis)]
    
    style User fill:#a6e3a1,stroke:#a6e3a1,color:#11111b;
    style Web fill:#89b4fa,stroke:#89b4fa,color:#11111b;
    style Redis fill:#f9e2af,stroke:#f9e2af,color:#11111b;
```

---

## 🔁 Diagramă de Secvență (Request Flow)

Cum se procesează un request la endpoint-ul `/visits` (configurat în [app/main.py](../../app/main.py)):

```mermaid
sequenceDiagram
    autonumber
    actor User as Utilizator / Browser
    participant Web as FastAPI (Serviciul 'web')
    participant Redis as Redis (Serviciul 'redis')

    User->>Web: GET /visits
    activate Web
    Note over Web: Execută r.incr("visits")
    Web->>Redis: INCR visits
    activate Redis
    Redis-->>Web: Returnează noua valoare (ex: 42)
    deactivate Redis
    Web-->>User: JSON: {"visits": 42}
    deactivate Web
```

Pentru endpoint-urile noi solicitate în [README.md](../../README.md):
- **`GET /visits/count`**: Citește valoarea folosind `r.get("visits")` fără să o incrementeze.
- **`POST /visits/reset`**: Resetează valoarea cu `r.set("visits", 0)`.

---

## 🏗️ Diagramă de Flux (CI/CD Pipeline)

Fluxul dorit pentru pipeline-ul din [.github/workflows/ci.yml](../../.github/workflows/ci.yml) la fiecare `git push`:

```mermaid
flowchart TD
    Start([Git Push / PR]) --> Checkout[1. Actions Checkout v4]
    Checkout --> Python[2. Setup Python 3.11]
    Python --> Deps[3. Instalare Dependențe <br> pip install -r app/requirements.txt]
    Deps --> Lint[4. Rulare Linter <br> flake8 / black / ruff]
    Lint --> Test[5. Rulare Teste Unitare <br> pytest -v]
    Test --> Build[6. Build Docker Image <br> intern-task-devops:ci]
    Build --> End([Pipeline Succesful 🎉])

    style Start fill:#a6e3a1,stroke:#a6e3a1,color:#11111b;
    style End fill:#a6e3a1,stroke:#a6e3a1,color:#11111b;
```

---

> [!NOTE]
> Pentru detalii despre problemele de networking identificate între containere, consultă [[03_Debugging/Bug_Journal.md|Jurnalul de Debugging]].
