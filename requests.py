import requests

# API endpoint 
url = "https://googleapis.com" 

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
user_prompt = input("Ask Buddy a question;")
data = {
    "model": "example-model-1",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

response = requests.post(url, headers=headers, json=data,timeout=10)  # Added a timeout of 10 seconds
return response

if response.status_code == 200:
    result = response.json()
    print("\nAI Response:", result["choices"][0]["message"]["content"])
else:
    print("Error:", response.status_code, response.text)
