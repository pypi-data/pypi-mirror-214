import requests, json

class Chat:
	def GPT(text):
		headers = {
			"Host": "us-central1-chat-for-chatgpt.cloudfunctions.net",
			"Connection": "keep-alive",
			"If-None-Match": 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
			"Accept": "*/*",
			"User-Agent": "com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2",
			"Content-Type": "application/json",
			"Accept-Language": "en-GB,en;q=0.9"}
		data = {
			"data": {
				"message": str(text),
			}
		}
		response = requests.post("https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta", headers=headers, data=json.dumps(data)).json()
		try:
			result = response["result"]["choices"][0]["text"]
			return result
		except:
			return None