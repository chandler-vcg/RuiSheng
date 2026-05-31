<template>
  <slot name="header">
    <text class="title">PPT合成台</text>
  </slot>

  <div class="steps">
    <div 
      v-for="(step, index) in finalConfig.steps" 
      :key="step"
      class="step"
      :class="{ active: state.currentStep === step }"
    >
      {{ step }} {{ finalConfig.stepTitles[step - 1] }}
      <span v-if="index < finalConfig.steps.length -1" class="arrow">→</span>
    </div>
  </div>

  <!-- 步骤内容 -->
  <div v-show="state.currentStep === 1" class="step-content">
    <div class="options">
      <div 
        v-for="(option, index) in finalConfig.storageOptions"
        :key="index"
        class="option-card"
        :class="{ 
          selected: state.selectedStorageMode === index,
          disabled: !option.value
        }"
        @click="option.value && (state.selectedStorageMode = index)"
      >
        {{ option.text }}
      </div>
    </div>
	
	<!-- 上传ppt按钮 -->
	<div class="button-group step1-buttons">
	    <button 
	      class="prev-btn"
	      :disabled="state.currentStep === 1"
	      @click="prevStep"
	    >
	      上一步
	    </button>
	    <button 
	      class="upload-btn"
	      @click="handleUploadPPT"
	    >
	      上传PPT
	    </button>
	    <button 
	      class="next-btn"
	      @click="handleAction"
	      :disabled="state.isLoading"
	    >
	      {{ getButtonText }}
	    </button>
	</div>
	
  </div>

  <div v-show="state.currentStep === 2" class="step-content">
    <div class="options">
      <div 
        v-for="(option, index) in finalConfig.syncOptions"
        :key="index"
        class="option-card"
        :class="{ selected: state.selectedSyncType === index }"
        @click="state.selectedSyncType = index"
      >
        {{ option.text }}
      </div>
    </div>
  </div>
  
  <div v-show="state.currentStep === 3 && state.showStep3" class="step-content">
      <div class="options">
        <template v-if="state.selectedSyncType === 0">
          <!-- 有声课件选项 -->
          <div 
            v-for="(option, index) in finalConfig.audioOptions"
            :key="index"
            class="option-card"
            :class="{ selected: state.selectedPPTOption === index }"
            @click="state.selectedPPTOption = index"
          >
            {{ option.text }}
          </div>
        </template>
        
        <template v-else>
          <!-- 视频预览区域 -->
          <div class="video-preview">
            <div v-if="!previewVideoUrl" class="video-placeholder">视频预览区域</div>
            <video v-else :key="previewVideoUrl" :src="previewVideoUrl" controls class="preview-video" muted autoplay></video>
          </div>
        </template>
      </div>
      
      <div class="button-group_3">
      <button class="prev-btn" @click="prevStep">上一步</button>
      <div class="action-buttons">
        
        <button 
          class="next-btn"
          :disabled="state.isLoading"
          @click="state.selectedSyncType === 0 ? handlePPTSynthesis() : handleVideoSynthesis()"
        >
          {{ synthesisButtonText }}
        </button>
		
		<button
		  class="download-btn"
		  :disabled="!state.isSynthesisComplete"
		  @click="handleDownload(state.selectedSyncType === 0 ? 'ppt' : 'video')"
		>
		  点击下载
		</button>
      </div>
    </div>
    </div>

  <div class="button-group" v-show="state.currentStep !== 1 && state.currentStep !== 3">
    <button 
      class="prev-btn"
      :disabled="state.currentStep === 1"
      @click="prevStep"
    >
      上一步
    </button>
    <button 
      class="next-btn"
      @click="handleAction"
      :disabled="state.isLoading"
    >
      {{ getButtonText }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
})

// 录音数据响应式引用
const recordings = ref([]);
const pptFile = ref(null);
const outputFilePath = ref("updated_presentation.pptx"); // 后端处理后 PPT 的保存路径
const videoOutputPath = "output/video_temp.mp4";
const videoWithSubtitlePath = "output/video_final.mp4";
const previewVideoUrl = ref(""); // 频预览地址

// 从本地存储获取录音数据
onMounted(() => {
  const savedRecordings = uni.getStorageSync('recordings')
  if(savedRecordings) {
    recordings.value = savedRecordings.map(item => ({
      text: item.title,
      value: item.src
    }))
  }
})

