# 📋 Urmărire Progres / Definition of Done (DOD)

> [!NOTE]
> Acest document conține cerințele preluate **1 la 1** din secțiunile `Ce trebuie să faci` și `Definition of Done` ale fișierului [[README.md]]. 
> Folosește-l ca listă de verificare interactivă pe parcursul rezolvării task-ului.
> 
> Înapoi la [[Dashboard|🚀 Dashboard]].

---

## 🛠️ Ce trebuie să faci

- [x] 1. **Pornește aplicația cu `docker compose up`** și asigură-te că răspunde la `http://localhost:8000/health`.
- [x] 2. **Verifică că `http://localhost:8000/visits` funcționează** (folosește Redis pentru a număra vizitele).
- [x] 3. **Adaugă un healthcheck** în `docker-compose.yml` pentru serviciul web (folosește endpoint-ul `/health`).
- [ ] 4. **Extinde /visits ednpoint** astfel incat sa existe functionalitatea de read `/visits/count` reset `/visits/reset` ** 
- [ ] 5. **Creaza CI pipeline** ce sa ruleze automat la fiecare git push.
- [ ] 6. **Completează `NOTES.md`** — copiază `NOTES.md.template` în `NOTES.md` și scrie un writeup scurt (vezi mai jos).

---

## ✅ Definition of Done

Înainte să livrezi, verifică:

- [x] `docker compose up --build` pornește ambele servicii fără erori.
- [x] `GET http://localhost:8000/health` întoarce `200` cu `{"status": "ok", "redis": true}`.
- [x] `GET http://localhost:8000/visits` incrementează la fiecare request.
- [x] `docker compose ps` arată serviciul `web` ca `healthy`.
- [ ] Adaugă un fișier `.env.example` și mută hardcoded values în variabile de mediu.
- [ ] Optimizează `Dockerfile` (cache layers, image size).
- [x] Adaugă un step de linting în CI.
- [ ] **Extinde API-ul cu două endpoint-uri noi pentru counter (cu teste):**
- [ ] `GET /visits/count` — întoarce numărul curent de vizite **fără** să-l incrementeze. 
- [ ] `POST /visits/reset` — resetează counter-ul la `0` și întoarce `{"visits": 0}`. 
- [ ] **Adaugă un UI minimal pe path-ul `/index`:**. 
  - [ ] Returnează o pagină HTML care obtine datele din backend endpoint (`/visits`).
  - [ ] Adauga buton de reset ce apeleaza  (`/reset`).
- [ ] Nice to have CI pipeline succesful on github.
- [ ] `NOTES.md` e completat.
