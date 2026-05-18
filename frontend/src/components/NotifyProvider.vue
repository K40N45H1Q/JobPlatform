<template>
  <div class="notify-wrap">
    <Transition name="notify">
      <div v-if="message" class="notify" :class="notificationType">
        {{ message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref(null)
const notificationType = ref('info')

let timeoutId = null
let isShowing = false

function showNotification(notificationMessage, type = 'info') {
  if (timeoutId) clearTimeout(timeoutId)

  message.value = null
  isShowing = false

  setTimeout(() => {
    message.value = notificationMessage
    notificationType.value = type
    isShowing = true

    timeoutId = setTimeout(() => {
      message.value = null
      isShowing = false
    }, 3000)
  }, 0)
}

window.notify = showNotification
</script>

<style scoped>
.notify-wrap {
  position: absolute;
  top: -70px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  pointer-events: none;
  z-index: 9999;
}

.notify {
  width: 100%;
  max-width: 100%;
  text-align: center;
  padding: 12px 14px;
  border-radius: 10px;
  color: #ffffff;
  box-sizing: border-box;
  font-weight: 500;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.info {
  background-color: #2563eb !important;
}

.success {
  background-color: #16a34a !important;
}

.error {
  background-color: #dc2626 !important;
}

.warning {
  background-color: #d97706 !important;
}

.notify-enter-active,
.notify-leave-active {
  transition: all 0.2s ease;
}

.notify-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.notify-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>