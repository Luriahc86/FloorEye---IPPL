<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 to-blue-600 p-4"
  >
    <div
      class="bg-white rounded-3xl shadow-2xl w-full max-w-md md:max-w-lg p-8 md:p-10 transition-all"
    >
      <!-- Logo -->
      <div class="flex flex-col items-center text-center mb-6 -mt-2">
        <img
          :src="logo"
          alt="FloorEye Logo"
          class="w-28 h-28 sm:w-32 sm:h-32 object-contain mb-3 animate-fade-in"
        />
      </div>

      <!-- Judul -->
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">DAFTAR</h2>
        <p class="text-gray-600 text-sm sm:text-base">
          Buat akun baru untuk memulai
        </p>
      </div>

      <!-- Form -->
      <form class="space-y-5" @submit.prevent="handleRegister">
        <!-- Nama Lengkap -->
        <div>
          <label class="block text-gray-700 font-medium mb-2"
            >Nama Lengkap</label
          >
          <input
            v-model="nama"
            type="text"
            placeholder="Masukkan nama lengkap"
            :disabled="loading"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition disabled:opacity-50"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-gray-700 font-medium mb-2">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Masukkan email"
            :disabled="loading"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition disabled:opacity-50"
          />
        </div>

        <!-- Username -->
        <div>
          <label class="block text-gray-700 font-medium mb-2">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Masukkan username"
            :disabled="loading"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition disabled:opacity-50"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-gray-700 font-medium mb-2">Password</label>
          <div class="relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Masukkan password"
              :disabled="loading"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition pr-12 disabled:opacity-50"
            />
            <button
              type="button"
              @click="togglePassword"
              :disabled="loading"
              class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition disabled:opacity-50"
            >
              <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Konfirmasi Password -->
        <div>
          <label class="block text-gray-700 font-medium mb-2"
            >Konfirmasi Password</label
          >
          <div class="relative">
            <input
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="Masukkan ulang password"
              :disabled="loading"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition pr-12 disabled:opacity-50"
            />
            <button
              type="button"
              @click="toggleConfirmPassword"
              :disabled="loading"
              class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition disabled:opacity-50"
            >
              <component
                :is="showConfirmPassword ? EyeOff : Eye"
                class="w-5 h-5"
              />
            </button>
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"
        >
          {{ errorMessage }}
        </div>

        <div
          v-if="successMessage"
          class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm"
        >
          {{ successMessage }}
        </div>

        <!-- Tombol Daftar -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition shadow-lg hover:shadow-xl disabled:opacity-50"
        >
          {{ loading ? "Mendaftarkan..." : "Daftar" }}
        </button>
      </form>

      <!-- Tombol Login -->
      <p class="text-center text-gray-600 text-sm sm:text-base mt-6">
        Sudah punya akun?
        <button
          @click="goToLogin"
          :disabled="loading"
          class="text-blue-600 font-semibold hover:underline disabled:opacity-50"
        >
          Masuk
        </button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Eye, EyeOff } from "lucide-vue-next";
import logo from "@/assets/FloorEye.png";

const router = useRouter();

// Data form
const nama = ref("");
const email = ref("");
const username = ref("");
const password = ref("");
const confirmPassword = ref("");

// State show/hide password
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

function togglePassword() {
  showPassword.value = !showPassword.value;
}

function toggleConfirmPassword() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

// Simulasi proses register
function handleRegister() {
  errorMessage.value = "";
  successMessage.value = "";

  if (
    !nama.value ||
    !email.value ||
    !username.value ||
    !password.value ||
    !confirmPassword.value
  ) {
    errorMessage.value = "Harap isi semua kolom!";
    return;
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errorMessage.value = "Format email tidak valid!";
    return;
  }

  if (username.value.length < 3) {
    errorMessage.value = "Username minimal 3 karakter!";
    return;
  }

  if (password.value.length < 6) {
    errorMessage.value = "Password minimal 6 karakter!";
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Konfirmasi password tidak cocok!";
    return;
  }

  loading.value = true;

  // Simulate API call
  setTimeout(() => {
    successMessage.value = `Pendaftaran berhasil! Selamat datang, ${nama.value}! Anda akan dialihkan ke halaman login.`;

    setTimeout(() => {
      router.push("/");
    }, 2000);
  }, 1000);
}

function goToLogin() {
  router.push("/");
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out both;
}
</style>
