#!/usr/bin/env python3
"""
Speechify TTS 命令行工具
支持将文本转换为语音并保存到本地文件

# 转换文本
python speechify_tts.py -t "Hello, world!"

# 从文件读取
python speechify_tts.py -f input.txt

# 指定语音和语言
python speechify_tts.py -t "你好世界" -v "zh-cn-female" -l "zh-CN" -m "simba-multilingual"

# 列出可用语音
python speechify_tts.py --list-voices

# 命令行参数

| 参数            | 简写 | 描述                       | 默认值                        |
|-----------------|-------|----------------------------|-------------------------------|
| `--api-key`     | `-k`  | Speechify API 密钥         | 环境变量 `SPEECHIFY_API_KEY` |
| `--text`        | `-t`  | 要转换的文本内容           | -                             |
| `--file`        | `-f`  | 包含文本的文件路径         | -                             |
| `--voice`       | `-v`  | 语音 ID                   | `cliff`                      |
| `--language`    | `-l`  | 语言代码 (如 `en-US`, `zh-CN`) | `en-US`                     |
| `--model`       | `-m`  | TTS 模型                  | `simba-english`              |
| `--output-dir`  | `-o`  | 输出目录                   | `./`                         |
| `--prefix`      | `-p`  | 文件名前缀                 | `tts_audio`                  |
| `--list-voices` | -     | 列出可用语音               | -                             |

# 支持的模型

- **simba-english**: 专为英语优化的模型
- **simba-multilingual**: 支持多语言的模型

# 输出文件格式

生成的音频文件将以 MP3 格式保存，文件名格式为：

{prefix}_{YYYYMMDD_HHMMSS}.mp3


例如：`tts_audio_20250730_143022.mp3`
"""


import argparse
import base64
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import requests


class SpeechifyTTS:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.sws.speechify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_voices(self):
        """获取可用的语音列表"""
        try:
            response = requests.get(f"{self.base_url}/voices", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取语音列表失败: {e}")
            return None
    
    def text_to_speech(self, text, voice_id="cliff", language="en-US", model="simba-english"):
        """将文本转换为语音"""
        payload = {
            "input": text,
            "voice_id": voice_id,
            "language": language,
            "model": model
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/audio/speech",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"TTS 请求失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"错误详情: {e.response.text}")
            return None
    
    def save_audio(self, audio_data, output_dir="./", prefix="tts_audio"):
        """保存音频文件到本地"""
        # 生成包含当前时间的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.mp3"
        filepath = Path(output_dir) / filename
        
        # 确保输出目录存在
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # 解码 Base64 音频数据
            audio_bytes = base64.b64decode(audio_data)
            
            # 写入文件
            with open(filepath, 'wb') as f:
                f.write(audio_bytes)
            
            print(f"音频文件已保存: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"保存音频文件失败: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Speechify TTS 命令行工具 - 将文本转换为语音",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s -t "Hello, world!" -k YOUR_API_KEY
  %(prog)s -t "你好，世界！" -k YOUR_API_KEY -v "zh-cn-female" -l "zh-CN"
  %(prog)s -f input.txt -k YOUR_API_KEY -o ./outputs/
  %(prog)s --list-voices -k YOUR_API_KEY
        """
    )
    
    # 基本参数
    parser.add_argument('-k', '--api-key', 
                       help='Speechify API密钥 (也可通过环境变量 SPEECHIFY_API_KEY 设置)')
    parser.add_argument('-t', '--text', 
                       help='要转换的文本内容')
    parser.add_argument('-f', '--file', 
                       help='包含文本内容的文件路径')
    
    # 语音参数
    parser.add_argument('-v', '--voice', default='cliff',
                       help='语音ID (默认: cliff)')
    parser.add_argument('-l', '--language', default='en-US',
                       help='语言代码 (默认: en-US)')
    parser.add_argument('-m', '--model', default='simba-english',
                       choices=['simba-english', 'simba-multilingual'],
                       help='TTS模型 (默认: simba-english)')
    
    # 输出参数
    parser.add_argument('-o', '--output-dir', default='./',
                       help='输出目录 (默认: 当前目录)')
    parser.add_argument('-p', '--prefix', default='tts_audio',
                       help='输出文件名前缀 (默认: tts_audio)')
    
    # 其他功能
    parser.add_argument('--list-voices', action='store_true',
                       help='列出可用的语音')
    
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = args.api_key or os.getenv('SPEECHIFY_API_KEY')
    if not api_key:
        print("错误: 请提供API密钥 (-k) 或设置环境变量 SPEECHIFY_API_KEY")
        sys.exit(1)
    
    # 初始化TTS客户端
    tts = SpeechifyTTS(api_key)
    
    # 列出语音
    if args.list_voices:
        print("正在获取可用语音列表...")
        voices = tts.get_voices()
        if voices:
            print("\n可用语音:")
            for voice in voices:
                print(f"  - ID: {voice.get('id', 'N/A')}")
                print(f"    名称: {voice.get('name', 'N/A')}")
                print(f"    语言: {voice.get('language', 'N/A')}")
                print(f"    性别: {voice.get('gender', 'N/A')}")
                print()
        return
    
    # 获取文本内容
    text_content = None
    if args.text:
        text_content = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text_content = f.read().strip()
        except Exception as e:
            print(f"读取文件失败: {e}")
            sys.exit(1)
    else:
        print("错误: 请提供文本内容 (-t) 或文本文件 (-f)")
        sys.exit(1)
    
    if not text_content:
        print("错误: 文本内容为空")
        sys.exit(1)
    
    # 检查文本长度
    if len(text_content) > 5000:
        print(f"警告: 文本长度 ({len(text_content)}) 超过建议的5000字符限制")
        confirm = input("是否继续? (y/N): ")
        if confirm.lower() != 'y':
            sys.exit(0)
    
    print(f"正在转换文本到语音...")
    print(f"文本长度: {len(text_content)} 字符")
    print(f"语音: {args.voice}")
    print(f"语言: {args.language}")
    print(f"模型: {args.model}")
    
    # 调用TTS API
    result = tts.text_to_speech(
        text=text_content,
        voice_id=args.voice,
        language=args.language,
        model=args.model
    )
    
    if not result:
        print("TTS转换失败")
        sys.exit(1)
    
    # 提取音频数据
    audio_data = result.get('audio_data') or result.get('audioData') or result.get('data')
    if not audio_data:
        print("响应中未找到音频数据")
        print(f"响应内容: {result}")
        sys.exit(1)
    
    # 保存音频文件
    filepath = tts.save_audio(
        audio_data=audio_data,
        output_dir=args.output_dir,
        prefix=args.prefix
    )
    
    if filepath:
        file_size = os.path.getsize(filepath)
        print(f"转换完成!")
        print(f"文件大小: {file_size / 1024:.1f} KB")
    else:
        print("保存文件失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
