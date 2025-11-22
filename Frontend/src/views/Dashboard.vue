<template>
  <div class="dashboard p-8 space-y-6">
    <!-- TITLE -->
    <h1 class="text-3xl font-bold text-gray-800">Dashboard</h1>
    <p class="text-gray-500">
      Selamat datang di sistem monitoring kebersihan FloorEye.
    </p>

    <!-- CARD STATISTIC -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="p-6 bg-white shadow rounded-xl">
        <p class="text-sm text-gray-500">Total Staff</p>
        <p class="text-3xl font-bold">0</p>
      </div>

      <div class="p-6 bg-white shadow rounded-xl">
        <p class="text-sm text-gray-500">CCTV Aktif</p>
        <p class="text-3xl font-bold">0</p>
      </div>

      <div class="p-6 bg-white shadow rounded-xl">
        <p class="text-sm text-gray-500">Laporan Pending</p>
        <p class="text-3xl font-bold">0</p>
      </div>

      <div class="p-6 bg-white shadow rounded-xl">
        <p class="text-sm text-gray-500">Area Bersih</p>
        <p class="text-3xl font-bold">0</p>
      </div>
    </div>

    <!-- SECTION LAPORAN TERBARU -->
    <div class="p-6 bg-white shadow rounded-xl">
      <h2 class="text-xl font-semibold mb-2">Laporan Terbaru</h2>
      <p class="text-gray-500 mb-4">Belum ada laporan hari ini.</p>
    </div>
  </div>
</template>

<script setup>
// Tidak ada Sidebar
</script>

<style scoped>
.dashboard {
  background-color: #f9fafb;
  min-height: 100vh;
}
</style>
