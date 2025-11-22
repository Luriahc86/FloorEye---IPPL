<template>
  <div class="kelola-cctv p-8">
    <h1 class="text-2xl font-bold mb-2">Kelola CCTV</h1>
    <p class="text-gray-600 mb-6">
      Tambah dan kelola link CCTV untuk monitoring otomatis
    </p>

    <div class="flex flex-wrap gap-8">
      <!-- Form Tambah CCTV -->
      <div class="w-full md:w-1/2 bg-white p-6 rounded-xl shadow">
        <h2 class="font-semibold text-lg mb-4">Tambah CCTV Baru</h2>
        <p class="text-sm text-gray-500 mb-4">
          Masukkan informasi CCTV untuk pemantauan area kebersihan
        </p>

        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Nama CCTV</label>
          <input
            v-model="nama"
            type="text"
            placeholder="CCTV Terminal 1A - Gate 1"
            :disabled="loading"
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          />
        </div>

        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Lokasi</label>
          <input
            v-model="lokasi"
            type="text"
            placeholder="Terminal 1A"
            :disabled="loading"
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          />
        </div>

        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Link RTSP/HTTP</label>
          <input
            v-model="link"
            type="text"
            placeholder="rtsp://192.168.1.100/stream"
            :disabled="loading"
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          />
        </div>

        <div
          v-if="errorMessage"
          class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-3"
        >
          {{ errorMessage }}
        </div>

        <button
          @click="tambahCCTV"
          :disabled="loading"
          class="bg-blue-600 text-white w-full py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {{ loading ? "Menambah..." : "+ Tambah CCTV" }}
        </button>
      </div>

      <!-- Daftar CCTV -->
      <div class="w-full md:w-1/3 bg-white p-6 rounded-xl shadow">
        <h2 class="font-semibold text-lg mb-4">
          Daftar CCTV ({{ cctvList.length }})
        </h2>

        <div
          v-if="cctvList.length === 0"
          class="text-gray-500 italic text-center py-6"
        >
          Belum ada CCTV terdaftar.
        </div>

        <div
          v-for="(cam, index) in cctvList"
          :key="cam.id || index"
          class="border-b py-4 flex justify-between items-start"
        >
          <div>
            <p class="font-medium">{{ cam.nama }}</p>
            <p class="text-sm text-gray-500 flex items-center gap-1">
              📍 {{ cam.lokasi }}
            </p>
            <p class="text-sm text-blue-500 break-all">{{ cam.link }}</p>
            <span
              class="inline-block mt-2 px-3 py-1 text-xs rounded-full font-semibold"
              :class="
                cam.aktif
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-200 text-gray-600'
              "
            >
              {{ cam.aktif ? "Aktif" : "Nonaktif" }}
            </span>
          </div>

          <div class="flex flex-col items-end gap-2">
            <button
              @click="toggleAktif(cam.id || index)"
              :disabled="loading"
              class="text-sm text-blue-600 hover:text-blue-800 underline disabled:opacity-50"
            >
              {{ cam.aktif ? "Nonaktifkan" : "Aktifkan" }}
            </button>
            <button
              @click="hapusCCTV(cam.id || index)"
              :disabled="loading"
              class="text-red-500 hover:text-red-700 disabled:opacity-50"
            >
              🗑
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getCCTVList,
  addCCTV,
  deleteCCTV,
  updateCCTVStatus,
} from "@/api/floorEye";

const nama = ref("");
const lokasi = ref("");
const link = ref("");
const cctvList = ref([]);
const loading = ref(false);
const errorMessage = ref("");

onMounted(() => {
  loadCCTVList();
});

async function loadCCTVList() {
  const data = await getCCTVList();
  cctvList.value = Array.isArray(data) ? data : [];
}

async function tambahCCTV() {
  if (!nama.value || !lokasi.value || !link.value) {
    errorMessage.value = "Lengkapi semua data!";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  const result = await addCCTV(nama.value, lokasi.value, link.value);

  if (result.error) {
    errorMessage.value = result.error || "Gagal menambah CCTV";
    loading.value = false;
    return;
  }

  await loadCCTVList();
  nama.value = "";
  lokasi.value = "";
  link.value = "";
  loading.value = false;
}

async function hapusCCTV(id) {
  if (!confirm("Yakin ingin menghapus CCTV ini?")) return;

  loading.value = true;
  const result = await deleteCCTV(id);

  if (result.error) {
    console.error("Gagal menghapus CCTV:", result.error);
    alert("Gagal menghapus CCTV");
  }

  await loadCCTVList();
  loading.value = false;
}

async function toggleAktif(id) {
  const cctv = cctvList.value.find(
    (c) => (c.id || cctvList.value.indexOf(c)) === id
  );
  if (!cctv) return;

  loading.value = true;
  const result = await updateCCTVStatus(id, !cctv.aktif);

  if (result.error) {
    console.error("Gagal update status CCTV:", result.error);
    alert("Gagal update status CCTV");
  }

  await loadCCTVList();
  loading.value = false;
}
</script>

<style scoped>
.kelola-cctv {
  background-color: #f9fafb;
  min-height: 100vh;
}
</style>
