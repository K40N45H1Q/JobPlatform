<template>
  <div class="repair-wrapper">
    <Navbar />
    <SearchForm />
  </div>
  <Companies />
  <Footer />
  <NotifyProvider />
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import SearchForm from './components/SearchForm.vue'
import Companies from './components/Companies.vue'
import Footer from './components/Footer.vue';
import NotifyProvider from './components/NotifyProvider.vue'
</script>

<style>
@font-face {
  font-family: "JetBrainsMono";
  font-style: normal;
  font-weight: 100 900;
  src: url("/JetBrainsMono.ttf") format("truetype");
  font-display: swap;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "JetBrainsMono", monospace;
}

html, body, #root, .test {
  height: 100%;
}

a {
  text-decoration: none;
}

html, body, #root, .wrapper {
  scrollbar-width: thin;
  scrollbar-color: #1538d4 #000;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent !important;
}

::-webkit-scrollbar-thumb {
  background: #1538d4;
  border-radius: 999px;
  border: 2px solid #000;
}

::-webkit-scrollbar-thumb:hover {
  background: #0f2fb0;
}

.repair-wrapper {
  height: max-content;
  overflow: hidden;
  background-color: #1538d4;
}

@media (max-width: 330px) {
  html, body {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden !important;
    background: #000 !important;
  }

  .repair-wrapper,
  .repair-wrapper * {
    visibility: hidden !important;
  }

  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background: #000;
    z-index: 2147483646;
    pointer-events: none;
  }

  body::after {
    content: ":(";
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 72px;
    line-height: 1;
    z-index: 2147483647;
    pointer-events: none;
    transform: rotate(-270deg);
    transform-origin: center;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}
</style>
