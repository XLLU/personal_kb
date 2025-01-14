<template>
  <div class="app">
    <div class="sidebar">
      <div class="logo">
        <h1>AI 知识库助手</h1>
      </div>
      <div class="sidebar-content">
        <button class="new-chat" @click="clearChat">
          <span class="icon">＋</span>
          新对话
        </button>
      </div>
    </div>
    <div class="main">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-else class="chat-wrapper">
        <Chat ref="chatComponent" />
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from './services/api';
import Chat from './components/Chat.vue';

export default {
  name: 'App',
  components: {
    Chat
  },
  data() {
    return {
      error: null
    }
  },
  methods: {
    clearChat() {
      if (this.$refs.chatComponent) {
        this.$refs.chatComponent.clearMessages();
      }
    }
  },
  async created() {
    try {
      await apiService.testConnection();
    } catch (err) {
      this.error = '系统连接失败，请检查配置';
    }
  }
}
</script>

<style>
:root {
  --sidebar-width: 260px;
  --primary-color: #202123;
  --secondary-color: #343541;
  --text-primary: #ECECF1;
  --text-secondary: #D9D9E3;
  --border-color: #4E4F60;
  --hover-color: #2A2B32;
  --chat-bg: #343541;
  --user-msg-bg: #343541;
  --assistant-msg-bg: #444654;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--secondary-color);
  color: var(--text-primary);
}

.app {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: var(--sidebar-width);
  background-color: var(--primary-color);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-color);
}

.logo {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.logo h1 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--text-primary);
}

.sidebar-content {
  padding: 1rem;
}

.new-chat {
  width: 100%;
  padding: 0.75rem;
  background-color: transparent;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.2s;
}

.new-chat:hover {
  background-color: var(--hover-color);
}

.icon {
  font-size: 1.2rem;
}

.main {
  flex: 1;
  overflow: hidden;
  position: relative;
  background-color: var(--secondary-color);
}

.chat-wrapper {
  height: 100%;
}

.error-message {
  color: #ff4a4a;
  text-align: center;
  padding: 1rem;
  background-color: rgba(255, 74, 74, 0.1);
  margin: 1rem;
  border-radius: 0.5rem;
}
</style> 