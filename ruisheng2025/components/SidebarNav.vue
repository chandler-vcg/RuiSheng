<template>
  <view class="button-sidebar">
	
	<!-- 顶部头像区域 -->
    <view class="profile-section">
      <image 
        class="avatar"s
        src="/static/touxiang.png" 
        mode="aspectFill"
      />
      <text class="username">睿声</text>
    </view>
	
	<view class="logo-container">
	  <image 
	    class="logo-image"
	    src="/static/ruisheng.jpg" 
	  />
	  <text class="logo-text">Sagacious Resonance</text>
	</view>
    <view 
      v-for="(item, index) in menuItems"
      :key="index"
      class="nav-button"
      :class="{ active: activeIndex === index }"
      @click="handleClick(index)"
    >
      {{ item.label }}
    </view>
  </view>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  menuItems: {
    type: Array,
    default: () => [
      { label: '我的声音集', path: '/pages/index/voice' },
      { label: '语音助手', path: '/pages/index/explaination' },
      { label: '静态课件', path: '/pages/index/ppt_ppt' },
	  { label: '静态课件', path: '/pages/index/ppt_video' },
      { label: '视频换声', path: '/pages/index/video' },
	  { label: '退出登录', path: '/pages/index/login' }
    ]
  },
  activeIndex: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['navigate'])

// 内部维护激活状态
const activeIndex = ref(props.activeIndex)

// 监听父组件传入的activeIndex变化
watch(
  () => props.activeIndex,
  (newVal) => {
    activeIndex.value = newVal
  }
)

const handleClick = (index) => {
  activeIndex.value = index
  emit('navigate', props.menuItems[index].path)
}
</script>

<style scoped>
/* 头像区域 */
.profile-section {
  padding: 40rpx 20rpx;
  display: flex;
  align-items: center;
  border-bottom: 2rpx solid #f0f0f0;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
}

.username {
  font-size: 36px;
  font-weight: 600;
  color: #333;
  letter-spacing: 1rpx;
}
	
	
.button-sidebar {
  width: 240px;
  background: #ffffff;
  padding: 20rpx 10rpx;
  box-shadow: 4rpx 0 12rpx rgba(0,0,0,0.08);
}

.nav-button {
  margin: 12rpx 16rpx;
  padding: 28rpx 32rpx;
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #666;
  background: #f8f8f8;
  box-shadow: 0 2rpx 6rpx rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.nav-button.active {
  background: #007AFF;
  color: white;
  box-shadow: 0 4rpx 12rpx rgba(0,122,255,0.3);
}

/* Logo样式 */
.logo-container {
  display: flex;
  align-items: center;
  height:60px;
}

.logo-image {
  width: 110rpx;
  height: 110rpx;
}

.logo-text {
  font-size: 32rpx;
  font-weight: 600;
  color: #007AFF;
  letter-spacing: 1rpx;
}
</style>