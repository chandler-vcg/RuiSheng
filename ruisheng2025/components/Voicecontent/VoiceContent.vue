<template>
  <view class="container">
    <!-- 主内容区 -->
    <view class="content-wrapper">
      <!-- 顶部标题 -->
      <view class="content-header">我的声色集</view>

      <!-- 声音列表 -->
      <view class="voice-list">
        <view
          class="voice-item"
          v-for="(item, index) in recordings"
          :key="index"
        >
          <view class="voice-info">
            <text class="voice-title">{{ item.title }}</text>
            <view class="voice-progress">
              <text class="time">{{ formatTime(item.currentTime) }}/{{ formatTime(item.duration) }}</text>
              <view class="progress-bar">
                <view 
                  class="progress" 
                  :style="{ width: item.progress + '%' }"
                ></view>
              </view>
            </view>
          </view>
          <view class="voice-controls">
            <button class="icon-btn" @click.stop="togglePlay(index)">
              {{ playingIndex === index ? '⏸' : '▶️' }}
            </button>
            <button class="icon-btn" @click.stop="downloadAudio(item)">⬇️</button>
            <button class="icon-btn delete-btn" @click.stop="deleteRecording(index)">🗑️</button>
          </view>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="bottom-buttons">
        <view class="button stop-button" @click="chooseAudio">上传音色</view>
        <view
          class="button start-button active"
          :class="{ recording: isRecording }"
          @click="toggleRecording"
        >
          {{ isRecording ? '⏹ 停止录制' : '🎙 录制声音' }}
        </view>
        <view class="button clear-button" @click="clearMemory">清除内存</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onBeforeUnmount, onMounted } from 'vue';

// 录音列表数据
const recordings = ref([
  { title: '标准男声', duration: null, currentTime: 0, src: "voice/normal/man_1.wav", progress: 0, _audio: null },
  { title: '标准女声', duration: null, currentTime: 0, src: "voice/normal/woman_1.wav", progress: 0, _audio: null },
  { title: '高兴女青年', duration: null, currentTime: 0, src: "voice/happy/高兴女青年.wav", progress: 0, _audio: null },
  { title: '高兴女少年', duration: null, currentTime: 0, src: "voice/happy/高兴女少年.wav", progress: 0, _audio: null },
  { title: '激动女青年', duration: null, currentTime: 0, src: "voice/preferrence/激动女青年.wav", progress: 0, _audio: null },
  { title: '悲伤男青年', duration: null, currentTime: 0, src: "voice/sad/悲伤男青年.wav", progress: 0, _audio: null },
  { title: '悲伤女青年', duration: null, currentTime: 0, src: "voice/sad/悲伤女青年.wav", progress: 0, _audio: null },
  { title: '恐惧男青年', duration: null, currentTime: 0, src: "voice/fear/恐惧男青年.wav", progress: 0, _audio: null },
  { title: '恐惧女青年', duration: null, currentTime: 0, src: "voice/fear/恐惧女青年.wav", progress: 0, _audio: null },
  { title: '疑惑男青年', duration: null, currentTime: 0, src: "voice/doubt/疑惑男青年.wav", progress: 0, _audio: null },
  { title: '疑惑女青年', duration: null, currentTime: 0, src: "voice/doubt/疑惑女青年.wav", progress: 0, _audio: null },
  { title: '厌恶男青年', duration: null, currentTime: 0, src: "voice/disgust/厌恶男青年.wav", progress: 0, _audio: null },
  { title: '厌恶女青年', duration: null, currentTime: 0, src: "voice/disgust/厌恶女青年.wav", progress: 0, _audio: null },
  { title: '惊讶男少年', duration: null, currentTime: 0, src: "voice/astonish/惊讶男少年.wav", progress: 0, _audio: null },
  { title: '惊讶男中年', duration: null, currentTime: 0, src: "voice/astonish/惊讶男中年.wav", progress: 0, _audio: null },
  { title: '惊讶女青年', duration: null, currentTime: 0, src: "voice/astonish/惊讶女青年.wav", progress: 0, _audio: null },
  { title: '愤怒男中年', duration: null, currentTime: 0, src: "voice/angry/愤怒男中年.wav", progress: 0, _audio: null }
]);


//uni.removeStorageSync('recordings')

// 新增：预加载音频时长
const loadDurations = async () => {
  const promises = recordings.value.map(async (item, index) => {
    if (!item.duration) {
      return new Promise((resolve) => {
        const audio = new Audio(item.src);
        audio.addEventListener('loadedmetadata', () => {
          recordings.value[index].duration = audio.duration;
          resolve();
        });
        audio.addEventListener('error', () => {
          recordings.value[index].duration = 0;
          resolve();
        });
      });
    }
  });
  await Promise.all(promises);
  saveRecordingsToStorage();
};

