import os, json, subprocess
unique_headings = ["6.1. Satzteil", "6.2. Verbstamm", "6.3. Indikativ Präsens (laṭ)"]
target_lang = "Tamil"

system_prompt = f"You are a translation API. Translate these technical German Sanskrit grammar headings into {target_lang}. Return ONLY a valid JSON object mapping the exact German string to the {target_lang} string. Do not use romanization or IAST for the translation, use the native script. Be extremely accurate."
user_content = "Translate these exact keys:\n" + json.dumps(unique_headings, ensure_ascii=False)

data = {
    "model": "google/gemini-2.5-pro",
    "response_format": {"type": "json_object"},
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ],
    "temperature": 0.1
}

curl_cmd = ['curl', '-s', '-X', 'POST', 'https://openrouter.ai/api/v1/chat/completions', 
            '-H', 'Content-Type: application/json',
            '-H', f"Authorization: Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
            '-d', json.dumps(data), '--max-time', '60']
            
proc = subprocess.run(curl_cmd, capture_output=True, text=True)
print(proc.stdout)
