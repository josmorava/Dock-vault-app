<script setup lang="ts">
import { Link, router } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";
import LocaleThemeSwitcher from "../Components/LocaleThemeSwitcher.vue";

const { t } = useI18n();

function logout() {
  router.post("/logout");
}
</script>

<template>
  <div class="min-h-screen flex flex-col md:flex-row">
    <aside class="hidden md:flex md:w-56 md:flex-col md:justify-between gap-1 border-r border-gray-200 dark:border-gray-800 p-4">
      <div class="flex flex-col gap-1">
        <Link href="/documents" class="rounded-lg px-3 py-2 hover:bg-accent/10 font-medium">{{ t("nav.documents") }}</Link>
        <Link href="/notes" class="rounded-lg px-3 py-2 hover:bg-accent/10 font-medium">{{ t("nav.notes") }}</Link>
        <Link href="/settings" class="rounded-lg px-3 py-2 hover:bg-accent/10 font-medium">{{ t("nav.settings") }}</Link>
      </div>
      <button
        type="button"
        class="text-left rounded-lg px-3 py-2 text-sm text-gray-500 hover:bg-red-500/10 hover:text-red-600"
        @click="logout"
      >
        {{ t("logout") }}
      </button>
    </aside>

    <div class="flex-1 flex flex-col">
      <header class="flex justify-end p-4">
        <LocaleThemeSwitcher />
      </header>

      <main class="flex-1 px-4 pb-20 md:pb-4">
        <slot />
      </main>
    </div>

    <nav
      class="md:hidden fixed bottom-0 inset-x-0 bg-surface-light dark:bg-surface-dark border-t border-gray-200 dark:border-gray-800 flex justify-around py-2"
      style="padding-bottom: env(safe-area-inset-bottom)"
    >
      <Link href="/documents" class="text-sm font-medium">{{ t("nav.documents") }}</Link>
      <Link href="/notes" class="text-sm font-medium">{{ t("nav.notes") }}</Link>
      <Link href="/settings" class="text-sm font-medium">{{ t("nav.settings") }}</Link>
    </nav>
  </div>
</template>