// 初始化录音数据
onMounted(async () => {
  recordings.value = savedRecordings || [];
  const savedRecordings = uni.getStorageSync('recordings');
  await loadDurations(); // 预加载时长
});

// 响应式状态
const playingIndex = ref(null);
const isRecording = ref(false);
const mediaRecorder = ref(null);
const audioChunks = ref([]);

// 格式化时间显示（MM:SS）
const formatTime = (seconds) => {
  if (!seconds) return "00:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

// 保存录音数据到内存
const saveRecordingsToStorage = () => {
  uni.setStorageSync('recordings', recordings.value);
};

// 停止所有音频
const stopAllAudios = (excludeIndex = -1) => {
  recordings.value.forEach((item, index) => {
    if (index === excludeIndex) return;
    if (item._audio) {
      item._audio.pause();
      item._audio.removeEventListener('timeupdate', () => updateProgress(index));
      item._audio.removeEventListener('ended', () => onAudioEnd(index));
      item._audio = null;
    }
    item.currentTime = 0;
    item.progress = 0;
  });
  playingIndex.value = null;
};

// 播放方法
const togglePlay = async (index) => {
  const item = recordings.value[index];

  // 先停止所有其他音频
  if (index !== playingIndex.value) {
    stopAllAudios(index);
  }

  // 当前音频已存在实例
  if (item._audio) {
    if (!item._audio.paused) {
      item._audio.pause();
      playingIndex.value = null;
    } else {
      await item._audio.play();
      playingIndex.value = index;
    }
    return;
  }

  // 创建新实例
  item._audio = new Audio(item.src);
  item._audio.addEventListener('timeupdate', () => updateProgress(index));
  item._audio.addEventListener('ended', () => onAudioEnd(index));

  try {
    await item._audio.play();
    playingIndex.value = index;
    if (!item._durationSet) {
      item.duration = item._audio.duration;
      item._durationSet = true;
    }
  } catch (err) {
    console.error('播放失败:', err);
  }
};

// 更新进度
const updateProgress = (index) => {
  const item = recordings.value[index];
  if (!item._audio) return;

  item.currentTime = item._audio.currentTime;
  item.progress = (item._audio.currentTime / item._audio.duration) * 100 || 0;
};

// 播放结束
const onAudioEnd = (index) => {
  stopAllAudios();
  recordings.value[index].currentTime = 0;
  recordings.value[index].progress = 0;
};

// 下载音频
const downloadAudio = (item) => {
  if (item.src.startsWith('blob:')) {
    const link = document.createElement('a');
    link.href = item.src;
    link.download = item.title + '.wav';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } else {
    const link = document.createElement('a');
    link.href = item.src;
    link.download = item.src.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

// 开始/停止录音
const toggleRecording = async () => {
  if (isRecording.value) {
    mediaRecorder.value.stop();
    isRecording.value = false;
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.value = new MediaRecorder(stream);

    audioChunks.value = [];

    mediaRecorder.value.ondataavailable = (e) => {
      audioChunks.value.push(e.data);
    };

    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' });

      const tempAudio = new Audio(URL.createObjectURL(audioBlob));
      tempAudio.onloadedmetadata = () => {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const newRecording = {
          title: `录音-${timestamp}`,
          duration: tempAudio.duration,
          currentTime: 0,
          src: URL.createObjectURL(audioBlob),
          progress: 0,
          _blob: audioBlob,
          _audio: null
        };

        recordings.value.push(newRecording);
        saveRecordingsToStorage();

        tempAudio.remove();
      };

      stream.getTracks().forEach(track => track.stop());

      uni.showToast({ title: '录音已保存', icon: 'success' });
    };

    mediaRecorder.value.start();
    isRecording.value = true;
    uni.showToast({ title: '正在录音...', icon: 'none' });

  } catch (error) {
    console.error('录音失败:', error);
    uni.showToast({
      title: `录音失败: ${error.message}`,
      icon: 'none'
    });
  }
};

// 选择音频文件
const chooseAudio = () => {
  uni.chooseFile({
    count: 1,
    type: "file",
    success: (res) => {
      const file = res.tempFiles[0];
      if (file && file.name.endsWith(".wav")) {
        const blobUrl = URL.createObjectURL(file);
        const newRecording = {
          title: file.name.replace(/\.[^/.]+$/, ""),
          duration: null,
          currentTime: 0,
          src: blobUrl,
          progress: 0,
          _file: file,
          _audio: null
        };

        recordings.value.push(newRecording);
        saveRecordingsToStorage();

        uni.showToast({ title: "添加成功", icon: "success" });
      } else {
        uni.showToast({ title: "请选择.wav文件", icon: "none" });
      }
    },
    fail: (err) => {
      console.error("选择失败:", err);
      uni.showToast({ title: "选择失败", icon: "none" });
    }
  });
};

// 清除内存
const clearMemory = () => {
  uni.showModal({
    title: '确认清除',
    content: '确定要清除所有用户录音吗？系统预置音色将保留',
    success: (res) => {
      if (res.confirm) {
        // 保留系统预置录音（通过判断是否包含_blob或_file属性）
        recordings.value = recordings.value.filter(item => 
          !('_blob' in item) && 
          !('_file' in item) &&
          item.src.startsWith('voice')
        );
        
        uni.setStorageSync('recordings', recordings.value);
        uni.showToast({ title: '用户录音已清除', icon: 'success' });
      }
    }
  });
};

// 删除录音
const deleteRecording = (index) => {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这条录音吗？',
    success: (res) => {
      if (res.confirm) {
        recordings.value.splice(index, 1);
        saveRecordingsToStorage();
        uni.showToast({ title: '删除成功', icon: 'success' });
      }
    }
  });
};

