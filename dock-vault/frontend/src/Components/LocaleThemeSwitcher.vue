<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useTheme } from "../composables/useTheme";
import { setLocale } from "../i18n";

const { locale, t } = useI18n();
const { theme, toggleTheme } = useTheme();

function onLocaleChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value as "es" | "en";
  setLocale(value);
}
</script>

<template>
  <div class="flex items-center gap-2">
    <select
      :value="locale"
      class="h-9 w-16 rounded-lg border border-gray-200 dark:border-gray-700 bg-surface-light dark:bg-surface-dark text-gray-700 dark:text-gray-200 text-sm font-medium text-center appearance-none cursor-pointer"
      :aria-label="t('language.label')"
      @change="onLocaleChange"
    >
      <option value="es">ES</option>
      <option value="en">EN</option>
    </select>

    <button
      type="button"
      class="h-9 w-9 flex items-center justify-center rounded-lg border border-gray-200 dark:border-gray-700 bg-surface-light dark:bg-surface-dark text-gray-500 dark:text-gray-300"
      :title="theme === 'dark' ? t('theme.toggleToLight') : t('theme.toggleToDark')"
      :aria-label="theme === 'dark' ? t('theme.toggleToLight') : t('theme.toggleToDark')"
      @click="toggleTheme"
    >
      <svg v-if="theme === 'dark'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
        <path d="M12 4.5a1 1 0 0 1-1-1V2a1 1 0 1 1 2 0v1.5a1 1 0 0 1-1 1Zm0 15a1 1 0 0 1 1 1V22a1 1 0 1 1-2 0v-1.5a1 1 0 0 1 1-1Zm9-7.5a1 1 0 0 1-1 1h-1.5a1 1 0 1 1 0-2H20a1 1 0 0 1 1 1ZM5.5 12a1 1 0 0 1-1 1H3a1 1 0 1 1 0-2h1.5a1 1 0 0 1 1 1Zm12.02-6.52a1 1 0 0 1 0 1.42l-1.06 1.06a1 1 0 1 1-1.42-1.42l1.06-1.06a1 1 0 0 1 1.42 0ZM8.46 17.44a1 1 0 0 1 0 1.42l-1.06 1.06a1 1 0 1 1-1.42-1.42l1.06-1.06a1 1 0 0 1 1.42 0Zm9.06 1.42a1 1 0 0 1-1.42 0l-1.06-1.06a1 1 0 1 1 1.42-1.42l1.06 1.06a1 1 0 0 1 0 1.42ZM6.98 6.98a1 1 0 0 1-1.42 0L4.5 5.92a1 1 0 1 1 1.42-1.42l1.06 1.06a1 1 0 0 1 0 1.42ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Z" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
        <path d="M21.64 13a1 1 0 0 0-1.05-.14 8.05 8.05 0 0 1-3.37.73 8.15 8.15 0 0 1-8.14-8.14c0-1.22.25-2.37.73-3.37A1 1 0 0 0 8.4 1.36 10.14 10.14 0 1 0 22.14 14.05a1 1 0 0 0-.5-1.05Z" />
      </svg>
    </button>
  </div>
</template>