// 合并配置（改为计算属性）
const finalConfig = computed(() => ({
  steps: [1,2,3],
  stepTitles: ['音频选择', '模式选择',state.value.selectedSyncType === 0 ? 'PPT合成' : '视频合成'],
  storageOptions: recordings.value.length > 0 
    ? recordings.value 
    : [{text: '无可用音色', value: ''}], // 兜底显示
  syncOptions: [
    { text: '有声课件', value: '1' },
    { text: '视频课件', value: '2' }
  ],
  audioOptions: [
    { text: '原态生成', value: '1' },
    { text: '智能润色', value: '2' },
    { text: '逸韵修裁', value: '3' }
  ],
  ...props.config
}))

// 状态管理
const state = ref({
  currentStep: 1,
  selectedStorageMode: 0,
  selectedSyncType: 0,
  isLoading: false,
  showStep3: false,//步骤3显示
  selectedPPTOption: 0,
  isSynthesisComplete: false
})

// 计算属性
const getButtonText = computed(() => {
  if(state.value.isLoading) return '生成中...'
  return state.value.currentStep === finalConfig.value.steps ? '下一步' : '下一步'
})
// 第三步计算属性
const synthesisButtonText = computed(() => 
  state.value.selectedSyncType === 0 ? '合成PPT' : '合成视频'
)

const prevStep = () => {
  if (state.value.currentStep > 1) {
    if(state.value.currentStep === 3) {
      state.value.showStep3 = false
    }
    state.value.currentStep--
  }
}

// 最终步骤判断条件
const handleAction = async () => {
  //步骤1判断用户是否上传PPT
  if (state.value.currentStep === 1) {
    if (!pptFile.value?.path) {
      uni.showToast({
        title: '请先上传PPT文件',
        icon: 'none',
        duration: 2000
      });
      return; // 阻止继续执行
    }
  }
  
  // 步骤2处理分支
  if (state.value.currentStep === 2) {
    state.value.showStep3 = true
  }

  if (state.value.currentStep >= finalConfig.value.steps.length) {
    return;
  }
  
  //判断最后一步
  if (state.value.currentStep >= finalConfig.value.steps.length) {
    return;
  }
  
  // 使用新的对象触发响应式更新
  state.value = {
    ...state.value,
    currentStep: state.value.currentStep + 1
  };
}

// 选择PPT文件
const handleUploadPPT = async () => {
  try {
    const res = await uni.chooseFile({
      count: 1,
      extension: ['.ppt', '.pptx'],
      type: 'file'
    });

    if (res?.tempFiles?.length > 0) {
      // 存储文件信息
      pptFile.value = {
        file: res.tempFiles[0],
        path: res.tempFiles[0].path
      };
      console.log('PPT文件路径:', pptFile.value.path);
      uni.showToast({ title: 'PPT上传成功', icon: 'success' });
    }
  } catch (error) {
    console.error('文件选择失败:', error);
    previewImage.value = null;
    uni.showToast({ title: '文件上传失败', icon: 'none' });
  }
};

// 合成PPT
const handlePPTSynthesis = async () => {
  if (!pptFile.value?.path) {
    uni.showToast({ title: '请先选择PPT文件', icon: 'none' });
    return;
  }

  try {
	console.log('pptFile.value',pptFile.value.path);
	console.log('outputFilePath.value',outputFilePath.value);
	console.log(recordings.value[state.value.selectedStorageMode].value);
	console.log(finalConfig.value.audioOptions[state.value.selectedPPTOption].value);
	
    const response = await uni.request({
      url: `http://127.0.0.1:8000/process_ppt?ppt_path=${'try.pptx'}&output_path=${outputFilePath.value}&reference_audio=${recordings.value[state.value.selectedStorageMode].value}&choice=${finalConfig.value.audioOptions[state.value.selectedPPTOption].value}`,
      method: "POST",
      header: { "Content-Type": "application/json" },
      data: {
        ppt_path: 'try.pptx', // 传递文件路径
        output_path: outputFilePath.value,
		reference_audio:recordings.value[state.value.selectedStorageMode].value,
		choice:finalConfig.value.audioOptions[state.value.selectedPPTOption].value
      }
    });
	
	
    if (response.statusCode === 200) {
      state.value.isSynthesisComplete = true;
      uni.showToast({ title: '处理成功', icon: 'success' });
      console.log('结果:', response.data);
    } else {
      uni.showToast({ title: response.data.error || '处理失败', icon: 'none' });
	  console.log('结果:', response.data);
    }
  } catch (error) {
    console.error('上传失败:', error);
    uni.showToast({ title: '上传失败', icon: 'none' });
  }
};

