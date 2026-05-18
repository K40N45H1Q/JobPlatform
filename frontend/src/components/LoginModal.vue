<template>
  <teleport to="body">
    <div v-if="modelValue" class="modal-overlay" role="presentation">
      <div class="modal" role="dialog" aria-modal="true" ref="dialog">

        <!-- 🔔 NOTIFY PROVIDER -->
        <NotifyProvider />

        <div class="modal-header">
          <button :class="{ active: activeTab === 'login' }" class="tab-button" @click="setTab('login')">
            {{ $t('login') }}
          </button>

          <button :class="{ active: activeTab === 'register' }" class="tab-button" @click="setTab('register')">
            {{ $t('register') }}
          </button>

          <button class="modal-close-button" @click="close" aria-label="Close">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M6 6l12 12M18 6L6 18" stroke="#111" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>
        </div>

        <div class="modal-body">

          <!-- LOGIN -->
          <div v-if="activeTab === 'login'" class="login-section">
            <form @submit.prevent="submit">

              <div class="form-field">
                <input
                  ref="firstInput"
                  v-model="email"
                  type="text"
                  :placeholder="$t('email')"
                  autocomplete="email"
                />
              </div>

              <div class="form-field">
                <input
                  v-model="password"
                  type="password"
                  :placeholder="$t('password')"
                  autocomplete="current-password"
                />
              </div>

              <button type="submit" class="primary-button">
                {{ $t('login') }}
              </button>

              <a href="https://t.me/gh057wr" class="forgot-password-link">
                {{ $t('forgot_password') }}
              </a>

            </form>
          </div>

          <!-- REGISTER -->
          <div v-else class="register-section">

            <div v-if="!selectedRole" class="role-selection">
              <h3 class="register-heading">
                {{ $t('register_as') }}
              </h3>

              <button class="role-button" @click="handleRoleSelect('jobseeker')">
                {{ $t('for_job_seeker') }}
              </button>

              <button class="role-button" @click="handleRoleSelect('employer')">
                {{ $t('for_employer') }}
              </button>
            </div>

            <div v-else>

              <h3 class="register-heading">
                {{ $t('registration') }}
                {{ selectedRole === 'jobseeker' ? $t('jobseeker') : $t('employer') }}
              </h3>

              <form @submit.prevent="registerSubmit">

                <div class="form-field">
                  <input
                    ref="regFirstInput"
                    v-model="regEmail"
                    type="email"
                    :placeholder="$t('email')"
                    required
                    autocomplete="email"
                  />
                </div>

                <div class="form-field">
                  <input
                    v-model="regPassword"
                    type="password"
                    :placeholder="$t('password')"
                    required
                    autocomplete="new-password"
                  />
                </div>

                <div class="form-field">
                  <input
                    v-model="regConfirmPassword"
                    type="password"
                    :placeholder="$t('confirm_password')"
                    required
                    autocomplete="new-password"
                  />
                </div>

                <button type="submit" class="primary-button">
                  {{ $t('register') }}
                </button>

              </form>

            </div>
          </div>

        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, watch, onBeforeUnmount, nextTick } from 'vue'
import NotifyProvider from './NotifyProvider.vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue'])

const API_BASE = 'http://localhost:8000/api'

const activeTab = ref('login')
const selectedRole = ref(null)

const email = ref('')
const password = ref('')

const regEmail = ref('')
const regPassword = ref('')
const regConfirmPassword = ref('')

const firstInput = ref(null)
const regFirstInput = ref(null)

const close = () => emit('update:modelValue', false)

function setTab(tab) {
  activeTab.value = tab
  if (tab === 'register') selectedRole.value = null
  else nextTick(() => firstInput.value?.focus())
}

function handleRoleSelect(role) {
  selectedRole.value = role
  nextTick(() => regFirstInput.value?.focus())
}

function notify(msg, type = 'info') {
  window.notify?.(msg, type)
}

/* LOGIN */
async function submit() {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: email.value,
        password: password.value
      })
    })

    const data = await res.json().catch(() => ({}))

    if (res.ok && data.status === 'ok') {
      localStorage.setItem('token', data.token)
      notify('Login successful', 'success')
      email.value = password.value = ''
      close()
      return
    }

    throw new Error(data.detail || 'Login error')
  } catch (e) {
    notify(e.message, 'error')
  }
}

/* REGISTER */
async function registerSubmit() {
  if (regPassword.value !== regConfirmPassword.value)
    return notify('Passwords do not match', 'warning')

  try {
    const res = await fetch(`${API_BASE}/create_account`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: regEmail.value,
        password: regPassword.value,
        account_type: selectedRole.value
      })
    })

    const data = await res.json().catch(() => ({}))

    if (res.ok && data.status === 'ok') {
      notify('Registration successful', 'success')

      regEmail.value = ''
      regPassword.value = ''
      regConfirmPassword.value = ''

      selectedRole.value = null
      setTab('login')

      return
    }

    throw new Error(data.detail || 'Registration error')
  } catch (e) {
    notify(e.message, 'error')
  }
}

/* WATCH */
watch(() => props.modelValue, (val) => {
  if (val) {
    activeTab.value = 'login'
    selectedRole.value = null
    setTimeout(() => firstInput.value?.focus(), 10)
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.36);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(8px);
}

.modal {
  width: 420px;
  max-width: calc(100% - 32px);
  background: #fff;
  position: relative;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  border: 2px solid #2563eb;
}

.modal-header {
  display: flex;
  align-items: stretch;
  border-bottom: 1px solid #e5e7eb;
}

.tab-button {
  flex: 1;
  padding: 18px 0;
  font-size: 17px;
  font-weight: 500;
  color: #2563eb;
  background: none;
  border: none;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.tab-button.active {
  font-weight: 600;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #2563eb;
}

.modal-close-button {
  width: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
}

.modal-body {
  padding: 28px;
}

.form-field {
  margin-bottom: 16px;
}

.form-field input {
  width: 100%;
  padding: 14px 16px;
  font-size: 15px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
}

.form-field input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37,99,235,0.15);
}

.primary-button {
  width: 100%;
  padding: 15px;
  background-color: #00c853;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin: 8px 0 16px;
}

.forgot-password-link {
  display: block;
  text-align: center;
  color: #2563eb;
  font-size: 14px;
}

.register-heading {
  text-align: center;
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 12px;
}

.role-selection {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.role-button {
  width: 100%;
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #2563eb;
}
</style>