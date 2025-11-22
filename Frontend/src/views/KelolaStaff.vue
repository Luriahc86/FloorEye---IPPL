<template>
  <div class="kelola-staff p-8">
    <h1 class="text-2xl font-bold mb-2">Kelola Staff</h1>
    <p class="text-gray-600 mb-6">
      Tambah dan kelola nomor staff yang akan menerima notifikasi
    </p>

    <div class="flex flex-wrap gap-8">
      <!-- Form Tambah Staff -->
      <div class="w-full md:w-1/2 bg-white p-6 rounded-xl shadow">
        <h2 class="font-semibold text-lg mb-4">Tambah Staff Baru</h2>
        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Nama Staff</label>
          <input
            v-model="nama"
            type="text"
            placeholder="Masukkan nama staff"
            :disabled="loading"
            class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          />
        </div>
        <div class="mb-3">
          <label class="block text-sm font-medium mb-1">Akun Gmail</label>
          <input
            v-model="gmail"
            type="email"
            placeholder="example@gmail.com"
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
          @click="tambahStaff"
          :disabled="loading"
          class="bg-blue-600 text-white w-full py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {{ loading ? "Menambah..." : "+ Tambah Staff" }}
        </button>
      </div>

      <!-- Daftar Staff -->
      <div class="w-full md:w-1/3 bg-white p-6 rounded-xl shadow">
        <h2 class="font-semibold text-lg mb-4">
          Daftar Staff ({{ staffList.length }})
        </h2>

        <div
          v-if="staffList.length === 0"
          class="text-gray-500 italic text-center py-6"
        >
          Belum ada staff terdaftar.
        </div>

        <div
          v-for="(s, index) in staffList"
          :key="s.id || index"
          class="flex justify-between items-center border-b py-3"
        >
          <div>
            <p class="font-medium">{{ s.nama }}</p>
            <p class="text-sm text-gray-500">{{ s.telepon }}</p>
          </div>
          <button
            @click="hapusStaff(s.id || index)"
            :disabled="loading"
            class="text-red-500 hover:text-red-700 disabled:opacity-50"
          >
            🗑
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getStaffList, addStaff, deleteStaff } from "@/api/floorEye";

const nama = ref("");
const telepon = ref("");
const staffList = ref([]);
const loading = ref(false);
const errorMessage = ref("");

onMounted(() => {
  loadStaffList();
});

async function loadStaffList() {
  const data = await getStaffList();
  staffList.value = Array.isArray(data) ? data : [];
}

async function tambahStaff() {
  if (!nama.value || !telepon.value) {
    errorMessage.value = "Lengkapi semua data!";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  const result = await addStaff(nama.value, telepon.value);

  if (result.error) {
    errorMessage.value = result.error || "Gagal menambah staff";
    loading.value = false;
    return;
  }

  await loadStaffList();
  nama.value = "";
  telepon.value = "";
  loading.value = false;
}

async function hapusStaff(id) {
  if (!confirm("Yakin ingin menghapus staff ini?")) return;

  loading.value = true;
  const result = await deleteStaff(id);

  if (result.error) {
    console.error("Gagal menghapus staff:", result.error);
    alert("Gagal menghapus staff");
  }

  await loadStaffList();
  loading.value = false;
}
</script>

<style scoped>
.kelola-staff {
  background-color: #f9fafb;
  min-height: 100vh;
}
</style>