//合成视频
const handleVideoSynthesis = async () => {
  state.value.isLoading = true;
  try {
    const response = await uni.request({
      url: 'http://127.0.0.1:8000/ppt_to_video', // 确保与后端地址一致
      method: "POST",
      header: { "Content-Type": "application/json" },
      data: {
        ppt_path: 'try.pptx',//pptFile.value.path,
        video_output: videoOutputPath,
        video_src_output: videoWithSubtitlePath,
		reference_audio:recordings.value[state.value.selectedStorageMode].value,
      }
    });

    if (response.statusCode === 200) {
      // 合成成功处理
      state.value.isSynthesisComplete = true;
      previewVideoUrl.value = `http://127.0.0.1:8000/output/video_final.mp4`; // 更新预览视频地址
      uni.showToast({ title: '视频合成成功', icon: 'success' });
    } else {
      // 处理后端返回的错误
      const errorMsg = response.data?.detail || '视频合成失败';
      uni.showToast({ title: errorMsg, icon: 'none' });
    }
  } catch (error) {
    console.error('视频合成请求失败:', error);
    uni.showToast({ title: '请求失败，请检查网络', icon: 'none' });
  } finally {
    state.value.isLoading = false;
  }
}

//下载视频和PPT
const handleDownload = async (type) => {
  try {
    let fileUrl = '';
    let fileName = '';
    
    if (type === 'ppt') {
      fileName = `synthesized_${Date.now()}.pptx`;
    } else if (type === 'video') {
      fileName = `synthesized_video_${Date.now()}.mp4`;
    }

    // 创建下载链接
    const link = document.createElement('a');
    link.href = fileUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    uni.showToast({ title: '选择下载位置', icon: 'success' });
    
  } catch (error) {
    uni.showToast({ title: `下载失败：${error.message}`, icon: 'none' });
  }
}
</script>

<style scoped>
.title {
  font-size: 35px;
  margin-left: 690px;
  margin-bottom: 30px;
}

.steps {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-left: 500px;
  width: fit-content;
  font-size: 23px;
  margin-top: 10px;
  margin-left: 590px;
}

.step {
  color: #666;
  font-size: 20px;
  position: relative;
}

.step.active {
  color: #06a7ff;
  font-weight: bold;
}

.options {
  margin: 20px 0;
}

.option-card {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 15px;
  margin: 10px 0;
  cursor: pointer;
  transition: all 0.3s;
}

.option-card:hover {
  border-color: #06a7ff;
  background: #f0faff;
}

.option-card.selected {
  border-color: #06a7ff;
  background: #f0faff;
}

.disabled {
  opacity: 0.6;
  pointer-events: none;
  background: #f5f5f5;
}

.button-group {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
}

.button-group_3{
	margin-top: 30px;
	display: flex;
	justify-content: space-between;
	margin-right: 80px;
}

.button {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.prev-btn {
  background: #eee;
  width: 200px;
  height: 75px;
  padding-top: 14px;
}

.next-btn {
  background: #06a7ff;
  color: white;
  width: 200px;
  height: 75px;
  padding-top: 14px;
  margin-right: 200px;
}

/* 上传PPT钮组样式 */
.step1-buttons {
  margin-top: 30px;
  gap: 100px;
}

.step1-buttons button {
  flex: 1;
  padding: 12px 0;
  border-radius: 6px;
  font-size: 16px;
  transition: opacity 0.2s;
}

.upload-btn {
  background: #4CAF50;
  color: white;
  padding-top: 14px;
  height: 75px;
}

.step1-buttons button:active {
  opacity: 0.8;
}

/* 视频预览样式 */
.video-preview {
  margin-top: 20px;
  margin-left: 300px;
  width: 80%;
  max-width: 1000px;
  min-height: 450px;
  background: #f5f5f5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-placeholder {
  color: #666;
  font-size: 18px;
}

.preview-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.action-buttons {
  display: flex;
  gap: 20px;
}

.download-btn {
  background: #4CAF50;
  color: white;
  width: 200px;
  height: 75px;
  padding-top: 14px;
  margin-right: 200px;
}

.download-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
  opacity: 0.6;
}
</style>