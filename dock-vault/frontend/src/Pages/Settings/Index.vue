<script setup lang="ts">
import { router, useForm } from "@inertiajs/vue3";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import AppLayout from "../../Layouts/AppLayout.vue";

interface UserSummary {
  id: string;
  email: string;
  name: string;
  is_admin: boolean;
}

const props = defineProps<{
  user: { email: string; name: string; session_timeout_minutes: number; is_admin: boolean };
  users?: UserSummary[];
  errors?: Record<string, string>;
}>();

const { t } = useI18n();

const tab = ref<"profile" | "security" | "users">("profile");
const savedFlag = ref<string | null>(null);

function flashSaved(key: string) {
  savedFlag.value = key;
  setTimeout(() => {
    if (savedFlag.value === key) savedFlag.value = null;
  }, 2000);
}

const profileForm = useForm({ name: props.user.name });
function submitProfile() {
  profileForm.put("/settings/profile", { onSuccess: () => flashSaved("profile") });
}

const emailForm = useForm({ email: props.user.email, current_password: "" });
function submitEmail() {
  emailForm.put("/settings/email", {
    onSuccess: () => {
      emailForm.current_password = "";
      flashSaved("email");
    },
  });
}

const passwordForm = useForm({ current_password: "", new_password: "", new_password_confirmation: "" });
function submitPassword() {
  passwordForm.put("/settings/password", {
    onSuccess: () => {
      passwordForm.reset();
      flashSaved("password");
    },
  });
}

const newUserForm = useForm({ name: "", email: "", password: "" });
function submitNewUser() {
  newUserForm.post("/settings/users", {
    onSuccess: () => {
      newUserForm.reset();
      flashSaved("new_user");
    },
  });
}

function logout() {
  router.post("/logout");
}
</script>

