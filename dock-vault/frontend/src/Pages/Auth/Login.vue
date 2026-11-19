<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";
import LocaleThemeSwitcher from "../../Components/LocaleThemeSwitcher.vue";

defineProps<{ error?: string }>();

const { t } = useI18n();
const form = useForm({ email: "", password: "" });

function submit() {
  form.post("/login/submit");
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4 relative">
    <div class="absolute top-4 right-4">
      <LocaleThemeSwitcher />
    </div>

    <div class="w-full max-w-sm bg-surface-light dark:bg-surface-dark rounded-2xl shadow p-6">
      <h1 class="text-2xl font-semibold mb-1">{{ t("login.title") }}</h1>
      <p class="text-sm text-gray-500 mb-6">{{ t("login.subtitle") }}</p>

      <p v-if="error" class="mb-4 text-sm text-red-600">{{ error }}</p>

      <form class="space-y-4" @submit.prevent="submit">
        <div>
          <label class="block text-sm font-medium mb-1">{{ t("login.email") }}</label>
          <input v-model="form.email" type="email" required class="w-full rounded-lg border px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">{{ t("login.password") }}</label>
          <input v-model="form.password" type="password" required class="w-full rounded-lg border px-3 py-2" />
        </div>
        <button
          type="submit"
          class="w-full rounded-lg bg-accent text-white py-2 font-medium hover:opacity-90"
          :disabled="form.processing"
        >
          {{ t("login.submit") }}
        </button>
      </form>
    </div>
  </div>
</template>
