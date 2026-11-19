# UI/UX Design Brief — DocVault

## 1. Principios
- **Simple y ordenado**: jerarquía visual clara, poco ruido, prioridad al contenido (documentos).
- **Color con propósito**: paleta mayormente neutra con un color de acento vibrante que marque acciones y categorías, evitando saturar la pantalla.
- **Mobile-first**: cada pantalla se diseña primero para 375px de ancho y luego se expande a desktop.

## 2. Paleta de colores (propuesta)

| Uso | Light | Dark |
|---|---|---|
| Fondo base | `#F7F8FA` | `#0F1115` |
| Superficie/tarjeta | `#FFFFFF` | `#1A1D23` |
| Texto principal | `#1A1D23` | `#F2F3F5` |
| Texto secundario | `#6B7280` | `#9CA3AF` |
| Acento primario | `#4F46E5` (indigo) | `#818CF8` |
| Acento secundario | `#0EA5A4` (teal) | `#2DD4BF` |
| Éxito | `#16A34A` | `#4ADE80` |
| Advertencia | `#D97706` | `#FBBF24` |
| Error | `#DC2626` | `#F87171` |
| Borde/divisor | `#E5E7EB` | `#2A2E37` |

- Cada **categoría** de documento tiene un color de identificación sutil (chip de color) para escaneo visual rápido en el listado: Identidad (indigo), Educación (teal), Salud (rojo suave), Legal (ámbar), Finanzas (verde), Vehículos (azul), Vivienda (violeta), Otros (gris).

## 3. Tipografía
- Fuente: **Inter** (system-ui fallback), ya coherente con Tailwind defaults.
- Escala: `text-2xl` títulos de página, `text-lg` títulos de tarjeta, `text-sm` metadata/fecha, `text-base` contenido general.

## 4. Componentes clave

### DocumentCard (listado)
- Thumbnail/ícono de tipo de archivo a la izquierda.
- Nombre del documento + chip de categoría con color.
- Tags como chips pequeños debajo.
- Nota truncada a 1 línea (si existe) con ícono de nota.
- Fecha de subida/actualización a la derecha (desktop) o debajo (mobile).
- Swipe izquierda en mobile revela: Editar (ámbar) / Eliminar (rojo).

### UploadModal
- Drag & drop en desktop; en mobile, botones grandes "Tomar foto" / "Elegir archivo".
- Preview inmediato del archivo seleccionado.
- Formulario compacto: categoría (select con color), tags (input chips), nota (textarea colapsable).

### FilterBar
- Search input siempre visible arriba.
- Chips de categoría horizontales scrolleables en mobile (`overflow-x-auto`).
- Contador de resultados visible ("12 documentos").

### BottomNav (mobile) / Sidebar (desktop)
- 3 secciones: Documentos, Notas, Ajustes.
- Ícono + label, acento de color en el ítem activo.

### Empty states
- Ilustración simple + mensaje amigable + CTA ("Aún no tienes documentos. Sube el primero.") — nunca pantallas vacías sin guía.

## 5. Patrones móviles nativos (Capacitor)
- **Pull-to-refresh**: indicador circular con el color de acento, al soltar recarga el listado.
- **Swipe actions**: fricción/threshold estándar de iOS/Android (usar librería tipo `vue3-touch-events` o gestos nativos de Capacitor).
- **Safe areas**: respetar notch/home indicator (`env(safe-area-inset-*)` en CSS).
- **Feedback táctil**: pequeña vibración (Haptics de Capacitor) al confirmar eliminar o completar upload.

## 6. Modo oscuro
- Activado por `prefers-color-scheme` + toggle manual persistente en ajustes (localStorage).
- Todos los componentes definidos con variantes `dark:` de Tailwind desde el inicio, no como parche posterior.

## 7. Accesibilidad
- Contraste mínimo AA en todos los textos sobre fondo.
- Tamaño de tap-target mínimo 44x44px en mobile.
- Confirmaciones de eliminar siempre explícitas (nunca swipe-to-delete instantáneo sin confirmación para documentos, dado que son irremplazables).
