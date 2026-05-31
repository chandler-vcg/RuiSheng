<template>
  <div class="container">
	<div class="panel-title">语音生成器：</div>
    <div class="record-container">
      <div
        class="btn card1 record-button"
        :class="{ 'pulse': isPulsing }"
        @click="handlePlayAudio"
      >
        <image class="sound-icon" src="/static/sound.png"></image>
      </div>
    </div>

    <div class="button-group">
      <button @click="synthesize">合成</button>
      <button @click="download">下载</button>
    </div>
  </div>
</template>
 
 <script setup>
 import { ref } from 'vue'
 
 const state = ref({
   isLoading: false
 })
 
 // 播放相关状态
 const isPulsing = ref(false)
 const audioContext = ref(null)
 const isPlaying = ref(false)
 const audioUrl = ref(null)
const errorMessage = ref('');

//props声明
const props = defineProps({
  inputText: {
    type: String,
    default: ''
  },
  refAudioPath: {
    type: String,
    default: ''
  },
  emotionParams: {
      type: Object,
      default: () => ({
        speedFactor: 1,
        temperature: "1",
      })
    }
})

//emits 声明
const emit = defineEmits(['update-text'])
 
const synthesize = async () => {
  console.log("发送参数:", {
    text: props.inputText,
    ref_audio: props.refAudioPath,
    speed_factor: props.emotionParams.speedFactor,
    emotion: props.emotionParams.temperature
  });
  try {
    // 参数校验
    if (!props.refAudioPath) {
    	uni.showToast({ title: '请先选择音频模型', icon: 'none' })
    	return
    }
    	
    if (!props.inputText.trim()) {
    	uni.showToast({ title: '请输入合成文本', icon: 'none' })
    	return
    }
    	
    state.value.isLoading = true 
    	  
    uni.showLoading({ title: "AI正在飞速合成语音..." }); // 显示加载提示

    const response = await uni.request({ 
      url: "http://127.0.0.1:8000/text_to_speech",
      method: "POST",
      data: {
        ref_audio: props.refAudioPath,
        text: props.inputText,
        speed_factor: props.emotionParams.speedFactor,
        emotion: props.emotionParams.temperature
      },
      header: {
        "Content-Type": "application/json",
      },
      responseType: "arraybuffer",
    });

    uni.hideLoading();

    // 处理二进制错误响应
    if (response.statusCode !== 200) {
      const decoder = new TextDecoder('utf-8');
      const errorData = decoder.decode(new Uint8Array(response.data));
      throw new Error(`API错误: ${errorData}`);
    }

    // 成功处理
    const audioBlob = new Blob([response.data], { type: "audio/wav" });
    audioUrl.value = URL.createObjectURL(audioBlob);
	uni.showToast({ title: '合成成功', icon: 'none' })

  } catch (err) {
    console.error("请求失败详情:", err);
	uni.showToast({ title: '合成失败', icon: 'none' })
  } finally {
    state.value.isLoading = false;
  }
};
 
// 初始化音频上下文
const initAudio = () => {
  if (!audioContext.value) {
    audioContext.value = uni.createInnerAudioContext();
    audioContext.value.onPlay(() => {
      isPlaying.value = true;
      isPulsing.value = true;
    });
    audioContext.value.onEnded(() => {
      isPlaying.value = false;
      isPulsing.value = false;
    });
    audioContext.value.onError((err) => {
      console.error('播放错误:', err);
      uni.showToast({ title: '播放失败', icon: 'none' });
      isPlaying.value = false;
      isPulsing.value = false;
    });
  }
};
 
 // 处理音频播放
 const handlePlayAudio = async () => {
	console.log('音频',props.refAudioPath)
	console.log('文字',props.inputText)
	console.log('语速以及情感',props.emotionParams.speedFactor,props.emotionParams.temperature,props.emotionParams.fragmentInterval)
   if (!audioUrl.value) {
     uni.showToast({ title: "请先点击'合成'按钮", icon: "none" })
     return
   }
 
   if (isPlaying.value) {
     audioContext.value.stop()
     isPlaying.value = false
     isPulsing.value = false
     return
   }
 
   initAudio()
   audioContext.value.src = audioUrl.value
   await audioContext.value.play()
 };
 
 // 下载音频
 const download = () => {
   if (!audioUrl.value) {
     uni.showToast({ title: '请先合成音频', icon: 'none' })
     return
   }
 
   const link = document.createElement('a')
   link.href = audioUrl.value
   link.download = 'audio.wav'
   document.body.appendChild(link)
   link.click()
   document.body.removeChild(link)
 };
 </script>
 
<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; 
  padding: 0 40px; 
}

.panel-title {
  margin-top: 20px;
  font-size: 24px;
  color: #444;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.record-container {
  margin-top: 40px;
  flex-shrink: 0; /* 防止被压缩 */
}
 
 .record-button {
   width: 250px;
   height: 250px;
   border-radius: 50%;
   display: flex;
   align-items: center;
   justify-content: center;
   box-shadow: 0 0 30px rgba(116, 165, 255, 0.8);
   transition: transform 0.3s ease;
 }
 
 .record-button.pulse {
   animation: pulse 2.5s infinite;
 }
 
 @keyframes pulse {
   0% { transform: scale(0.9); }
   50% { transform: scale(1.2); }
   100% { transform: scale(0.9); }
 }
 
 .sound-icon {
   width: 100px;
   height: 100px;
 }
 
.button-group {
  display: flex;
  flex-direction: column; /* 改为垂直排列 */
  gap: 40px;
  margin-right: 30px;
}

 button {
   margin-top: 50px;
   width: 200px;
   height: 75px;
   padding: 12px 24px;
   border: none;
   border-radius: 10px;
   font-size: 20px;
   background: #06a7ff;
   color: white;
   cursor: pointer;
   transition: opacity 0.2s;
 }
 
button:active {
   opacity: 0.8;
 }
</style>