<template>
  <AppLayout>
    <h1 class="text-2xl font-semibold mb-4">{{ t("settings.title") }}</h1>

    <div class="flex gap-2 mb-4 border-b border-gray-200 dark:border-gray-800">
      <button
        type="button"
        class="px-3 py-2 text-sm font-medium border-b-2 -mb-px"
        :class="tab === 'profile' ? 'border-accent text-accent' : 'border-transparent text-gray-500'"
        @click="tab = 'profile'"
      >
        {{ t("settings.tabProfile") }}
      </button>
      <button
        type="button"
        class="px-3 py-2 text-sm font-medium border-b-2 -mb-px"
        :class="tab === 'security' ? 'border-accent text-accent' : 'border-transparent text-gray-500'"
        @click="tab = 'security'"
      >
        {{ t("settings.tabSecurity") }}
      </button>
      <button
        v-if="user.is_admin"
        type="button"
        class="px-3 py-2 text-sm font-medium border-b-2 -mb-px"
        :class="tab === 'users' ? 'border-accent text-accent' : 'border-transparent text-gray-500'"
        @click="tab = 'users'"
      >
        {{ t("settings.tabUsers") }}
      </button>
    </div>

    <!-- Perfil -->
    <div v-if="tab === 'profile'" class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm max-w-md space-y-4">
      <div>
        <span class="text-sm text-gray-500">{{ t("settings.email") }}</span>
        <p class="font-medium">{{ user.email }}</p>
      </div>
      <div>
        <span class="text-sm text-gray-500">{{ t("settings.sessionTimeout") }}</span>
        <p class="font-medium">{{ user.session_timeout_minutes }} {{ t("settings.minutesInactivity") }}</p>
      </div>

      <form class="space-y-2 pt-2 border-t border-gray-100 dark:border-gray-800" @submit.prevent="submitProfile">
        <label class="block text-sm font-medium">{{ t("settings.name") }}</label>
        <input v-model="profileForm.name" type="text" class="w-full rounded-lg border px-3 py-2" />
        <button
          type="submit"
          class="rounded-lg bg-accent text-white px-4 py-2 text-sm font-medium disabled:opacity-50"
          :disabled="profileForm.processing"
        >
          {{ savedFlag === "profile" ? t("settings.saved") : t("settings.save") }}
        </button>
      </form>
    </div>

    <!-- Seguridad -->
    <div v-else-if="tab === 'security'" class="space-y-4 max-w-md">
      <form
        class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm space-y-2"
        @submit.prevent="submitEmail"
      >
        <h2 class="font-medium mb-1">{{ t("settings.changeEmail") }}</h2>
        <label class="block text-sm font-medium">{{ t("settings.newEmail") }}</label>
        <input v-model="emailForm.email" type="email" class="w-full rounded-lg border px-3 py-2" />
        <label class="block text-sm font-medium">{{ t("settings.currentPassword") }}</label>
        <input v-model="emailForm.current_password" type="password" class="w-full rounded-lg border px-3 py-2" />
        <p v-if="errors?.email" class="text-sm text-red-600">{{ errors.email }}</p>
        <button
          type="submit"
          class="rounded-lg bg-accent text-white px-4 py-2 text-sm font-medium disabled:opacity-50"
          :disabled="emailForm.processing"
        >
          {{ savedFlag === "email" ? t("settings.saved") : t("settings.save") }}
        </button>
      </form>

      <form
        class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm space-y-2"
        @submit.prevent="submitPassword"
      >
        <h2 class="font-medium mb-1">{{ t("settings.changePassword") }}</h2>
        <label class="block text-sm font-medium">{{ t("settings.currentPassword") }}</label>
        <input v-model="passwordForm.current_password" type="password" class="w-full rounded-lg border px-3 py-2" />
        <label class="block text-sm font-medium">{{ t("settings.newPassword") }}</label>
        <input v-model="passwordForm.new_password" type="password" class="w-full rounded-lg border px-3 py-2" />
        <label class="block text-sm font-medium">{{ t("settings.confirmPassword") }}</label>
        <input
          v-model="passwordForm.new_password_confirmation"
          type="password"
          class="w-full rounded-lg border px-3 py-2"
        />
        <p v-if="errors?.password" class="text-sm text-red-600">{{ errors.password }}</p>
        <button
          type="submit"
          class="rounded-lg bg-accent text-white px-4 py-2 text-sm font-medium disabled:opacity-50"
          :disabled="passwordForm.processing"
        >
          {{ savedFlag === "password" ? t("settings.saved") : t("settings.save") }}
        </button>
      </form>
    </div>

    <!-- Usuarios (admin) -->
    <div v-else-if="tab === 'users'" class="space-y-4 max-w-md">
      <form
        class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm space-y-2"
        @submit.prevent="submitNewUser"
      >
        <h2 class="font-medium mb-1">{{ t("settings.newUserTitle") }}</h2>
        <label class="block text-sm font-medium">{{ t("settings.newUserName") }}</label>
        <input v-model="newUserForm.name" type="text" class="w-full rounded-lg border px-3 py-2" />
        <label class="block text-sm font-medium">{{ t("settings.newUserEmail") }}</label>
        <input v-model="newUserForm.email" type="email" class="w-full rounded-lg border px-3 py-2" />
        <label class="block text-sm font-medium">{{ t("settings.newUserPassword") }}</label>
        <input v-model="newUserForm.password" type="password" class="w-full rounded-lg border px-3 py-2" />
        <p v-if="errors?.new_user" class="text-sm text-red-600">{{ errors.new_user }}</p>
        <button
          type="submit"
          class="rounded-lg bg-accent text-white px-4 py-2 text-sm font-medium disabled:opacity-50"
          :disabled="newUserForm.processing"
        >
          {{ savedFlag === "new_user" ? t("settings.saved") : t("settings.createUser") }}
        </button>
      </form>

      <div class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm">
        <h2 class="font-medium mb-2">{{ t("settings.existingUsers") }}</h2>
        <ul class="space-y-2">
          <li v-for="u in users" :key="u.id" class="flex items-center justify-between text-sm">
            <span>{{ u.name || u.email }} <span class="text-gray-500">({{ u.email }})</span></span>
            <span v-if="u.is_admin" class="text-xs px-2 py-0.5 rounded-full bg-accent/10 text-accent">
              {{ t("settings.adminBadge") }}
            </span>
          </li>
        </ul>
      </div>
    </div>

    <button
      type="button"
      class="md:hidden mt-6 text-sm text-red-600 font-medium"
      @click="logout"
    >
      {{ t("logout") }}
    </button>
  </AppLayout>
</template>
