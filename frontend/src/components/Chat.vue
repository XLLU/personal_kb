<template>
  <div class="chat-container">
    <div class="messages" ref="messagesContainer">
      <div class="welcome-message" v-if="messages.length === 0">
        <h2>欢迎使用 AI 知识库助手</h2>
        <p>您可以开始提问了...</p>
      </div>
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="['message-wrapper', message.role]">
        <div class="message">
          <div class="avatar">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="content">{{ message.content }}</div>
        </div>
      </div>
    </div>
    <div class="input-container">
      <div class="input-wrapper">
        <textarea
          v-model="userInput"
          @keyup.enter.exact="sendMessage"
          @keydown.enter.exact.prevent
          placeholder="输入消息，按 Enter 发送..."
          :disabled="loading"
          rows="1"
          ref="inputArea"
        ></textarea>
        <button 
          class="send-button"
          @click="sendMessage" 
          :disabled="loading || !userInput.trim()"
        >
          <span v-if="loading" class="loading"></span>
          <span v-else class="send-icon">↑</span>
        </button>
      </div>
      <div class="input-info">
        按 Enter 发送，Shift + Enter 换行
      </div>
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
      
      const message = this.userInput.trim();
      if (!message || this.loading) return;

      this.messages.push({
        role: 'user',
        content: message
      });
      
      this.userInput = '';
      this.loading = true;
      this.adjustTextareaHeight();

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
    },
    adjustTextareaHeight() {
      const textarea = this.$refs.inputArea;
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
    },
    clearMessages() {
      this.messages = [];
    }
  },
  mounted() {
    this.$refs.inputArea.addEventListener('input', this.adjustTextareaHeight);
  },
  beforeUnmount() {
    this.$refs.inputArea.removeEventListener('input', this.adjustTextareaHeight);
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--chat-bg);
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding-bottom: 150px;
}

.welcome-message {
  text-align: center;
  padding: 4rem 1rem;
  color: var(--text-secondary);
}

.welcome-message h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.message-wrapper {
  border-bottom: 1px solid var(--border-color);
}

.message-wrapper.assistant {
  background-color: var(--assistant-msg-bg);
}

.message {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
}

.avatar {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  background-color: var(--hover-color);
  flex-shrink: 0;
}

.content {
  line-height: 1.6;
  white-space: pre-wrap;
  padding: 0.25rem 0;
}

.input-container {
  position: fixed;
  bottom: 0;
  left: var(--sidebar-width);
  right: 0;
  padding: 1.5rem;
  background: linear-gradient(180deg, 
    rgba(52,53,65,0) 0%, 
    rgba(52,53,65,0.9) 20%, 
    rgba(52,53,65,1) 100%
  );
}

.input-wrapper {
  max-width: 800px;
  margin: 0 auto;
  background-color: var(--primary-color);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  padding: 0.75rem;
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
}

textarea {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 1rem;
  line-height: 1.5;
  max-height: 200px;
  resize: none;
  padding: 0;
}

textarea:focus {
  outline: none;
}

.send-button {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.send-button:hover:not(:disabled) {
  background-color: var(--hover-color);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-icon {
  font-size: 1.2rem;
  transform: rotate(-90deg);
}

.loading {
  width: 16px;
  height: 16px;
  border: 2px solid var(--text-secondary);
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

.input-info {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.75rem;
  margin-top: 0.5rem;
  opacity: 0.8;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 滚动条样式 */
.messages::-webkit-scrollbar {
  width: 6px;
}

.messages::-webkit-scrollbar-track {
  background: transparent;
}

.messages::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
}
</style> 