# k8s-SRE-Valtech

Monorepo con tres microservicios FastAPI y sus manifiestos de Kubernetes para un entorno local (`namespace: sre-local`). Cada servicio usa SQLite en `/data`, montado como PVC en Kubernetes.

## Servicios
- **Auth Service** (`/auth`): alta y consulta de usuarios (`POST /auth/api/users`, `GET /auth/api/users/{username}`); BD `users.db`.
- **Expenses Service** (`/expenses`): CRUD de gastos (`/api/expenses`); BD `expenses.db`.
- **Reporting Service** (`/reports`): consultas de gastos (`/monthly`, `/by-category`, `/range`) leyendo la misma BD de gastos en modo solo lectura.

## Requisitos
- Docker para construir imágenes.
- `kubectl` y un cluster con `ingress-nginx`.
- Entrada DNS/hosts para `api.local` apuntando al Ingress.

## Estructura rápida
- `services/*`: código de cada servicio FastAPI y sus Dockerfiles.
- `k8s/namespace.yaml`: namespace `sre-local`.
- `k8s/{auth,expenses,reporting}`: Deployments, Services, ConfigMaps y PVCs.
- `k8s/ingress.yaml`: rutas HTTP (`api.local/auth|expenses|reports`) con rewrite.

## Construir imágenes locales
```bash
docker build -t auth-service:local services/auth-service
docker build -t expenses-service:local services/expenses-service
docker build -t reporting-service:local services/reporting-service
```

## Despliegue en Kubernetes
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/auth
kubectl apply -f k8s/expenses
kubectl apply -f k8s/reporting
kubectl apply -f k8s/ingress.yaml
```
Notas:
- Los PVC `auth-db-pvc` y `expenses-db-pvc` son de 1Gi. Reporting monta `expenses-db-pvc` en modo lectura para reutilizar la BD.
- Los pods publican liveness/readiness en `/` puerto 8000.

## Uso de las APIs (vía Ingress `api.local`)
- **Crear usuario**  
  `POST http://api.local/auth/api/users` con cuerpo JSON `{ "username": "...", "email": "...", "full_name": "...", "hashed_password": "..." }`
- **Crear gasto**  
  `POST http://api.local/expenses/api/expenses` con `{ "user_id": 1, "amount": 10.5, "category": "food", "description": "...", "date": "2024-01-15" }`
- **Listar gastos**  
  `GET http://api.local/expenses/api/expenses?user_id=1`
- **Reportes**  
  - Mensual: `GET http://api.local/reports/monthly?user_id=1&year=2024&month=01`  
  - Por categoría: `GET http://api.local/reports/by-category?user_id=1`  
  - Rango: `GET http://api.local/reports/range?user_id=1&start=2024-01-01&end=2024-01-31`

## Ejecución local (sin Kubernetes)
```bash
cd services/auth-service    # o expenses-service / reporting-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Variables como `ROOT_PATH`, `DB_DIR` y `DB_NAME` pueden sobreescribirse con env vars o `.env` (auth/expenses cargan `.env` automáticamente).
