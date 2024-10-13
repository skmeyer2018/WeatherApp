from meta_ai_api import MetaAI
class getInfo:
	def __init__(self, inquiry, response):
		self.inquiry=inquiry
		self.response=response

	ai = MetaAI()

	def get_response(self, request_prompt):
		resp = self.ai.prompt(message=request_prompt)
		self.response=resp["message"]




