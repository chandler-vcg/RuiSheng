<template>
  <view class="container">
    <!-- 主内容区 -->
    <view class="content-wrapper">
	  <div class="panel-title">声音集：</div>
      <!-- 声音列表 -->
      <view class="voice-list">
        <view
          class="voice-item"
          v-for="(item, index) in recordings"
          :key="index"
		  :class="{ selected: selectedVoiceIndex === index }"
          @click="selectVoiceItem(index)"
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
          <view class="voice-controls" @click.stop>
            <button class="icon-btn" @click.stop="togglePlay(index)">
              {{ playingIndex === index ? '⏸' : '▶️' }}
            </button>
          </view>
        </view>
      </view>
    
    </view>
  </view>
</template>

<script setup>
import { ref, onBeforeUnmount, onMounted } from 'vue';

// 录音列表数据
const recordings = ref([]);

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
  const savedRecordings = uni.getStorageSync('recordings');
  recordings.value = savedRecordings || [];
  await loadDurations(); // 预加载时长
});

// 响应式状态
const playingIndex = ref(null);
const selectedVoiceIndex = ref(-1); // 当前选中项的索引

// 定义emits
const emit = defineEmits(['select-audio'])

// 点击处理方法
const selectVoiceItem = (index) => {
  selectedVoiceIndex.value = index;
  // 触发事件传递选中音频路径
  emit('select-audio', recordings.value[index].src)
};

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
  background: white;
  overflow: visible; /* 确保不裁剪子元素 */
}

.panel-title {
  left: 28px;
  margin-top: 20px;
  font-size: 24px;
  color: #444;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

/* 主内容区 */
.content-wrapper {
  border: 2px solid #e0e3e9;
  flex: 1;
  padding: 32rpx;
  background: white;
  border-radius: 40rpx;
  box-shadow: -4rpx 0 12rpx rgba(0,0,0,0.05);
  height: 390px;
}

/* 声音列表 */
.voice-list {
  max-height: 280px;
  overflow-y: auto;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
  margin-top: 30px;
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
}

.voice-item.selected {
  border-color: #06a7ff !important;
  background: #f0faff !important;
  box-shadow: 0 2px 8px rgba(6, 167, 255, 0.15);
}

/* 增加点击动画效果 */
.voice-item:active {
  transform: scale(0.98);
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

</style>