<script setup lang="ts">
import { useI18n } from "vue-i18n";
import AppLayout from "../../Layouts/AppLayout.vue";

interface DocItem {
  id: string;
  name: string;
  category: { name: string; color: string };
  tags: { id: string; name: string }[];
  note: string;
  created_at: string;
}

defineProps<{ documents: DocItem[]; categories: { id: string; name: string; color: string }[] }>();

const { t } = useI18n();
</script>

<template>
  <AppLayout>
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-2xl font-semibold">{{ t("documents.title") }}</h1>
      <button class="rounded-lg bg-accent text-white px-4 py-2 text-sm font-medium">{{ t("documents.upload") }}</button>
    </div>

    <div v-if="documents.length === 0" class="text-center py-16 text-gray-500">
      {{ t("documents.empty") }}
    </div>

    <div v-else class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="doc in documents"
        :key="doc.id"
        class="bg-surface-light dark:bg-surface-dark rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-800"
      >
        <div class="flex items-center gap-2 mb-2">
          <span
            class="text-xs px-2 py-0.5 rounded-full"
            :style="{ backgroundColor: doc.category.color + '22', color: doc.category.color }"
          >
            {{ doc.category.name }}
          </span>
        </div>
        <h2 class="font-medium">{{ doc.name }}</h2>
        <p v-if="doc.note" class="text-sm text-gray-500 truncate">{{ doc.note }}</p>
      </div>
    </div>
  </AppLayout>
</template>
