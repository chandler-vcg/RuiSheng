<template>
  <view class="container">
    <SidebarNav :active-index="4" @navigate="handleNavigate"/>
    <view class="content-wrapper">
      <view class="two-column-layout">
        <!-- 左侧视频区域 -->
        <view class="left-column">
          <view class="video-preview" v-if="synthesizedVideo">
                <video 
                  class="preview-player"
                  :src="synthesizedVideo"
                  controls
                ></video>
              </view>
              <view class="video-preview" v-else>
                <view class="empty-prompt">视频预览区域</view>
              </view>
          <!-- 操作按钮组 -->
          <view class="button-group">
            <button class="action-btn" @click="handleUploadVideo">上传视频</button>
            <button class="action-btn" @click="handleSynthesize">合成视频</button>
            <button 
                  class="action-btn" 
                  @click="handleDownloadVideo"
                >下载视频</button>
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
const synthesizedVideo = ref(null)
const videoFile = ref(null);

// 音频相关状态
const selectedAudio = ref(null)
const emotionParams = ref({
  speed: 1,
  temperature: "1"
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

// 选择视频文件
const handleUploadVideo = async () => {
  try {
    const res = await uni.chooseFile({
      count: 1,
      extension: ['.mp4', '.mov', '.avi'], // 添加视频格式
      type: 'file'
    });

    if (res?.tempFiles?.length > 0) {
      videoFile.value = {
        file: res.tempFiles[0],
        path: res.tempFiles[0].path
      };
      uni.showToast({
        title: '视频上传成功',
        icon: 'success',
        duration: 2000
      });
      console.log('选择的视频路径:', videoFile.value.path);
    }
  } catch (error) {
    console.error('选择文件失败:', error);
    uni.showToast({ title: '选择文件失败', icon: 'none' });
  }
}

// 合成处理方法
const handleSynthesize = async () => {
  try {
	if (!videoFile.value?.path) {
	  uni.showToast({
	    title: '请先上传视频文件',
	    icon: 'none',
	    duration: 2000
	  });
	  return; // 阻止继续执行
	}
	
	if (!selectedAudio.value) {
		uni.showToast({ title: '请先选择音频模型', icon: 'none' })
		return
	}
	console.log("发送参数:", {
	  video_path: "video.mp4",//'videoFile.value.path',
	  output_path: 'output_video.mp4',
	  reference_audio: selectedAudio.value, // 使用选中的音频路径
	  speed_factor: parseFloat(emotionParams.value.speed),
	});
	uni.showLoading({ title: "合成中..." });
    // 调用合成接口
    const response = await uni.request({
      url: `http://localhost:8080/process`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data: {
        video_path: "video.mp4",//'videoFile.value.path',
        speed_factor: parseFloat(emotionParams.value.speed),
        output_path: 'output_video.mp4',
        reference_audio: selectedAudio.value, // 使用选中的音频路径,
		top_k:5.0,
		top_p:1.0
      }
    });
	
	uni.hideLoading();
	
    if (response.statusCode === 200) {
      synthesizedVideo.value = `http://127.0.0.1:8000/files/${response.data.output_filename}`
      uni.showToast({ title: '合成成功', icon: 'success' })
    }
  } catch (error) {
    console.error('合成失败:', error)
    uni.showToast({ title: '合成失败', icon: 'none' })
  }
}

// 下载处理方法
const handleDownloadVideo = async () => {
  if (!synthesizedVideo.value) {
      uni.showToast({
        title: '请先合成视频',
        icon: 'none',
        duration: 2000
      })
      return
    }
  
  try {
    const result = await uni.downloadFile({
      url: synthesizedVideo.value,
      filePath: `${uni.env.USER_DATA_PATH}/${Date.now()}.mp4`
    })
    
    if (result.statusCode === 200) {
      uni.saveFileToDisk({
        filePath: result.tempFilePath,
        success: () => uni.showToast({ title: '下载成功', icon: 'success' })
      })
    }
  } catch (error) {
    uni.showToast({ title: '下载失败', icon: 'none' })
  }
}
</script>

<style scoped>
/* 基础布局 */
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

/* 左侧视频区域 */
.left-column {
  flex: 1;
}

.video-preview {
  height: 735px;
  border: 2px solid #e8ebf0;
  border-radius: 24px;
  overflow: hidden;
}

.preview-player {
  width: 100%;
  height: 100%;
  object-fit: contain;
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
  margin: 0; /* 移除默认外边距 */
  padding: 12px 24px;
  border: none !important;
  border-radius: 10px;
  font-size: 20px;
  background: #06a7ff !important;
  color: white !important;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:active {
  opacity: 0.8;
  transform: none; /* 移除原缩放效果 */
}

/* 右侧配置区域 */
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
  border: 1px solid #e8ebf0;
  border-radius: 8px;
  background: white;
  color: #7f8c8d;
  transition: all 0.2s;
}

.lang-btn.active-lang {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

/* 子组件样式 */
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
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 24px;
  background: #f8f9fa;
}

.preview-video {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 保持视频比例 */
}
</style>