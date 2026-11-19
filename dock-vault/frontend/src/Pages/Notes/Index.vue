<script setup lang="ts">
import { useI18n } from "vue-i18n";
import AppLayout from "../../Layouts/AppLayout.vue";

interface NoteItem {
  id: string;
  title: string;
  content: string;
  updated_at: string;
}

defineProps<{ notes: NoteItem[] }>();

const { t } = useI18n();
</script>

<template>
  <AppLayout>
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-semibold">{{ t("notes.title") }}</h1>
      <button class="rounded-lg bg-accent2 text-white px-4 py-2 text-sm font-medium">{{ t("notes.new") }}</button>
    </div>

    <div v-if="notes.length === 0" class="text-center py-16 text-gray-500">{{ t("notes.empty") }}</div>

    <div v-else class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="note in notes"
        :key="note.id"
        class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-800"
      >
        <h2 class="font-medium mb-1">{{ note.title }}</h2>
        <p class="text-sm text-gray-500 line-clamp-3">{{ note.content }}</p>
      </div>
    </div>
  </AppLayout>
</template>
