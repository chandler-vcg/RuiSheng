import subprocess
import whisper
from moviepy.editor import VideoFileClip,AudioFileClip
import requests
from fastapi import FastAPI,Body
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/files", StaticFiles(directory="."), name="files")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#更换视频的音频
def change_audio(video_path,audio_path,output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print("音频更换完成")

#合成语音
def text_to_speech(text,reference_audio,changed_audio,top_k,top_p,temperature):
    url = "http://127.0.0.1:9880/tts"
    params = {
        "text": text,
        "text_lang": "zh",
        "ref_audio_path": reference_audio,
        "prompt_lang": "zh",
        "media_type": "wav",
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        'prompt_text': ''
    }

    response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        with open(changed_audio, "wb") as f:
            f.write(response.content)
        print("语音合成成功！")
    else:
        print("错误2:", response.json())


# 1. 提取音频
def extract_audio(video_path, audio_path):
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("音频提取完成")


# 2. 语音识别并生成字幕
def generate_subtitles(audio_path, srt_path,reference_audio,changed_audio, top_k, top_p, temperature):
    model = whisper.load_model("medium")  # 可选："tiny", "base", "small", "medium", "large"
    result = model.transcribe(audio_path)
    text_list=[]
    # 生成 SRT 字幕
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            text_list.append(text)
            f.write(f"{i + 1}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{text}\n\n")
    text="".join(text_list)
    text_to_speech(text, reference_audio,changed_audio, top_k, top_p, temperature)
    print("字幕生成完成")


# 时间戳格式转换
def format_timestamp(seconds):
    millisec = int((seconds - int(seconds)) * 1000)
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02},{millisec:03}"


# 3. 硬编码字幕到视频
def add_subtitles(video_path, srt_path, output_path):
    command = [
        "ffmpeg", "-i", video_path, "-vf", f"subtitles={srt_path}:force_style='FontSize=15,PrimaryColour=&HFFFFFF&'",
        "-c:a", "copy", output_path, "-y"
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("字幕已嵌入到视频")

@app.post("/process_video")
def process_video(
    input_video: str = Body(...),
    output_audio: str = Body(...),
    changed_audio: str = Body(...),
    reference_audio: str = Body(...),
    output_srt: str = Body(...),
    output_video: str = Body(...),
    output_final_video: str = Body(...),
    top_k: int = Body(...),
    top_p: int = Body(...),
    temperature: int = Body(...)
):
    # 执行流程
    extract_audio(input_video, output_audio)
    generate_subtitles(output_audio, output_srt,reference_audio, changed_audio, top_k, top_p, temperature)
    add_subtitles(input_video, output_srt, output_video)
    print("处理完成，最终视频已保存")
    change_audio(output_video ,changed_audio ,output_final_video)

    return {"message": "video 处理完成", "output_path": output_final_video}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)