# Esquema de Backend — DocVault

## 1. Apps Django

```
apps/
├── users/        # auth, perfil, sesión con expiración
├── documents/    # Document, Category, Tag
├── notes/        # Note
└── core/         # storage helpers, mixins de ownership
```

## 2. Modelos de datos

### users.User (custom, extiende AbstractUser)
| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| email | EmailField | unique, usado como username |
| name | CharField | |
| is_admin | Boolean | puede crear otros usuarios |
| session_timeout_minutes | Integer | default 30, configurable en ajustes |
| dark_mode_preference | CharField | `system` / `light` / `dark` |
| created_at / updated_at | DateTime | |

### documents.Category
| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| name | CharField | ej: "Identidad" |
| color | CharField | hex, para chip visual |
| owner | FK User | null=True si es categoría global de sistema |
| is_default | Boolean | categorías predefinidas del seed |

### documents.Tag
| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| name | CharField | único por usuario |
| owner | FK User | |

### documents.Document
| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| owner | FK User | índice, aislamiento de datos |
| name | CharField | nombre visible |
| file | FileField | storage backend S3/B2 |
| file_type | CharField | mime real detectado |
| file_size | Integer | bytes |
| category | FK Category | on_delete=PROTECT |
| tags | M2M Tag | |
| note | TextField | nota asociada al documento, opcional |
| created_at / updated_at | DateTime | |

Índices: `(owner, category)`, `(owner, created_at)`, búsqueda full-text sobre `name` + `note` (Postgres `SearchVector`).

### notes.Note (independiente)
| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| owner | FK User | |
| title | CharField | |
| content | TextField | |
| created_at / updated_at | DateTime | |

## 3. Reglas de negocio / permisos
- Todo queryset filtra siempre por `owner=request.user` — ningún endpoint debe permitir acceso cruzado entre usuarios (verificado con tests de permisos).
- `Category.is_default=True` son visibles para todos los usuarios (seed inicial); un usuario puede añadir categorías propias.
- Borrado de `Document` es hard-delete del registro + borrado del archivo en el storage (señal `post_delete`), no hay papelera en fase 1.
- Reemplazo de archivo en edición borra el archivo anterior del storage tras confirmar el nuevo upload.

## 4. Endpoints/Rutas Inertia (equivalentes REST internos)

| Método | Ruta | Acción |
|---|---|---|
| GET | `/login` | página login |
| POST | `/login` | autenticar |
| POST | `/logout` | cerrar sesión |
| GET | `/documents` | listado + filtros (`?q=&category=&tag=`) |
| POST | `/documents` | crear documento (multipart) |
| GET | `/documents/:id` | detalle |
| PUT | `/documents/:id` | editar metadata/nota |
| POST | `/documents/:id/replace` | reemplazar archivo |
| GET | `/documents/:id/download` | descarga autenticada (redirige a URL firmada) |
| DELETE | `/documents/:id` | eliminar |
| GET | `/categories` | listado (para selects/filtros) |
| GET | `/notes` | listado notas |
| POST | `/notes` | crear nota |
| PUT | `/notes/:id` | editar nota |
| DELETE | `/notes/:id` | eliminar nota |
| GET | `/settings` | página ajustes |
| PUT | `/settings/profile` | nombre |
| PUT | `/settings/email` | cambiar email (requiere password) |
| PUT | `/settings/password` | cambiar password |
| POST | `/settings/users` | crear usuario (solo admin) |

## 5. Middleware de expiración de sesión
- Middleware custom `SessionActivityMiddleware`: en cada request autenticado, compara `now - last_activity` contra `session_timeout_minutes`; si excede, hace `logout()` y responde 401/redirect a `/login` con mensaje. Actualiza `last_activity` en cada request válido.

## 6. Storage helper (`core/storage.py`)
- Wrapper sobre `django-storages` para:
  - Generar key de archivo (`{user_id}/{document_id}/{filename}`).
  - Generar URL firmada de descarga (expira en 5 min).
  - Validar tipo real de archivo (`python-magic`) contra whitelist.
  - Borrar archivo del bucket al eliminar/reemplazar documento.

## 7. Seed inicial
- Comando `manage.py seed_categories` crea las 8 categorías default (`is_default=True`, `owner=None`) al desplegar.
