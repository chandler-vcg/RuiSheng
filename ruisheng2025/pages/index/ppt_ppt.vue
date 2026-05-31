<template>
  <view class="container">
    <SidebarNav :active-index="2" @navigate="handleNavigate"/>
    <view class="content-wrapper">
      <view class="two-column-layout">
        <!-- 左侧区域 -->
        <view class="left-column">
          <!-- 静态课件模式 -->
          <view class="ppt-preview">
            <view class="preview-controls">
              <view class="param-selector">
                <picker 
                  @change="handleLangChange" 
                  :value="selectedLangIndex" 
                  :range="langOptions" 
                  range-key="text"
                  mode="selector"
                >
                  <view class="lang-select-btn">
                    {{ langOptions[selectedLangIndex].text }} ▼
                  </view>
                </picker>
              </view>
            </view>
            <view class="empty-prompt">PPT预览区域</view>
          </view>
          
          <view class="button-group">
            <button class="action-btn" @click="handleUploadVideo">上传ppt</button>
            <button class="action-btn" @click="handlePPTSynthesis">合成ppt</button>
            <button 
              class="action-btn" 
              @click="handleDownloadVideo"
            >下载ppt</button>
          </view>
        </view>

        <!-- 右侧配置区域 -->
        <view class="right-column">
          <!-- 语言选择器 -->
          <view class="language-box">
            <button 
              v-for="lang in languages"
              :key="lang.value"
              class="lang-btn"
              :class="{ 'active-lang': selectedLang === lang.value }"
              @click="selectedLang = lang.value"
            >
              {{ lang.text }}
            </button>
          </view>

          <emotion 
            class="card"
            @update-params="handleEmotionParams"
          />
          <VoiceContent 
            class="voice-content"
            @select-audio="handleAudioSelect"
          />
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import SidebarNav from '@/components/SidebarNav.vue'
import VoiceContent from '@/components/card/VoiceContent.vue'
import emotion from '@/components/card/emotion.vue'

// 语言选择配置
const languages = [
  { text: '中文', value: 'zh' },
  { text: '英文', value: 'en' }
]
const selectedLang = ref('zh')
const pptFile = ref(null)

const selectedLangIndex = ref(0)
const langOptions = ref([
  { text: '原态转化', value: '1' },
  { text: '智能润色', value: '2' },
  { text: '逸韵修裁', value: '3' }
]);

// 选择器变更处理
const handleLangChange = (e) => {
  selectedLangIndex.value = e.detail.value;
  console.log('当前选择模式:', langOptions.value[selectedLangIndex.value].text);
};

// 音频相关状态
const selectedAudio = ref(null)
const emotionParams = ref({
  speed: 1.0,
  temperature: 1.0,
  interval: 0.3
})

// 子组件事件处理
const handleEmotionParams = (params) => {
  emotionParams.value = params
}

const handleAudioSelect = (audioPath) => {
  selectedAudio.value = audioPath
}

// 导航处理
const handleNavigate = (path) => {
  uni.navigateTo({ url: path })
}

// 文件上传逻辑
const handleUploadVideo = async () => {
  try {
    const res = await uni.chooseFile({
      count: 1,
      extension: ['.ppt', '.pptx'],
      type: 'file'
    });
  
    if (res?.tempFiles?.length > 0) {
      pptFile.value = {
        file: res.tempFiles[0],
        path: res.tempFiles[0].path
      };
      console.log('PPT文件路径:', pptFile.value.path);
      uni.showToast({ title: 'PPT上传成功', icon: 'success' });
    }
  } catch (error) {
    console.error('文件选择失败:', error);
    uni.showToast({ title: '文件上传失败', icon: 'none' });
  }
}

// 合成PPT
const handlePPTSynthesis = async () => {
  if (!pptFile.value?.path) {
    uni.showToast({ title: '请先选择PPT文件', icon: 'none' });
    return;
  }

  try {
    const response = await uni.request({
      url: `http://127.0.0.1:8000/process_ppt`,
      method: "POST",
      header: { "Content-Type": "application/json" },
      data: {
        ppt_path: pptFile.value.path,
        speed_factor: emotionParams.value.speed,
        emotion: emotionParams.value.temperature,
        languages: selectedLang.value
      }
    });
    
    if (response.statusCode === 200) {
      uni.showToast({ title: '处理成功', icon: 'success' });
    } else {
      uni.showToast({ title: response.data.error || '处理失败', icon: 'none' });
    }
  } catch (error) {
    console.error('上传失败:', error);
    uni.showToast({ title: '上传失败', icon: 'none' });
  }
};

// 下载处理
const handleDownloadVideo = async () => {
  if (!pptFile.value?.path) {
    uni.showToast({ title: '请先合成PPT', icon: 'none' });
    return;
  }
  
  try {
    const link = document.createElement('a');
    link.href = pptFile.value.path;
    link.download = `synthesized_${Date.now()}.pptx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    uni.showToast({ title: '开始下载', icon: 'success' });
  } catch (error) {
    uni.showToast({ title: `下载失败：${error.message}`, icon: 'none' });
  }
}
</script>

<style scoped>
/* 保持原有样式不变 */
.container {
  display: flex;
}

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
  gap: 24px;
  min-height: calc(100vh - 128rpx);
  width: 100%
}

.left-column {
  flex: 1;
}

.ppt-preview {
  height: 830px;
  border: 2px solid #e8ebf0;
  border-radius: 24px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-group {
  margin-top: 24px;
  display: flex;
  gap: 70px;
  justify-content: center;
}

.action-btn {
  width: 200px;
  height: 75px;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 20px;
  background: #06a7ff;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
}

.action-btn:active {
  opacity: 0.8;
}

.right-column {
  width: 800px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.language-box {
  padding: 12px;
  background: white;
  border: 2px solid #e8ebf0;
  border-radius: 12px;
  display: flex;
  gap: 12px;
}

.lang-btn {
  flex: 1;
  padding: 8px 16px;
  border-radius: 8px;
  background: white;
  color: #7f8c8d;
  transition: all 0.2s;
}

.lang-btn.active-lang {
  background: #3498db;
  color: white;
}

.card {
  border: 2px solid #e8ebf0;
  border-radius: 12px;
  padding: 16px;
  background: white;
  height: 200px;
}

.voice-content {
  width: 800px;
}

.empty-prompt {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 24px;
  background: #f8f9fa;
}

.preview-controls {
  position: absolute;
  top: 20px;
  left: 271px;
  z-index: 2;
  width: 200px;
}

.lang-select-btn {
  padding: 12rpx 24rpx;
  background-color: #e6f7ff;
  border: 2rpx solid #91d5ff;
  border-radius: 12px;
  color: #1890ff;
  font-size: 28px;
  transition: all 0.3s;
  box-shadow: 0 2rpx 6rpx rgba(24, 144, 255, 0.2);
}

.lang-select-btn:active {
  background-color: #bae7ff;
  transform: scale(0.98);
}
</style>