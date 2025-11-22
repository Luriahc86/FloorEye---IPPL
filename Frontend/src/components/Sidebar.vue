<template>
  <aside class="
      bg-white shadow-lg flex flex-col h-screen border-r
      w-64 lg:w-64
      fixed lg:static
      inset-y-0 left-0 z-40
    "
  >
    <!-- Header -->
    <div class="p-6 border-b flex items-center justify-between">
      <h1 class="text-2xl font-bold text-blue-600">FloorEye</h1>
      <button
        class="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
        @click="$emit('close-sidebar')"
      >
        ✕
      </button>
    </div>

    <!-- Navigation -->
    <nav class="p-4 space-y-2 flex-1 overflow-y-auto">

      <router-link :to="'/dashboard'" :class="linkClass('/dashboard')">
        <span class="text-xl mr-2">🏠</span> Dashboard
      </router-link>

      <router-link :to="'/kelola-staff'" :class="linkClass('/kelola-staff')">
        <span class="text-xl mr-2">👥</span> Kelola Staff
      </router-link>

      <router-link :to="'/kelola-cctv'" :class="linkClass('/kelola-cctv')">
        <span class="text-xl mr-2">📹</span> Kelola CCTV
      </router-link>

      <router-link :to="'/laporan'" :class="linkClass('/laporan')">
        <span class="text-xl mr-2">🧾</span> Laporan Kebersihan
      </router-link>

    </nav>

    <!-- Logout -->
    <div class="p-4 border-t mt-auto">
      <button
        class="w-full py-2 rounded-lg flex items-center justify-center gap-2 
               text-red-600 hover:bg-red-50 transition"
        @click="logout"
      >
        🚪 Keluar
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

function logout() {
  router.push("/")
}

function linkClass(path) {
  const active = route.path === path

  return [
    "flex items-center px-4 py-3 rounded-lg font-medium transition",
    active
      ? "bg-blue-600 text-white shadow"
      : "text-gray-700 hover:bg-blue-50 hover:text-blue-700"
  ]
}
</script>

<style scoped>
/* Optional smooth scrolling inside sidebar */
nav::-webkit-scrollbar {
  width: 6px;
}
nav::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
</style>