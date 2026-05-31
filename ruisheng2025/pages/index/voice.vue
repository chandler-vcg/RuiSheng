<template>
  <view class="container">
    <SidebarNav :active-index="0" @navigate="handleNavigate"/>
    <view class="content-wrapper">
		<VoiceContent />
    </view>
  </view>
</template>

<script setup>
import SidebarNav from '@/components/SidebarNav.vue'
import VoiceContent from '@/components/Voicecontent/VoiceContent.vue'

const handleNavigate = (path) => {
  uni.navigateTo({ url: path })
}
</script>

<style scoped>
/* 新增容器flex布局 */
.container {
  display: flex;
  min-height: 100vh;
}

/* 主内容区调整 */
.content-wrapper {
  flex: 1;
  padding: 32rpx;
  background: white;
  border-radius: 24rpx 0 0 24rpx;
  /* box-shadow: -4rpx 0 12rpx rgba(0,0,0,0.05); //方便看盒子的形状*/
  min-height: calc(100vh - 64rpx);
  overflow-y: auto;
  width: 600px;
}
</style>