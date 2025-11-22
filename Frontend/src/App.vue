<template>
  <div class="min-h-screen flex">

    <!-- Sidebar -->
    <Sidebar v-if="showSidebar" />

    <!-- Halaman utama -->
    <main
      :class="showSidebar ? 'flex-1 p-0 lg:ml-0' : 'w-full p-0'"
      class="transition-all"
    >
      <RouterView />
    </main>

  </div>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue"
import { useRoute } from "vue-router"
import { computed } from "vue"

const route = useRoute()

// halaman auth tanpa sidebar
const hidePaths = ["/", "/register", "/forgot-password"]

// computed = reactive → selalu update kalau route berubah
const showSidebar = computed(() => !hidePaths.includes(route.path))
</script>
