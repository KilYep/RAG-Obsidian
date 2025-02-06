<template>
  <div class="container mt-4">
    <h1>笔记 AI 助手</h1>
    
    <!-- 对话历史 -->
    <div class="chat-box">
      <div v-for="(msg, index) in messages" :key="index" class="message">
        <div :class="msg.role === 'user' ? 'user-msg' : 'ai-msg'">
          {{ msg.content }}
        </div>
      </div>
    </div>
    
    <!-- 输入框 -->
    <div class="input-box">
      <input 
        v-model="userInput" 
        @keyup.enter="sendMessage"
        placeholder="输入问题..."
      >
      <button @click="sendMessage" :disabled="isLoading">
        {{ isLoading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)

// async function sendMessage() {
//   if (!userInput.value.trim() || isLoading.value) return
  
//   // 添加用户消息
//   messages.value.push({ role: 'user', content: userInput.value })
  
//   isLoading.value = true
//   const currentInput = userInput.value
//   userInput.value = ''

// try {
//     const response = await fetch('http://localhost:8000/stream', {  // 确保这是你的流式API端点
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ input: currentInput })
//     })

//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`)
//     }

//     // 创建一个新的AI消息
//     const aiMessageIndex = messages.value.push({ 
//       role: 'assistant', 
//       content: '' 
//     }) - 1

//     // 获取响应的读取器
//     const reader = response.body.getReader()
//     const decoder = new TextDecoder()

//     while (true) {
//       const { done, value } = await reader.read()
//       if (done) break

//       // 解码并添加新的文本到现有消息
//       const text = decoder.decode(value)
//       messages.value[aiMessageIndex].content += text
//     }

//   } catch (error) {
//     console.error('发送消息失败:', error)
//     messages.value.push({ 
//       role: 'assistant', 
//       content: '抱歉，发生错误，请稍后重试。' 
//     })
//   } finally {
//     isLoading.value = false
//   }
// }

// async function sendMessage() {
//   if (!userInput.value.trim() || isLoading.value) return
  
//   // 添加用户消息
//   messages.value.push({ role: 'user', content: userInput.value })
  
//   isLoading.value = true
//   const currentInput = userInput.value
//   userInput.value = ''

//   try {
//     const response = await fetch('http://localhost:8000/stream', {  // 确保这是你的流式API端点
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ input: currentInput })
//     })

//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`)
//     }

//     // 创建一个新的AI消息
//     const aiMessageIndex = messages.value.push({ 
//       role: 'assistant', 
//       content: '' 
//     }) - 1

//     // 获取响应的读取器
//     const reader = response.body.getReader()
//     const decoder = new TextDecoder()

//     while (true) {
//       const { done, value } = await reader.read()
//       if (done) break

//       // 解码并添加新的文本到现有消息
//       const text = decoder.decode(value)
//       console.log('Received text:', text)  // 添加调试日志
      
//       // 尝试解析数据行
//       const lines = text.split('\n')
//       for (const line of lines) {
//         if (line.startsWith('data: ')) {
//           const data = line.slice(6).trim()
//           if (data && data !== '""') {
//             messages.value[aiMessageIndex].content += data.replace(/^"|"$/g, '')
//           }
//         }
//       }
//     }

//   } catch (error) {
//     console.error('发送消息失败:', error)
//     messages.value.push({ 
//       role: 'assistant', 
//       content: '抱歉，发生错误，请稍后重试。' 
//     })
//   } finally {
//     isLoading.value = false
//   }
// }

async function sendMessage() {
  if (!userInput.value.trim() || isLoading.value) return
  
  // 添加用户消息
  messages.value.push({ role: 'user', content: userInput.value })
  
  isLoading.value = true
  const currentInput = userInput.value
  userInput.value = ''

  try {
    const response = await fetch('http://localhost:8000/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: currentInput })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    // 创建一个新的AI消息
    const aiMessageIndex = messages.value.push({ 
      role: 'assistant', 
      content: '' 
    }) - 1

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      const lines = text.split('\n')
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6).trim()
          if (!data) continue
          
          try {
            const jsonData = JSON.parse(data)
            // 如果不是包含 run_id 的元数据，则添加到内容中
            if (!jsonData.run_id) {
              messages.value[aiMessageIndex].content += jsonData
            }
          } catch {
            // 如果不是 JSON 格式，直接添加文本
            if (data !== '""') {
              messages.value[aiMessageIndex].content += data.replace(/^"|"$/g, '')
            }
          }
        }
      }
    }

  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value.push({ 
      role: 'assistant', 
      content: '抱歉，发生错误，请稍后重试。' 
    })
  } finally {
    isLoading.value = false
  }
}

</script>

<style scoped>
.chat-box {
  height: 400px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 10px;
  margin: 20px 0;
}

.message {
  margin: 10px 0;
}

.user-msg {
  background: #e3f2fd;
  padding: 10px;
  border-radius: 10px;
  margin-left: 20%;
}

.ai-msg {
  background: #f5f5f5;
  padding: 10px;
  border-radius: 10px;
  margin-right: 20%;
}

.input-box {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 8px;
}

button {
  padding: 8px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
}
</style>