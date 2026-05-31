import tkinter as tk
from tkinter import filedialog, messagebox
from gradio_client import Client, file
import os
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

# Gradio 服务器地址
SERVER_URL = "http://localhost:9872/"
client = Client(SERVER_URL)


def select_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, file_path)


def synthesize_speech():
    ref_wav = audio_entry.get()
    text = text_entry.get("1.0", tk.END).strip()
    if not ref_wav or not text:
        messagebox.showwarning("警告", "请提供音频样本和文本！")
        return

    try:
        result = client.predict(
            ref_wav_path=file(ref_wav),
            prompt_text="",  # 参考文本可留空
            prompt_language="中文",
            text=text,
            text_language="中文",
            how_to_cut="凑四句一切",
            top_k=15,
            top_p=1,
            temperature=1,
            ref_free=False,
            speed=1,
            if_freeze=False,
            inp_refs=None,
            api_name="/get_tts_wav"
        )
        messagebox.showinfo("成功", "语音合成完成！")
    except Exception as e:
        messagebox.showerror("错误", str(e))


# 创建主窗口
root = tk.Tk()
root.title("TTS 语音合成")
root.geometry("500x400")

tk.Label(root, text="参考音频:").pack()
audio_frame = tk.Frame(root)
audio_frame.pack()
audio_entry = tk.Entry(audio_frame, width=50)
audio_entry.pack(side=tk.LEFT)
audio_button = tk.Button(audio_frame, text="选择文件", command=select_audio_file)
audio_button.pack(side=tk.RIGHT)

tk.Label(root, text="需要合成的文本:").pack()
text_entry = tk.Text(root, height=5)
text_entry.pack()

synthesize_button = tk.Button(root, text="合成语音", command=synthesize_speech)
synthesize_button.pack()

root.mainloop()
