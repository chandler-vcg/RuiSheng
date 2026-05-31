<template>
  <div class="card-container"> 
	<div class="panel-title">声速韵律：</div>
	  
    <div class="fixed-mode-container">
      <div class="data-card">
        <div class="card-backdrop"></div>
        <img class="card-logo" src="/static/speed.png" />
        <div class="card-content">
          <div class="card-title">语速控制</div>
          <div class="option-list">
            <button
              v-for="item in finalConfig.speedFactor"
              :key="item.value"
              class="option-btn"
              :class="{ active: state.speedFactor === item.value }"
              @click="state.speedFactor = item.value"
            >
              {{ item.text }}
            </button>
          </div>
        </div>
      </div>

      <div class="data-card">
        <div class="card-backdrop"></div>
        <img class="card-logo" src="/static/emotion.png" />
        <div class="card-content">
          <div class="card-title">情感控制</div>
          <div class="option-list">
            <button
              v-for="item in finalConfig.emotion"
              :key="item.value"
              class="option-btn"
              :class="{ active: state.temperature === item.value}"
              @click="setEmotion(item)"
            >
              {{ item.text }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const finalConfig = ref({
  speedFactor: [
    {text: '慢速', value: 0.6},
    {text: '正常', value: 1},
    {text: '快速', value: 1.5}
  ],
  emotion: [
    { text: '高兴', value: '1'},
    { text: '悲伤', value: '2'},
    { text: '愤怒', value: '3'},
    { text: '平静', value: '4'},
    { text: '惊讶', value: '5'},
    { text: '恐惧', value: '6'},
    { text: '喜好', value: '7'},
    { text: '厌恶', value: '8'},
    { text: '疑惑', value: '9'},
	{ text: '期待', value: '10'},
	{ text: '自信', value: '11'},
	{ text: '担忧', value: '12'},
	{ text: '怀念', value: '13'},
	{ text: '激动', value: '14'},
	{ text: '羞涩', value: '15'}
  ]
})

const state = ref({
  speedFactor: 1,
  temperature: '1'
})

// watch监听参数变化
watch(
  () => state.value,
  (newVal) => {
    emit('update-params', {
      speedFactor: Number(newVal.speedFactor),
      temperature: Number(newVal.temperature)
    })
  },
  { deep: true }
)

const emit = defineEmits(['update-params'])

const setEmotion = (item) => {
  state.value.temperature = item.value
}
</script>

<style scoped>
.card-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  max-width: 760px;
}

.panel-title {
  left: 28px;
  top: 28px;
  font-size: 24px;
  color: #444;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.fixed-mode-container {
  display: flex;
  gap: 40px;
}

.data-card {
  margin-top: 30px;
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

.option-list {
  position: absolute;
  right: 180px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 100px;
  scrollbar-width: none;
  -ms-overflow-style: none;
  overflow-y: auto;
  padding-top: 40px;
  margin-right: 110px;
}

.option-btn {
  padding: 6px 12px;
  border: 1px solid #e0e3e9;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
  width: 110px;
  min-height: 51px;
}

.option-btn:hover {
  border-color: #007aff;
  color: #007aff;
}

.option-btn.active {
  background: #007aff;
  color: white;
  border-color: #007aff;
}
</style>