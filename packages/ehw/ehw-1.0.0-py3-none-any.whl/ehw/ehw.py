import requests
import logging
import platform

######## START CONTENT ########

class EHW:

	@staticmethod
	def GetHWId():
		response = requests.get('https://eons.sh/hw/id', params={
			'os': platform.system(),
			'machine': platform.machine(),
			'arch': platform.architecture()[0],
			'processor': platform.processor(),
			'version': platform.version(),
			'hostname': platform.node()
		})
		return response.text
		

	#Called when executing this as a functor.
	def __call__(this):
		print(EHW.GetHWId())
