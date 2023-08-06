import requests

url = "https://text-translator2.p.rapidapi.com/translate"

payload = {
	"source_language": input(),
	"target_language": input(),
	"text": input()
}
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": "d9050d5653msh75d645c395b0db8p19a102jsn44253b504e66",
	"X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())