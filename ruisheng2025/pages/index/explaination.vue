<template>
  <view class="container">
    <SidebarNav :active-index="1" @navigate="handleNavigate"/>
    <view class="content-wrapper">
      <!-- 新增两列布局容器 -->
      <view class="two-column-layout">
        <!-- 左侧文本输入区域 -->
        <textarea 
          class="multi-line-input"
          v-model="inputText"
          placeholder="请输入内容,支持中、英、韩、日混合输入" 
          maxlength="2000"
          auto-height
          @input="handleInput"
        ></textarea>

        <!-- 右侧组件列 -->
        <view class="right-column">
          <generate 
            class='TTS_standard'
            :input-text="inputText"
            :ref-audio-path="selectedAudioPath"
            :emotion-params="emotionParams"
            @update-text="inputText = $event"
          ></generate>
          
          <emotion 
            class='card'
            @update-params="handleEmotionParams"
          ></emotion>
          
          <VoiceContent 
            class='Voice_Content'
            @select-audio="handleAudioSelect"
          ></VoiceContent>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
	
import generate from '@/components/card/generate.vue'
import SidebarNav from '@/components/SidebarNav.vue'
import VoiceContent from '@/components/card/VoiceContent.vue'
import emotion from '@/components/card/emotion.vue'
const inputText = ref('')

const selectedAudioPath = ref('')

// 新增情感参数状态
const emotionParams = ref({
  speedFactor: '1',
  temperature: '1'
})

// 处理情感参数更新
const handleEmotionParams = (params) => {
  emotionParams.value = params
}

// 处理音频选择
const handleAudioSelect = (path) => {
  selectedAudioPath.value = path
}

const handleInput = (e) => { 
  inputText.value = e.detail.value
}

const handleNavigate = (path) => {
  uni.navigateTo({ url: path })
}
</script>

<style scoped>
/* 新增容器flex布局 */
.container {
  display: flex;
}

/* 主内容区调整 */
.content-wrapper {
  flex: 1;
  padding: 32rpx;
  background: white;
  border-radius: 24rpx 0 0 24rpx;
  min-height: calc(100vh - 64rpx);
  overflow-y: auto;
  width: 600px;
}

.two-column-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}



/* 右侧组件垂直排列 */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 800px; /* 保持原有组件宽度 */
}

/* 声音样本库 */
.Voice_Content{
  width: 800px;
}

.TTS_standard{
	border: 2px solid #e0e3e9;
	border-radius: 40rpx;
	box-shadow: -4rpx 0 12rpx rgba(0,0,0,0.05);
	height: 320px;
	width: 720px;
}

.multi-line-input {
  flex: 1;
  width: 100%;
  min-height: 1000px;
  padding: 16px;
  border: 2px solid #e0e3e9;
  border-radius: 40rpx;
  font-size: 20px;
  line-height: 1.6;
  color: #2d3748;
  background: white;
  transition: all 0.3s;
  resize: vertical; /* 允许垂直调整大小 */
  white-space: pre-wrap; /* 保留换行符 */
  box-shadow: -4rpx 0 12rpx rgba(0,0,0,0.05);
}

/* 聚焦状态 */
.multi-line-input:focus {
  border-color: #4f46e5;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

/* 字数统计 */
.counter {
  text-align: right;
  margin-top: 8px;
  font-size: 12px;
  color: #64748b;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .multi-line-input {
    min-height: 120px;
  }
}

.card{
	border: 2px solid #e0e3e9;
	border-radius: 40rpx;
	box-shadow: -4rpx 0 12rpx rgba(0,0,0,0.05);
	width: 100%;
	height: 200px;
}

</style>