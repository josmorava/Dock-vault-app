# PRD — DocVault
Product Requirements Document

## 1. Resumen
DocVault es una aplicación personal para almacenar, organizar y consultar documentos importantes (cédula, pasaporte, permiso de trabajo, documentos médicos, títulos académicos, etc.) junto con notas asociadas. Complementa esto con un módulo simple de notas generales. Uso personal, sin dominio dedicado, pensado para escalar a un pequeño número de usuarios (familia).

## 2. Problema a resolver
Documentos importantes están dispersos entre email, WhatsApp, fotos del teléfono y carpetas locales, sin organización ni forma rápida de encontrarlos cuando se necesitan (trámites, citas médicas, renovaciones).

## 3. Usuarios
- **Fase 1:** un solo usuario (operaciones@corpus.global), uso de prueba.
- **Fase 2:** multiusuario, cada cuenta ve únicamente sus propios documentos y notas (aislamiento total por usuario, sin compartición cross-usuario en esta fase).

## 4. Alcance funcional (Fase 1)

### 4.1 Autenticación y cuenta
- Login con email + contraseña.
- Expiración de sesión por inactividad (timeout configurable, default 30 min).
- Panel de ajustes:
  - Cambiar email.
  - Cambiar contraseña.
  - Crear nuevo usuario (admin puede invitar/crear cuentas).
  - Ver/editar perfil básico (nombre).

### 4.2 Módulo Documentos
- Subir documento (imagen JPG/PNG/HEIC, PDF, Word/Excel).
- Al subir: seleccionar **categoría** (de una lista predefinida, gestionable) y opcionalmente **tags** libres.
- Agregar una **nota** asociada al documento (texto libre, ej: "Título universitario 2016 - pendiente por firma 2026").
- Listado de documentos con:
  - Búsqueda por nombre/nota.
  - Filtro por categoría.
  - Filtro por tag.
- Ver documento (preview en el caso de imágenes/PDF).
- Descargar documento original.
- Actualizar: reemplazar archivo, editar categoría/tags/nota.
- Eliminar documento (con confirmación).

### 4.3 Módulo Notas
- CRUD simple de notas independientes (título + contenido + fecha).
- Notas por documento (ya cubiertas en 4.2) coexisten como funcionalidad separada del CRUD general de notas.

### 4.4 Categorías predefinidas (editable a futuro)
Identidad, Educación, Salud, Legal, Finanzas, Vehículos, Vivienda, Otros.

## 5. Requisitos no funcionales
- **Responsive** — mobile-first, ya que se usará empaquetado con Capacitor como app de teléfono.
- **Seguridad:** HTTPS obligatorio, expiración de sesión por inactividad. (2FA y cifrado en reposo quedan como mejoras futuras, ver `06-Futuras-Mejoras.md`).
- **Privacidad:** los archivos contienen datos de identidad — nunca se exponen vía URLs públicas no firmadas; todo acceso a archivos pasa por el backend autenticado (URLs firmadas de corta duración si se usa storage tipo S3).
- **Disponibilidad:** app de uso personal, no requiere SLA alto, pero sí backups periódicos de DB y archivos.

## 6. Fuera de alcance (Fase 1)
- Compartir documentos con terceros vía link.
- OCR / extracción automática de datos.
- Recordatorios de vencimiento.
- 2FA.
- Cifrado de archivos en reposo a nivel de aplicación.

## 7. Métricas de éxito (uso personal)
- Poder subir y encontrar cualquier documento en menos de 30 segundos desde el teléfono.
- Cero pérdida de datos (backups funcionando).
