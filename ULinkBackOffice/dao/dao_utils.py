from os import stat
from django.utils import timezone
import random
import string

		

class dao_utils(object):
	@staticmethod
	def generateUploadNumber():
		uid = ''.join(random.choices(string.digits, k=10))
		uid = 'File'+""+uid
		return uid
	
	@staticmethod
	def generatePaperNumber():
		uid = ''.join(random.choices(string.digits, k=10))
		uid = 'PAPER-'+""+uid
		return uid
	
	@staticmethod
	def processingLines(lineStr):
		'''Converting the string serialize with ',' and '|', to a list of key value'''
		try:
			liste = []
			lines = lineStr.split("|")
			for elt in lines:
				line = elt.split(",")
				liste.append({
					'brand': line[0],
					'model': line[1],
					'year': line[2],
					'carId': line[3],
					'plateId': line[4]
				})
			return liste

		except Exception as e:
			print("Error on processingLines", e)
			return []
	

	@staticmethod
	def convertDataPost(**kwargs):
		return kwargs
