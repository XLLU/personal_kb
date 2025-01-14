<template>
  <div class="login-container">
    <h2>知识库登录</h2>
    <div class="login-form">
      <input 
        v-model="apiKey"
        type="password"
        placeholder="请输入您的 API Key"
        @keyup.enter="handleLogin"
        :disabled="loading"
      >
      <button 
        @click="handleLogin"
        :disabled="loading"
      >
        {{ loading ? '验证中...' : '登录' }}
      </button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      apiKey: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      if (!this.apiKey) {
        this.error = '请输入 API Key';
        return;
      }
      
      this.loading = true;
      this.error = '';
      
      try {
        const response = await fetch('/api/auth/verify', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ apiKey: this.apiKey })
        });
        
        const data = await response.json();
        
        if (response.ok) {
          localStorage.setItem('apiKey', this.apiKey);
          this.$emit('login-success');
        } else {
          this.error = data.error || 'API Key 验证失败';
        }
      } catch (err) {
        console.error('Login error:', err);
        this.error = '登录失败，请检查网络连接';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 10px;
}
</style> 