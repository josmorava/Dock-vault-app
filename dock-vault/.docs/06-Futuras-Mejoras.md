# Futuras Mejoras — DocVault
Roadmap post-Fase 1, no bloqueante para el MVP.

## Seguridad
- 2FA (TOTP) para el login, dado que hay documentos de identidad.
- Cifrado de archivos en reposo a nivel de aplicación (cifrar antes de subir a B2, clave derivada del usuario).
- Log de auditoría (quién vio/descargó qué documento y cuándo).

## Documentos
- Fecha de vencimiento por documento (pasaporte, permiso de trabajo, licencias) + recordatorios (email/push) 30/15/7 días antes.
- OCR para extraer texto y sugerir fecha de vencimiento automáticamente al subir.
- Compartir un documento puntual vía link temporal firmado (para trámites con terceros).
- Papelera con retención de 30 días antes del borrado definitivo (en vez de hard-delete inmediato).
- Exportar todo el archivo personal en un ZIP de respaldo descargable.
- Versionado de documentos (historial de reemplazos, no solo el último archivo).

## Multiusuario
- Roles más granulares (admin / miembro) y posible compartición selectiva entre miembros de una misma familia/cuenta.
- Compartir una carpeta/categoría específica con otro usuario (ej. documentos de los hijos visibles para ambos padres).

## Mobile / Capacitor
- Notificaciones push para recordatorios de vencimiento.
- Modo offline con sincronización posterior (cache local de metadata, no de archivos completos).
- Biometría (Face ID/huella) como capa adicional antes de abrir la app, vía Capacitor.

## Infraestructura
- Dominio propio si el proyecto crece más allá de uso personal.
- Monitoreo básico (Sentry) para errores en producción.
- Backups verificados automáticamente (test de restauración periódico).
