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
        <h2>欢迎使用知识库系统</h2>
        <!-- 这里后续会添加上传和聊天组件 -->
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from './services/api';

export default {
  name: 'App',
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