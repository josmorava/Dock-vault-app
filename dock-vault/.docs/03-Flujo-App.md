# Flujo de la App — DocVault

## 1. Mapa de navegación

```
/login
  └─► /documents (home tras login)
        ├─► /documents?category=X&tag=Y&q=texto   (filtros/búsqueda)
        ├─► /documents/new                         (modal/página de subida)
        ├─► /documents/:id                         (detalle: preview + nota + metadata)
        │     ├─► editar (categoría, tags, nota, reemplazar archivo)
        │     ├─► descargar
        │     └─► eliminar (confirmación)
        ├─► /notes                                  (listado de notas independientes)
        │     ├─► /notes/new
        │     └─► /notes/:id (editar/eliminar)
        └─► /settings
              ├─► perfil (nombre)
              ├─► cambiar email
              ├─► cambiar contraseña
              └─► usuarios (crear nuevo usuario) [fase multiusuario]
```

## 2. Flujo: Login
1. Usuario abre la app → si no hay sesión activa, redirige a `/login`.
2. Ingresa email + contraseña.
3. Si falla 5 veces → bloqueo temporal (django-axes).
4. Login exitoso → redirige a `/documents`.
5. Sesión inactiva > 30 min → próxima acción fuerza logout con mensaje "Tu sesión expiró".

## 3. Flujo: Subir documento
1. Desde `/documents`, botón flotante "+" (mobile) o botón "Subir documento" (desktop).
2. Modal/página con:
   - Selector de archivo (o botón cámara en mobile vía Capacitor).
   - Nombre del documento (autocompletado del filename, editable).
   - Selector de categoría (dropdown, obligatorio).
   - Campo de tags (input tipo chips, libre, opcional).
   - Campo de nota (textarea, opcional).
3. Preview antes de confirmar (thumbnail si es imagen, ícono si es PDF/Office).
4. Confirmar → upload con barra de progreso → toast de éxito → vuelve al listado con el nuevo doc arriba.

## 4. Flujo: Buscar/filtrar documentos
1. Barra de búsqueda superior (busca en nombre + nota).
2. Chips de categoría debajo de la barra (tap para filtrar, multi-tap desactiva).
3. Filtro de tags secundario (colapsable en mobile).
4. Resultados se actualizan en tiempo real (debounce 300ms) sin recargar página (Inertia partial reload).

## 5. Flujo: Ver/editar/eliminar documento
1. Tap/click en tarjeta de documento → vista detalle con preview grande.
2. Acciones: Descargar / Editar / Eliminar.
3. **Mobile:** swipe izquierda sobre la tarjeta en el listado revela accesos directos a Editar/Eliminar sin entrar al detalle.
4. Eliminar siempre pide confirmación (modal "¿Eliminar [nombre]? Esta acción no se puede deshacer").

## 6. Flujo: Notas
1. `/notes` lista notas independientes ordenadas por fecha de edición.
2. "+" nueva nota → título + contenido → guardar.
3. Notas por documento se editan directamente desde el detalle del documento (no aparecen en `/notes`, están claramente diferenciadas en UI con un ícono/label "Nota del documento").

## 7. Flujo: Ajustes
1. `/settings` con tabs: Perfil, Seguridad, Usuarios (si aplica rol admin).
2. Cambiar email → confirma con contraseña actual.
3. Cambiar contraseña → pide contraseña actual + nueva + confirmación.
4. Crear usuario (fase multiusuario) → email + nombre → invitación con contraseña temporal o link de set-password.

## 8. Interacciones móviles (Capacitor)
- **Pull-to-refresh** en `/documents` y `/notes` para recargar listado.
- **Swipe actions** en tarjetas de lista (editar/eliminar).
- **Cámara nativa** en el flujo de subida (botón "Tomar foto" además de "Elegir archivo").
- **Modo oscuro** que respeta la configuración del sistema operativo, con toggle manual en ajustes.
