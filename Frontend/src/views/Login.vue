<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-400 to-blue-600 p-4"
  >
    <div
      class="bg-white rounded-3xl shadow-2xl w-full max-w-md md:max-w-lg p-8 md:p-10 transition-all"
    >
      <div class="flex flex-col items-center text-center mb-6 -mt-2">
        <img
          :src="logo"
          alt="FloorEye Logo"
          class="w-28 h-28 sm:w-32 sm:h-32 object-contain mb-3 animate-fade-in"
        />
      </div>

      <div class="text-center mb-16 -mt-4">
        <h1 class="text-2xl sm:text-3xl font-extrabold text-gray-800 mb-1">
          LOGIN
        </h1>
        <p class="text-gray-600 text-sm sm:text-base">
          Masuk ke akun Anda untuk melanjutkan
        </p>
      </div>

      <form class="space-y-5 mt-2" @submit.prevent="handleLogin">
        <div>
          <label class="block text-gray-700 font-medium mb-2">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Masukkan username"
            :disabled="loading"
            class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-sm sm:text-base disabled:opacity-50"
          />
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">Password</label>
          <div class="relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Masukkan password"
              :disabled="loading"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition pr-12 text-sm sm:text-base disabled:opacity-50"
            />

            <button
              type="button"
              @click="togglePassword"
              :disabled="loading"
              class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-700 transition disabled:opacity-50"
            >
              <component :is="showPassword ? EyeOff : Eye" class="w-5 h-5" />
            </button>
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"
        >
          {{ errorMessage }}
        </div>

        <div class="text-right">
          <button
            type="button"
            @click="goToForgot"
            :disabled="loading"
            class="text-blue-600 text-sm sm:text-base hover:underline font-medium disabled:opacity-50"
          >
            Lupa password?
          </button>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition shadow-lg hover:shadow-xl text-sm sm:text-base disabled:opacity-50"
        >
          {{ loading ? "Memproses..." : "Masuk" }}
        </button>
      </form>

      <p class="text-center text-gray-600 text-sm sm:text-base mt-8">
        Belum punya akun?
        <button
          @click="goToRegister"
          :disabled="loading"
          class="text-blue-600 font-semibold hover:underline disabled:opacity-50"
        >
          Daftar
        </button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Eye, EyeOff } from "lucide-vue-next";
import { login } from "@/api/floorEye";
import logo from "@/assets/FloorEye.png";

const router = useRouter();
const showPassword = ref(false);
const username = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

function togglePassword() {
  showPassword.value = !showPassword.value;
}

async function handleLogin() {
  if (!username.value || !password.value) {
    errorMessage.value = "Username dan password harus diisi!";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  const result = await login(username.value, password.value);

  if (result.error) {
    errorMessage.value =
      result.error || "Login gagal! Periksa username dan password.";
    loading.value = false;
    return;
  }

  if (result.token) {
    router.push("/dashboard");
  } else {
    errorMessage.value = "Login gagal! Respons tidak valid dari server.";
    loading.value = false;
  }
}

function goToForgot() {
  router.push("/forgot-password");
}

function goToRegister() {
  router.push("/register");
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
