import json
class HTMLdb:
	def __init__(self):
		self.dates = None
		self.filename = "htmldb.json"
		self.db = { }

	def load(self):
		try:
			jsonFile = open(self.filename, 'rt')
			self.db = json.loads(jsonFile.read())
			jsonFile.close()
		except Exception as e:
			print(e)
			print("Unable to load", self.filename)

	def dump(self):
		jsonFile = open(self.filename, 'wt')
		json.dump(self.db, jsonFile, indent=4)
		jsonFile.close()

	def set(self, property, value):
		self.db[property] = value
		self.dump()

