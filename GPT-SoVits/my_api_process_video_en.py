import subprocess
import whisper
import uvicorn
from openai import OpenAI
from langdetect import detect
from pydub import AudioSegment
import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
class ProcessRequest(BaseModel):
    video_path: str
    speed_factor: float
    output_path: str
    reference_audio: str
    top_k: int
    top_p: float

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#提取视频的音频
def extract_audio_from_video(video_path, audio_path):
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("音频提取完成")
#extract_audio_from_video(r"C:\Users\17555\Desktop\final_video.mp4",r"C:\Users\17555\Desktop\audio.wav")

#从音频中提取文本
def extract_text_from_audio(audio_path):
    model = whisper.load_model("medium")  # 可选："tiny", "base", "small", "medium", "large"
    result = model.transcribe(audio_path, language="Chinese", initial_prompt="以下是普通话的句子")
    #检测语言
    source_lang = result.get("language")
    print(f"检测到语言: {source_lang}")
    # 提取每一句话，放入列表
    text_list = [segment["text"] for segment in result["segments"]]

    # 输出结果（可选）
    for i, text in enumerate(text_list):
        print(f"{i + 1}: {text}")

    print("文本提取完成")
    print("text_list:",text_list)
    return text_list
#text=extract_text_from_audio(r"C:\Users\17555\Desktop\audio.wav")
#print(text)

def translate_text(text_list):
    result_list=[]
    api = "sk-97911fd3236c466f9b4d65dfddef6385"
    client = OpenAI(api_key=api, base_url="https://api.deepseek.com")
    #lang=detect(text_list[0])
    #print("lang:",lang)
    #if(lang=="zh-cn"):
     #   language="英文"
    #else:
    #    language="中文"
    #print("翻译为language:{}".format(language))
    for text in text_list:
        prompt2="直接翻译这段话为{}:{}，除了原文对应的内容，不要给我任何多余的内容".format("英文",text)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt2},
            ],
            temperature=1.3,
            stream=False
        )
        result = response.choices[0].message.content
        result_list.append(result)
    print("翻译完成！")
    print(result_list)
    return result_list
#result=translate_text(["用于跳出当前循环的剩余部分，直接进入下一次循环。","也可以实例化一个元素为实例化对象的数组"])
#print(result)

#合并音频
def merge_audio_files(audio_paths, output_path):
    """
    合并多个音频文件为一个音频文件
    :param audio_paths: List[str] - 音频文件路径列表
    :param output_path: str - 合并后的输出音频文件路径（如 'output.wav'）
    """
    combined = AudioSegment.empty()

    for path in audio_paths:
        if not os.path.exists(path):
            print(f"音频文件不存在: {path}")
            continue
        segment = AudioSegment.from_file(path)
        combined += segment

    combined.export(output_path, format="wav")  # 支持 mp3/wav/ogg 等
    print(f"合并完成，输出文件: {output_path}")

# 调用So-VITS API生成语音，每页ppt的文字单独一个音频，然后返回一个包含这些音频文件名的列表
def text_to_speech(texts,reference_audio,speed_factor,top_k=5,top_p=1,temperature=1):#接收一个字符串列表
    name_list=[];
    url = "http://127.0.0.1:9880/tts"
    for text in texts:
        params = {
            "text": text,
            "text_lang": "zh",
            "ref_audio_path": reference_audio,
            "prompt_lang": "zh",
            "media_type": "wav",
            "speed_factor":speed_factor,
            "top_k":top_k,
            "top_p":top_p,
            "temperature":temperature
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            with open("output{}.wav".format(texts.index(text)), "wb") as f:
                name_list.append("output{}.wav".format(texts.index(text)))
                f.write(response.content)
            print("语音合成成功！")
        else:
            print("错误:", response.json())
    print("音频列表：",name_list)
    return name_list

#提取文本
#texts=extract_text_from_audio(audio_path)
#翻译文本
#texts=translate_text(texts)
#合成语音
#audio_list=text_to_speech(texts)
#合并音频
#merge_audio_files(audio_list,r"C:\Users\17555\Desktop\final_audio.wav")

#替换视频的音频
def replace_audio(video_path, audio_path, output_path):
    """
    使用 ffmpeg 将视频的音频替换为指定音频文件。

    参数:
        video_path (str): 原始视频文件路径
        audio_path (str): 新音频文件路径
        output_path (str): 替换音频后的输出视频文件路径
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"音频替换完成，输出文件：{output_path}")
    except subprocess.CalledProcessError as e:
        print("替换失败：", e)

# 示例用法
#replace_audio(video_path, r"C:\Users\17555\Desktop\final_audio.wav", r"C:\Users\17555\Desktop\output_video.mp4")


# API 路由
@app.post("/process")
def process_video(request: ProcessRequest):
# (video_path:str,speed_factor:float,output_path:str,reference_audio:str,top_k:int,top_p:int):
    try:
        print("1. 正在提取音频...")
        temp_audio = "temp_audio.wav"
        extract_audio_from_video(request.video_path, temp_audio)  # 使用模型字段

        print("2. 正在提取文本...")
        texts = extract_text_from_audio(temp_audio)

        print("3. 正在翻译文本...")
        translated_texts = translate_text(texts)

        print("4. 正在合成语音...")
        audio_segments = text_to_speech(translated_texts,request.speed_factor,request.reference_audio,request.top_k, request.top_p)

        print("5. 正在合并语音...")
        final_audio = "merged_audio.wav"
        merge_audio_files(audio_segments, final_audio)

        print("6. 正在替换视频音频...")
        replace_audio(request.video_path, final_audio, request.output_path)

        return {"message": "处理完成", "output_path": request.output_path}
    except Exception as e:
        import traceback
        traceback.print_exc()  # 打印完整堆栈信息
        return {
            "error": str(e),
            "details": traceback.format_exc(),
            "received_params": request.dict()  # 返回接收到的参数用于调试
        }

# 运行 FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
