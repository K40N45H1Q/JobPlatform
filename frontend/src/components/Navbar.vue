<template>
  <header>
    <div class="container">
      <a href="/" class="logo">AQUA</a>

      <nav>
        <a href="/">{{ t('menu.employers') }}</a>
        <button class="nav-link" @click.prevent="openLogin">{{ t('menu.entrance') }}</button>
        <LanguageSwitcher />
      </nav>

      <button
        class="hamburger"
        :class="{ open: mobileMenuOpen }"
        aria-controls="mobile-drawer"
        :aria-expanded="mobileMenuOpen"
        @click="toggleMobileMenu"
        type="button"
      >
        <span class="line" aria-hidden="true"></span>
      </button>
    </div>

    <div class="mobile-overlay" :class="{ open: mobileMenuOpen }" @click="closeMobileMenu"></div>

    <aside id="mobile-drawer" class="mobile-drawer" :class="{ open: mobileMenuOpen }" role="dialog" aria-modal="true">
      <div class="drawer-header">
        <div class="drawer-title">{{ t('menu.title') }}</div>
        <button class="drawer-close" @click="closeMobileMenu" aria-label="Close menu" type="button">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <nav class="drawer-nav">
        <!-- мобильная кнопка открытия модалки: стиль НЕ менял (как у остальных ссылок в drawer) -->
        <button class="drawer-link" @click.prevent="openLogin">{{ t('menu.entrance') }}</button>
        <a href="/employers" @click="closeMobileMenu">{{ t('menu.employers') }}</a>
      </nav>

      <div class="lang-section" role="region" aria-label="Language selection">
        <div class="lang-label">{{ t('languages.label') }}</div>
        <div class="lang-list" role="list">
          <button
            v-for="languageItem in languagesList"
            :key="languageItem.code"
            :class="['lang-item', { active: languageItem.code === locale.value }]"
            @click="selectLanguage(languageItem)"
            type="button"
            role="listitem"
          >
            <img :src="languageItem.flag" :alt="languageItem.code" />
            <span>{{ t('languages.' + languageItem.code) }}</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Модалка входа -->
    <LoginModal v-model="showLogin" />
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from './LanguageSwitcher.vue'
import LoginModal from './LoginModal.vue' // путь: файл должен быть рядом с этим компонентом

const i18n = useI18n()
const locale = i18n.locale
const t = i18n.t

const mobileMenuOpen = ref(false)
const showLogin = ref(false)

const languagesList = [
  { code: 'ru', flag: '/flags/ru.svg' },
  { code: 'en', flag: '/flags/gb.svg' }
]

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

function openLogin() {
  // закрываем мобильное меню если открыт
  mobileMenuOpen.value = false
  showLogin.value = true
}

function selectLanguage(languageItem) {
  locale.value = languageItem.code
  localStorage.setItem('lang', languageItem.code)
  closeMobileMenu()
}

// function onLoginSubmit(payload) {
//   // payload = { email, password }
//   console.log('Login submit', payload)
// }

onMounted(() => {
  const savedLanguage = localStorage.getItem('lang')
  if (savedLanguage) {
    locale.value = savedLanguage
  }
})
</script>

<style scoped>
header {
  width: 100%;
  height: 80px;
  background: rgba(21, 56, 212, 0.9);
  display: flex;
  align-items: center;
}
.container {
  width: 900px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
nav {
  display: flex;
  gap: 24px;
  align-items: center;
  font-size: 16px;
  color: #fff;
}
nav a {
  color: #fff;
  text-decoration: none;
}
.logo {
  color: #fff;
  text-decoration: none;
  font-weight: 800;
  font-size: 30px;
}
.hamburger {
  display: none;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  align-items: center;
  justify-content: center;
}
.hamburger .line {
  width: 22px;
  height: 2px;
  background: #fff;
  border-radius: 2px;
  position: relative;
  transition: transform .25s ease, opacity .25s ease;
}
.hamburger .line::before,
.hamburger .line::after {
  content: "";
  position: absolute;
  left: 0;
  width: 22px;
  height: 2px;
  background: #fff;
  border-radius: 2px;
  transition: transform .25s ease, top .25s ease, bottom .25s ease, opacity .25s ease;
}
.hamburger .line::before { top: -7px; }
.hamburger .line::after { bottom: -7px; }
.hamburger.open .line { transform: rotate(45deg); background: transparent; }
.hamburger.open .line::before { transform: rotate(-90deg); top: 0; }
.hamburger.open .line::after { transform: rotate(-90deg); bottom: 0; }

.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.32);
  opacity: 0;
  pointer-events: none;
  transition: opacity .28s ease;
  z-index: 9998;
}
.mobile-overlay.open {
  opacity: 1;
  pointer-events: auto;
}

.mobile-drawer {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 320px;
  max-width: 92vw;
  background: #fff;
  transform: translateX(100%);
  transition: transform .28s cubic-bezier(.2,.9,.2,1);
  box-shadow: -8px 0 30px rgba(0,0,0,0.18);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  padding: 16px;
  overflow-y: auto;
}
.mobile-drawer.open {
  transform: translateX(0);
}
.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.drawer-title {
  font-weight: 600;
  color: #111;
  font-size: 18px;
}
.drawer-close {
  background: none;
  border: none;
  padding: 6px;
  cursor: pointer;
}
.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}
.drawer-nav a {
  color: #111;
  text-decoration: none;
  padding: 12px 10px;
  border-radius: 8px;
}

/* nav-link — десктоп: белый текст (как и везде) */
.nav-link {
  background: none;
  border: none;
  color: #fff;
  font: inherit;
  cursor: pointer;
  padding: 0;
  text-decoration: none;
}

/* drawer-link — мобильное меню: вернуть поведение как у обычных ссылок drawer (тёмный текст на белом фоне) */
.drawer-link {
  background: transparent;
  border: none;
  color: #111;
  font: inherit;
  cursor: pointer;
  padding: 12px 10px;
  border-radius: 8px;
  text-align: left;
  display: block;
}

/* hover/focus состояния для drawer items */
.drawer-link:hover,
.drawer-link:focus,
.drawer-nav a:hover,
.drawer-nav a:focus {
  background-color: rgba(0,0,0,0.06);
  outline: none;
}

/* Стили для языковой секции */
.lang-section {
  margin-top: 16px;
}
.lang-label {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}
.lang-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.lang-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  background: transparent;
  border: 1px solid rgba(0,0,0,0.04);
}
.lang-item.active {
  background: rgba(0,0,0,0.06);
  border-color: rgba(0,0,0,0.08);
}
.lang-item img {
  width: 28px;
  height: 20px;
  object-fit: cover;
  border-radius: 3px;
}
.lang-item span {
  color: #111;
  font-size: 15px;
}

.lang-item:hover, .drawer-nav a:hover {
  width: 100%;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.1);
}

.drawer-link {
  width: 100% !important;
  text-align: center !important;
}

@media (max-width: 950px) {
  .container { width: calc(100% - 32px); padding: 0 16px; }
  nav { display: none; }
  .hamburger { display: inline-flex; }
}
@media (min-width: 951px) {
  .mobile-drawer { display: none; }
  .mobile-overlay { display: none; }
}
</style>
