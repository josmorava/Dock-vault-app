import { createI18n } from "vue-i18n";

const LOCALE_KEY = "docvault-locale";

const messages = {
  es: {
    nav: { documents: "Documentos", notes: "Notas", settings: "Ajustes" },
    language: { label: "Idioma" },
    login: {
      title: "DocVault",
      subtitle: "Tus documentos importantes, siempre a la mano.",
      email: "Email",
      password: "Contraseña",
      submit: "Entrar",
    },
    documents: {
      title: "Documentos",
      upload: "+ Subir documento",
      empty: "Aún no tienes documentos. Sube el primero.",
    },
    notes: {
      title: "Notas",
      new: "+ Nueva nota",
      empty: "Aún no tienes notas.",
    },
    settings: {
      title: "Ajustes",
      tabProfile: "Perfil",
      tabSecurity: "Seguridad",
      tabUsers: "Usuarios",
      name: "Nombre",
      email: "Email",
      sessionTimeout: "Expira sesión tras",
      minutesInactivity: "minutos de inactividad",
      save: "Guardar",
      saved: "Guardado",
      currentPassword: "Contraseña actual",
      newEmail: "Nuevo email",
      newPassword: "Nueva contraseña",
      confirmPassword: "Confirmar nueva contraseña",
      changeEmail: "Cambiar email",
      changePassword: "Cambiar contraseña",
      newUserTitle: "Crear usuario",
      newUserName: "Nombre",
      newUserEmail: "Email",
      newUserPassword: "Contraseña temporal",
      createUser: "Crear usuario",
      existingUsers: "Usuarios existentes",
      adminBadge: "Admin",
    },
    theme: { toggleToDark: "Cambiar a modo oscuro", toggleToLight: "Cambiar a modo claro" },
    logout: "Cerrar sesión",
  },
  en: {
    nav: { documents: "Documents", notes: "Notes", settings: "Settings" },
    language: { label: "Language" },
    login: {
      title: "DocVault",
      subtitle: "Your important documents, always at hand.",
      email: "Email",
      password: "Password",
      submit: "Sign in",
    },
    documents: {
      title: "Documents",
      upload: "+ Upload document",
      empty: "You don't have any documents yet. Upload the first one.",
    },
    notes: {
      title: "Notes",
      new: "+ New note",
      empty: "You don't have any notes yet.",
    },
    settings: {
      title: "Settings",
      tabProfile: "Profile",
      tabSecurity: "Security",
      tabUsers: "Users",
      name: "Name",
      email: "Email",
      sessionTimeout: "Session expires after",
      minutesInactivity: "minutes of inactivity",
      save: "Save",
      saved: "Saved",
      currentPassword: "Current password",
      newEmail: "New email",
      newPassword: "New password",
      confirmPassword: "Confirm new password",
      changeEmail: "Change email",
      changePassword: "Change password",
      newUserTitle: "Create user",
      newUserName: "Name",
      newUserEmail: "Email",
      newUserPassword: "Temporary password",
      createUser: "Create user",
      existingUsers: "Existing users",
      adminBadge: "Admin",
    },
    theme: { toggleToDark: "Switch to dark mode", toggleToLight: "Switch to light mode" },
    logout: "Log out",
  },
};

function readInitialLocale(): "es" | "en" {
  const stored = localStorage.getItem(LOCALE_KEY);
  return stored === "en" ? "en" : "es";
}

export const i18n = createI18n({
  legacy: false,
  locale: readInitialLocale(),
  fallbackLocale: "es",
  messages,
});

export function setLocale(locale: "es" | "en") {
  i18n.global.locale.value = locale;
  localStorage.setItem(LOCALE_KEY, locale);
}
