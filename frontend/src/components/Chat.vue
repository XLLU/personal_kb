<template>
  <div class="chat-container">
    <div class="messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.role]">
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
    <div class="input-area">
      <textarea
        v-model="userInput"
        @keyup.enter.exact="sendMessage"
        placeholder="输入消息，按Enter发送..."
        :disabled="loading"
      ></textarea>
      <button @click="sendMessage" :disabled="loading || !userInput.trim()">
        {{ loading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api';

export default {
  name: 'Chat',
  data() {
    return {
      messages: [],
      userInput: '',
      loading: false
    }
  },
  methods: {
    async sendMessage(e) {
      if (e.type === 'keyup' && e.shiftKey) return;
      if (e.type === 'keyup') e.preventDefault();
      
      const message = this.userInput.trim();
      if (!message || this.loading) return;

      this.messages.push({
        role: 'user',
        content: message
      });
      
      this.userInput = '';
      this.loading = true;

      try {
        const response = await apiService.sendChatMessage(message);
        this.messages.push({
          role: 'assistant',
          content: response.message
        });
      } catch (error) {
        this.messages.push({
          role: 'error',
          content: '消息发送失败，请重试'
        });
      } finally {
        this.loading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      container.scrollTop = container.scrollHeight;
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 12px;
  border-radius: 8px;
  margin: 4px 0;
}

.message.user {
  align-self: flex-end;
  background-color: #007AFF;
  color: white;
}

.message.assistant {
  align-self: flex-start;
  background-color: #f0f0f0;
  color: #333;
}

.message.error {
  align-self: center;
  background-color: #ffebee;
  color: #c62828;
}

.input-area {
  border-top: 1px solid #ddd;
  padding: 20px;
  display: flex;
  gap: 10px;
}

textarea {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  height: 40px;
  line-height: 20px;
}

button {
  padding: 10px 20px;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style> 