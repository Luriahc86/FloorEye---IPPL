<template>
  <div class="laporan p-8">
    <h1 class="text-2xl font-bold mb-2">Laporan Kebersihan</h1>
    <p class="text-gray-600 mb-6">
      Riwayat dan status laporan kebersihan dari semua area
    </p>

    <!-- Filter dan Pencarian -->
    <div
      class="bg-white p-5 rounded-xl shadow mb-6 flex flex-wrap gap-3 items-center"
    >
      <div class="flex-1 min-w-[250px]">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari berdasarkan area..."
          class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <div>
        <select
          v-model="filterStatus"
          class="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400"
        >
          <option value="">Semua Status</option>
          <option value="Pending">Pending</option>
          <option value="Selesai">Selesai</option>
        </select>
      </div>

      <button
        @click="exportLaporan"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
      >
        ⬇️ Export
      </button>
    </div>

    <!-- Daftar Laporan -->
    <div class="bg-white p-6 rounded-xl shadow">
      <h2 class="font-semibold text-lg mb-4">
        Daftar Laporan ({{ filteredLaporan.length }})
      </h2>

      <div v-if="loading" class="text-gray-500 italic text-center py-6">
        Memuat laporan...
      </div>

      <div
        v-else-if="filteredLaporan.length === 0"
        class="text-gray-500 italic text-center py-6"
      >
        Tidak ada laporan ditemukan.
      </div>

      <div
        v-for="(lap, index) in filteredLaporan"
        :key="lap.id || index"
        class="border-b py-4 flex justify-between items-start"
      >
        <div>
          <p class="font-semibold text-blue-700">📍 {{ lap.area }}</p>
          <p class="text-gray-500 text-sm mb-2">{{ lap.deskripsi }}</p>

          <div class="flex flex-wrap gap-4 text-sm text-gray-600">
            <span>🕒 {{ formatDate(lap.tanggal) }}</span>
            <span>👷 Ditugaskan: {{ lap.petugas }}</span>
            <span>🤖 Dilaporkan oleh: {{ lap.sumber }}</span>
          </div>
        </div>

        <div class="flex flex-col items-end gap-2">
          <span
            class="px-3 py-1 text-xs font-semibold rounded-full"
            :class="
              lap.status === 'Pending'
                ? 'bg-yellow-100 text-yellow-700'
                : 'bg-green-100 text-green-700'
            "
          >
            {{ lap.status }}
          </span>
          <select
            :value="lap.status"
            @change="(e) => updateStatus(lap.id || index, e.target.value)"
            :disabled="loading"
            class="text-xs border rounded px-2 py-1 disabled:opacity-50"
          >
            <option value="Pending">Pending</option>
            <option value="Selesai">Selesai</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { getLaporanList, updateLaporanStatus } from "@/api/floorEye";

const searchQuery = ref("");
const filterStatus = ref("");
const laporanList = ref([]);
const loading = ref(false);

onMounted(() => {
  loadLaporanList();
});

async function loadLaporanList() {
  loading.value = true;
  const data = await getLaporanList();
  laporanList.value = Array.isArray(data) ? data : [];
  loading.value = false;
}

// Filter data berdasarkan pencarian & status
const filteredLaporan = computed(() => {
  return laporanList.value.filter((lap) => {
    const cocokCari = lap.area
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    const cocokStatus = filterStatus.value
      ? lap.status === filterStatus.value
      : true;
    return cocokCari && cocokStatus;
  });
});

function formatDate(dateString) {
  if (!dateString) return "Tidak diketahui";
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString("id-ID", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return dateString;
  }
}

async function updateStatus(id, newStatus) {
  loading.value = true;
  const result = await updateLaporanStatus(id, newStatus);

  if (result.error) {
    console.error("Gagal update status:", result.error);
    alert("Gagal update status laporan");
  }

  await loadLaporanList();
  loading.value = false;
}

async function exportLaporan() {
  const csvContent = [
    ["Area", "Deskripsi", "Tanggal", "Petugas", "Sumber", "Status"],
    ...filteredLaporan.value.map((lap) => [
      lap.area,
      lap.deskripsi,
      lap.tanggal,
      lap.petugas,
      lap.sumber,
      lap.status,
    ]),
  ]
    .map((row) => row.map((cell) => `"${cell}"`).join(","))
    .join("\n");

  const blob = new Blob([csvContent], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `laporan-${new Date().getTime()}.csv`;
  a.click();
  window.URL.revokeObjectURL(url);
}
</script>

<style scoped>
.laporan {
  background-color: #f9fafb;
  min-height: 100vh;
}
</style>
