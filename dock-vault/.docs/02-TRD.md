# TRD — DocVault
Technical Requirements Document

## 1. Stack tecnológico
Alineado con Legalys App / Corpus App para reuso de conocimiento y patrones.

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12 + Django 5.x |
| Puente Backend↔Frontend | Inertia.js (adapter Django: `inertia-django`) |
| Frontend | Vue 3 (Composition API) + TypeScript |
| Estilos | Tailwind CSS |
| Build frontend | Vite (en vez de webpack, más rápido para proyecto nuevo) |
| Base de datos | PostgreSQL |
| Storage de archivos | Backblaze B2 (S3-compatible) vía `django-storages` |
| Auth | Django auth (session-based) + `django-axes` (rate limit de login) |
| Mobile wrapper | Capacitor 6 |
| Contenedores | Docker + Docker Compose |
| Control de versiones | Git (repo propio, privado) |

## 2. Arquitectura general

```
┌─────────────┐      HTTPS       ┌──────────────────┐      S3 API      ┌─────────────┐
│  Vue 3 SPA  │ ───────────────► │  Django + Inertia │ ───────────────► │ Backblaze B2│
│ (Capacitor) │ ◄─────────────── │     Backend       │ ◄─────────────── │  (archivos) │
└─────────────┘   Inertia pages  └──────────────────┘                  └─────────────┘
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │ PostgreSQL  │
                                   └─────────────┘
```

- Inertia evita construir una API REST separada: Django devuelve "páginas" Inertia (JSON con props), Vue las renderiza. Mismo patrón que Legalys/Corpus.
- Los archivos **nunca** se sirven con URL pública directa: el backend genera URLs firmadas de corta duración (presigned URLs, expiración ~5 min) o hace streaming autenticado del archivo.

## 3. Estructura de carpetas (separación frontend/backend solicitada)

```
docvault/
├── backend/
│   ├── config/              # settings, urls, wsgi/asgi
│   ├── apps/
│   │   ├── users/           # auth, perfil, ajustes de cuenta
│   │   ├── documents/       # modelo Document, Category, Tag
│   │   ├── notes/           # modelo Note (independiente + por documento)
│   │   └── core/            # utilidades comunes (storage, mixins)
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── Pages/           # páginas Inertia (Login, Documents/Index, Notes/Index, Settings)
│   │   ├── Components/      # componentes reutilizables (DocumentCard, UploadModal, etc.)
│   │   ├── Layouts/         # AppLayout, AuthLayout
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts
├── mobile/                  # Capacitor (android/ ios/ generados aquí)
├── docker-compose.yml
├── docker-compose.prod.yml
└── docs/                    # (este mismo tipo de documentación, dentro del repo)
```

## 4. Seguridad
- HTTPS obligatorio en producción (gestionado por el proveedor de hosting).
- Sesión con expiración por inactividad: `SESSION_COOKIE_AGE` + middleware custom que actualiza `last_activity` y fuerza logout si excede el timeout (default 30 min, configurable en ajustes).
- CSRF protection nativo de Django + Inertia.
- Passwords con hashing Argon2 (`django.contrib.auth.hashers.Argon2PasswordHasher`).
- Archivos servidos solo vía backend autenticado (nunca bucket público).
- Rate limiting de login (`django-axes`) para evitar fuerza bruta.
- Preparado para 2FA y cifrado en reposo en fase 2 (ver `06-Futuras-Mejoras.md`), sin bloquear la arquitectura actual.

## 5. Storage de archivos — detalle
- Bucket privado en Backblaze B2.
- `django-storages` con backend S3Boto3, `AWS_QUERYSTRING_AUTH=True` para URLs firmadas.
- Naming de archivos: `{user_id}/{document_uuid}/{filename_original}` para evitar colisiones y facilitar borrado por usuario.
- Límite de tamaño por archivo: 25 MB (configurable).
- Tipos permitidos: `.jpg .jpeg .png .heic .pdf .doc .docx .xls .xlsx`.
- Validación de tipo real (magic bytes) en backend, no solo por extensión.

## 6. Despliegue (producción personal, sin dominio dedicado)
- **Hosting:** Railway o Fly.io (Docker-based, subdominio gratuito incluido, HTTPS automático).
- **DB:** Postgres gestionado por el mismo proveedor.
- **Backups:** cron diario/semanal `pg_dump` → sube a un bucket B2 separado de backups; retención 30 días.
- **CI simple:** GitHub Actions (lint + tests) antes de deploy manual o auto-deploy en push a `main`.

## 7. Testing
- Backend: `pytest-django` para modelos, permisos (aislamiento por usuario) y endpoints críticos (upload/download).
- Frontend: Vitest para componentes clave (UploadModal, DocumentList filtros).
- E2E: Playwright (como en Legalys `e2e/`) para flujo login → subir doc → filtrar → descargar → eliminar.