// 组件卸载前清理
onBeforeUnmount(() => {
  recordings.value.forEach(item => {
    if (item._audio) {
      item._audio.pause();
      item._audio.remove();
    }
    if (item.src.startsWith('blob:')) {
      URL.revokeObjectURL(item.src);
    }
  });
});
</script>

<style scoped>
/* 主容器 */
.container {
  display: flex;
  min-height: 100vh;
  background: #f5f7fb;
}

/* 主内容区 */
.content-wrapper {
  flex: 1;
  padding: 32rpx;
  background: white;
  border-radius: 24rpx 0 0 24rpx;
  box-shadow: -4rpx 0 12rpx rgba(0,0,0,0.05);
}

.content-header {
  font-size: 40px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 48rpx;
  padding-bottom: 24rpx;
  border-bottom: 2rpx solid #e8e8e8;
}

/* 声音列表 */
.voice-list {
  max-height: 600px;
  overflow-y: auto;
}

.voice-item {
  display: flex;
  align-items: center;
  padding: 24rpx;
  margin-bottom: 24rpx;
  background: #ffffff;
  border: 2rpx solid #e8e8e8;
  border-radius: 12rpx;
  transition: all 0.2s;
  height: 100px;
  width: 98%;
}

.voice-info {
  flex: 1;
  margin-right: 24rpx;
}

.voice-title {
  display: block;
  font-size: 32rpx;
  color: #1a1a1a;
  margin-bottom: 16rpx;
}

.voice-progress {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.time {
  font-size: 24rpx;
  color: #666;
}

.progress-bar {
  height: 8rpx;
  background: #e8e8e8;
  border-radius: 4rpx;
}

.progress {
  height: 100%;
  background: #007AFF;
  border-radius: 4rpx;
  transition: width 0.2s;
}

/* 控制按钮 */
.bottom-buttons {
  display: flex;
  justify-content: space-around;
  width: 98%;
  padding: 10px;
  margin-top: 10px;
  gap: 40px;
}

.button {
  position: relative;
  outline: none;
  border: none;
  padding: 20px 40px;
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 2px;
  border-radius: 30px;
  color: #ffffff;
  text-transform: uppercase;
  transition: 0.4s ease-in-out;
  cursor: pointer;
  z-index: 1;
  overflow: hidden;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 55px;
  width: 30%;
}

.start-button {
  background: linear-gradient(135deg, #74A5FF, #CEFF7E);
  box-shadow: 0 4px 6px rgba(116, 165, 255, 0.3);
}

.start-button.recording {
  background: linear-gradient(135deg, #FF0000, #FF4500);
  animation: pulse 1.5s infinite;
}

.stop-button {
  background: linear-gradient(135deg, #fe7bbf, #974ec3);
  box-shadow: 0 4px 6px rgba(255, 111, 97, 0.3);
}

.clear-button {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  box-shadow: 0 4px 6px rgba(255, 215, 0, 0.3);
}

.button::before {
  position: absolute;
  content: "";
  top: 0;
  left: -60%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1), transparent);
  transform: rotate(-45deg);
  transition: 0.8s;
  z-index: -1;
}

.button:hover::before {
  transform: rotate(0);
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2), transparent);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.voice-controls {
  display: flex;
  gap: 8rpx;
}

.icon-btn {
  width: 100rpx;
  height: 100rpx;
  font-size: 50rpx;
  padding: 6rpx;
  border-radius: 8rpx;
  background: rgba(255, 255, 255, 0.1);
  color: #007AFF;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, transform 0.2s;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.delete-btn {
  color: #ff4d4f;
}

.delete-btn:hover {
  background: rgba(255, 77, 79, 0.1);
}
</style>