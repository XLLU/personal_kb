<template>
  <div class="app">
    <div class="header">
      <h1>个人知识库系统</h1>
    </div>
    <div class="main-content">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-else>
        <Chat />
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
.app {
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.error-message {
  color: red;
  text-align: center;
  padding: 20px;
  background-color: #ffebee;
  border-radius: 4px;
}
</style> 