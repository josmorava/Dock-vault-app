# Plan de Implementación — DocVault

## Fase 0 — Scaffolding (esta sesión)
- Crear repo git y estructura `backend/` + `frontend/` + `mobile/`.
- Configurar Docker Compose (Postgres + backend + frontend dev server).
- Django project base + `inertia-django` + primera página Vue renderizando ("Hello DocVault").
- Tailwind configurado con la paleta de `04-UIUX-Design-Brief.md`.

## Fase 1 — Auth y ajustes
- Modelo `User` custom + login/logout.
- Middleware de expiración de sesión por inactividad.
- Página `/settings`: cambiar email, cambiar contraseña, crear usuario (admin).

## Fase 2 — Módulo Documentos (core del producto)
- Modelos `Category`, `Tag`, `Document` + seed de categorías default.
- Integración storage B2 (`django-storages`) con URLs firmadas.
- Upload con validación de tipo/tamaño.
- Listado con búsqueda + filtros (categoría, tag).
- Detalle, edición, reemplazo de archivo, eliminación con confirmación.

## Fase 3 — Módulo Notas
- Modelo `Note` + CRUD completo (listado, crear, editar, eliminar).

## Fase 4 — Pulido UI/UX + responsive
- Layouts mobile-first, dark mode, empty states, toasts.
- BottomNav mobile / Sidebar desktop.

## Fase 5 — Capacitor / Mobile
- Envolver frontend con Capacitor.
- Plugin Cámara para upload directo.
- Pull-to-refresh, swipe actions, Haptics.
- Build APK de prueba para instalar en el teléfono.

## Fase 6 — Deploy a producción
- Provisionar Railway/Fly.io + Postgres gestionado.
- Configurar bucket B2 (prod) separado del de desarrollo.
- Variables de entorno y secretos.
- Cron de backups (`pg_dump` → B2 backups bucket).
- Deploy inicial + smoke test desde el teléfono.

## Fase 7 — Testing y cierre MVP
- Tests backend (permisos/aislamiento por usuario, upload/download).
- E2E Playwright del flujo completo.
- Checklist de seguridad básica antes de subir documentos reales de identidad.

---

**Siguiente paso inmediato:** Fase 0 — crear la estructura de carpetas del proyecto en `/home/jose/Documentos/DocVault App/` (fuera de esta carpeta `docs/`, en la raíz del proyecto).
