import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "mistral",
    "prompt": "Say hello from Ollama!"
}

# stream=True means we’ll read JSONL chunks line by line
response = requests.post(url, json=payload, stream=True)

output = ""
for line in response.iter_lines():
    if line:  # skip empty lines
        data = json.loads(line.decode("utf-8"))
        if "response" in data:
            output += data["response"]

print("Ollama replied:", output)
