import requests

url = "https://openai80.p.rapidapi.com/chat/completions"

payload = {
	"model": "gpt-3.5-turbo",
	"messages": [
		{
			"role": "user",
			"content": input()
		}
	]
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "d9050d5653msh75d645c395b0db8p19a102jsn44253b504e66",
	"X-RapidAPI-Host": "openai80.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()

content = data["choices"][0]["message"]["content"]

print(content)