from fastapi import FastAPI, HTTPException, Response, Body
from pydantic import BaseModel
from openai import OpenAI
import httpx
from fastapi.middleware.cors import CORSMiddleware
import os
import base64
import tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# DeepSeek配置（保持不变）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-8ffd0d01a56e4ec0a26593c495dd5a0f")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 情感映射（保持不变）
EMOTION_MAP = {
    "1": "高兴",
    "2": "悲伤",
    "3": "愤怒",
    "4": "平静",
    "5": "惊讶",
    "6": "恐惧",
    "7": "喜好",
    "8": "厌恶",
    "9": "疑惑",
    "10": "期待",
    "11": "自信",
    "12": "担忧",
    "13": "怀念",
    "14": "激动",
    "15": "羞涩"
}

# 定义请求体模型
class TextToSpeechRequest(BaseModel):
    text: str
    ref_audio: str  # Base64编码的音频字符串
    speed_factor: float
    emotion: str

@app.post("/text_to_speech")
async def text_to_speech(request: TextToSpeechRequest = Body(...)):
    # 1. 验证情感值
    if request.emotion not in EMOTION_MAP:
        raise HTTPException(status_code=400, detail="无效的 emotion 值")
    emotion_label = EMOTION_MAP[request.emotion]

    # 3. 调用DeepSeek生成文本（保持不变）
    system_prompt = f"请你根据情感{emotion_label}对以下文字增加语气词，我有以下要求1.只出现中文，不出现任何动作以及符号2.不需要扩充这句话，只需要简单的语气词‘嘿嘿’、‘哎’等。"
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.text}
        ],
        stream=False
    )
    generated_text = response.choices[0].message.content

    # 4. 调用TTS服务（保持不变）
    tts_request = {
        "text": generated_text,
        "text_lang": "auto",
        "ref_audio_path": request.ref_audio,
        "prompt_text": "",
        "prompt_lang": "auto",
        "top_k": 5,
        "top_p": 1,
        "temperature": 1,
        "text_split_method": "cut0",
        "batch_size": 1,
        "batch_threshold": 0.75,
        "split_bucket": True,
        "speed_factor": request.speed_factor,
        "fragment_interval": 0.3,
        "seed": -1,
        "media_type": "wav"
    }

    async with httpx.AsyncClient() as client:
        tts_response = await client.post(
            "http://127.0.0.1:9880/tts",
            json=tts_request,
            timeout=60.0
        )

    # 5. 返回响应（保持不变）
    encoded_text = base64.b64encode(generated_text.encode('utf-8')).decode('ascii')
    return Response(
        content=tts_response.content,
        media_type="audio/wav",
        headers={
            "Generated-Text": encoded_text,
            "X-Content-Length": str(len(tts_response.content))
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
