<template>
  <div class="card-container">
	<div class="panel-title">模式选择：</div>
    <div class="fixed-mode-container">
      <div 
        class="data-card"
        :class="{ 'active-card': selectedType === 'static' }"
        @click="selectType('static')"
      >
        <div class="card-backdrop"></div>
        <img class="card-logo" src="/static/ppt.png" />
        <div class="card-content">
          <div class="card-title">满分静态课件</div>
        </div>
      </div>

      <div 
        class="data-card"
        :class="{ 'active-card': selectedType === 'video' }"
        @click="selectType('video')"
      >
        <div class="card-backdrop"></div>
        <img class="card-logo" src="/static/video.png" />
        <div class="card-content">
          <div class="card-title">满分视频课件</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedType = ref('video')
const emit = defineEmits(['type-change'])

const selectType = (type) => {
  selectedType.value = type
  emit('type-change', type)
}
</script>

<style scoped>
.card-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  max-width: 760px;
}

.fixed-mode-container {
  display: flex;
  gap: 40px;
}

.data-card {
  position: relative;
  overflow: hidden;
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.2s;
  width: 600px;
  height: 90px;
}

.data-card:hover {
  transform: translateY(-2px);
}

.card-title {
  color: #666;
  font-size: 20px;
}

.card-backdrop {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: radial-gradient(
    circle at center,
    rgba(173, 216, 230, 0.5) 0%,
    rgba(173, 216, 230, 0.5) 70%,
    transparent 100%
  );
}

.card-logo {
  position: absolute;
  right: 42px;
  top: 50%;
  transform: translateY(-50%);
  width: 45px;
  height: 45px;
  object-fit: contain;
  opacity: 0.8;
  z-index: 1;
}

.card-content {
  position: relative;
  z-index: 2;
  width: 500px;
}

.active-card {
  border: 2px solid #007aff;
  box-shadow: 0 4px 16px rgba(0, 122, 255, 0.2);
}

.panel-title {
	margin-bottom: 10px;
  font-size: 24px;
  color: #444;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

</style>