# 睿声 (Sagacious Resonance)

基于 Uni-app(Vue 3) 的前端应用，整合 GPT-SoVITS 的语音合成与试听生成能力，提供语音助手、音频库管理、PPT/视频课件生成与视频换声等功能。

## 功能一览

1. **语音助手（TTS）**：输入文本 + 参考音频，生成语音并支持播放/下载。
2. **语音与情感参数**：支持语速与情感强度等参数调节。
3. **我的音频库**：内置音频库，支持上传、录音、播放、删除与本地缓存。
4. **静态课件（PPT → PPT）**：上传 PPT，生成处理后的 PPT。
5. **视频课件（PPT → Video）**：上传 PPT，生成带音频的视频课件。
6. **视频换声**：上传视频并选择音色，生成新的配音视频。

## 技术栈

- **Uni-app**
- **Vue 3**
- **HBuilderX**（推荐运行/调试）

## 页面一览

| 页面 | 路由 | 说明 |
|---|---|---|
| 登录 | `pages/index/login` | 登录入口与导航 |
| 语音助手 | `pages/index/explaination` | 文本转语音与情感参数 |
| 我的音频库 | `pages/index/voice` | 音色管理与录音 |
| 静态课件 | `pages/index/ppt_ppt` | PPT → PPT |
| 视频课件 | `pages/index/ppt_video` | PPT → Video |
| 视频换声 | `pages/index/video` | Video → 新配音 |

## 本地运行（推荐 HBuilderX）

1. 使用 HBuilderX 打开项目目录 `D:\睿声\ruisheng2025`。
2. 选择"运行到浏览器"或"运行到 App/小程序"。
3. 确保后端服务已启动（见下文）。

## 后端接口依赖

前端默认请求本地接口，请确保对应服务可用，或按需修改组件中的 URL。

| 功能 | 端点 |
|---|---|
| 文本转语音 | `POST http://127.0.0.1:8000/text_to_speech` |
| PPT → PPT | `POST http://127.0.0.1:8000/process_ppt` |
| PPT → Video | `POST http://127.0.0.1:8000/ppt_to_video` |
| 视频换声 | `POST http://localhost:8080/process` |

## 目录结构（核心）

```
ruisheng2025/
├── pages/
│   └── index/           # 登录、语音助手、课件与视频换声页面
├── components/
│   └── card/            # 语音/情感/生成等组件
│   └── Voicecontent/    # 音频库管理组件
├── static/             # 静态资源
├── voice/              # 预设音色资源
└── manifest.json       # Uni-app 配置
```
