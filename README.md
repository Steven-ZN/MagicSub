# MagicSub
AI-Powered Subtitle Translator
# Subtitle Translator with OpenAI GPT

This script provides a simple tool for translating SRT subtitle files using the OpenAI GPT-3.5-turbo API. It supports merging short subtitle segments, ensuring translations are coherent, and processing subtitles efficiently with retry logic for API failures.

---

## Features

- **Text Translation**: Translates text from one language to another using OpenAI's GPT API.
- **Subtitle Merging**: Merges subtitles with short time gaps or excessive length to ensure cohesive translation.
- **Error Handling**: Implements retry logic for API errors, falling back to the original text after multiple failures.
- **SRT Processing**: Reads and parses SRT subtitle files, translates their content, and outputs the translated subtitles to a new file.

---

## Requirements

- Python 3.7+
- OpenAI API Key
- Installed Python packages:
  - `openai`
  - `srt`
  - `asyncio`
  - `re`

Install dependencies using pip:

```bash
pip install openai srt
```

---

## Usage

### 1. Setup

1. Add your OpenAI API key in the script:
   ```python
   openai.api_key = "your_openai_api_key"
   ```

2. Update the paths to your input and output SRT files:
   ```python
   input_srt = "path/to/your/input.srt"
   output_srt = "path/to/your/output.srt"
   ```

### 2. Run the Script

Run the script in your terminal:

```bash
python script_name.py
```

### 3. Output

The translated SRT file will be saved to the specified output path.

---

## Code Overview

### 1. Translation Functionality

The `translate_text_async` function uses OpenAI's GPT API to translate text asynchronously. The `translate_text` function wraps it for synchronous use.

- **Parameters**:
  - `text`: The text to translate.
  - `source_language`: The source language (default: Japanese `"ja"`).
  - `target_language`: The target language (default: Chinese `"zh"`).
  - `max_retries`: Number of retries for failed API calls (default: 3).

### 2. Subtitle Merging

The `merge_subtitles` function combines consecutive subtitles with short gaps (`max_gap`) or excessive combined length (`max_length`) to ensure better translation.

- **Parameters**:
  - `max_gap`: Maximum gap in seconds to merge subtitles (default: 2).
  - `max_length`: Maximum character length for combined subtitles (default: 500).

### 3. SRT Translation

The `translate_srt` function reads the input SRT file, merges and translates subtitles, and writes the result to an output SRT file.

- **Parameters**:
  - `input_file`: Path to the input SRT file.
  - `output_file`: Path to save the translated SRT file.

---

## Example

Input Subtitle (Japanese):

```srt
1
00:00:01,000 --> 00:00:04,000
こんにちは、世界！

2
00:00:05,000 --> 00:00:07,000
これはサンプル字幕です。
```

Output Subtitle (Chinese):

```srt
1
00:00:01,000 --> 00:00:07,000
你好，世界！这是一个示例字幕。
```

---

## Error Handling

1. **API Failures**: The script retries API calls up to 3 times. If all retries fail, the original text is returned.
2. **File I/O Errors**: Handles errors in reading/writing files gracefully.

---

## Notes

- The OpenAI GPT API may incur usage costs. Ensure your API key has an active quota.
- The script is optimized for translating SRT files with simple text. Complex formatting or edge cases may require adjustments.

---

Feel free to clone and modify this repository for your subtitle translation needs! 😊
