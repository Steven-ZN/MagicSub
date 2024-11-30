

import openai
import srt
import re
import asyncio
openai.api_key = ""

async def translate_text_async(text, source_language="ja", target_language="zh", max_retries=3):
    """
    使用 OpenAI GPT API 翻译文本（异步版本）
    """
    attempt = 0
    while attempt < max_retries:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"你是一名翻译助手，负责将{source_language}翻译成{target_language}。"},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            attempt += 1
            print(f"翻译失败（尝试 {attempt}/{max_retries} 次）: {e}")
    print("翻译多次失败，返回原文。")
    return text

def translate_text(text, source_language="ja", target_language="zh", max_retries=3):
    """
    同步封装异步翻译函数
    """
    return asyncio.run(translate_text_async(text, source_language, target_language, max_retries))

def merge_subtitles(subtitles, max_gap=2, max_length=500):
    """
    合并短时间间隔的连续字幕段，并限制合并后文本的最大长度
    """
    merged = []
    buffer = []
    current_length = 0

    for subtitle in subtitles:
        subtitle_text_length = len(subtitle.content)
        if (buffer and
            (subtitle.start.total_seconds() - buffer[-1].end.total_seconds() > max_gap or
             current_length + subtitle_text_length > max_length)):
            # 如果间隔超过 max_gap 或合并长度超过 max_length，保存缓冲区内容
            merged.append(buffer)
            buffer = []
            current_length = 0
        buffer.append(subtitle)
        current_length += subtitle_text_length

    if buffer:
        merged.append(buffer)

    return merged

def translate_srt(input_file, output_file):
    """
    翻译 SRT 文件
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            srt_content = f.read()
    except Exception as e:
        print(f"无法读取文件: {e}")
        return

    # 解析 SRT 文件
    subtitles = list(srt.parse(srt_content))

    # 合并字幕段
    merged_subtitles = merge_subtitles(subtitles)

    # 翻译每段字幕
    translated_subtitles = []
    for group in merged_subtitles:
        combined_text = " ".join([re.sub(r'\s+', ' ', sub.content).strip() for sub in group])
        translated_text = translate_text(combined_text)

        # 创建新的字幕段
        for i, sub in enumerate(group):
            start_time = sub.start
            end_time = sub.end
            if i == len(group) - 1:
                end_time = group[-1].end  # 设定为最后一个字幕的结束时间

            translated_subtitles.append(
                srt.Subtitle(index=sub.index, start=start_time, end=end_time, content=translated_text))

    # 转换回 SRT 格式
    translated_srt = srt.compose(translated_subtitles)

    # 保存到文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_srt)
        print(f"翻译完成，已保存到 {output_file}")
    except Exception as e:
        print(f"无法写入文件: {e}")

if __name__ == "__main__":
    input_srt = "C:/Users/akdzb/Desktop/1.srt"  # 替换为你的日文 SRT 文件路径
    output_srt = "C:/Users/akdzb/Desktop/2.srt"  # 翻译后的中文 SRT 文件路径
    translate_srt(input_srt, output_srt)



