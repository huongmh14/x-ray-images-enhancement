import os
import imageio.v2 as imageio

from datetime import datetime

import src.arguments as ah

from src.algorithms.medical_pipeline import EnhancementConfig, MedicalEnhancement

class AlgorithmRunner:
	def __init__(self):
		self.arg_handler	= ah.ArgumentHandler()
		self.algorithm		= self.arg_handler.get_algorithm()
		self.image				= self.arg_handler.get_image()
		self.images_path	= self.arg_handler.get_path()
		self.parameter_overrides = self.arg_handler.get_parameter_overrides()
		output_path = self.arg_handler.get_output_path()
		if output_path:
			self.results_path = output_path
		else:
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			self.results_path	= os.path.join("results", timestamp)

		os.makedirs(self.results_path, exist_ok=True)

	def __del__(self):
		self.algorithm		= ''
		self.image				= ''
		self.images_path	= ''
		self.results_path	= ''

	def run(self):
		'''Runs the algorithm in the images.'''

		if self.images_path:
			images = sorted(
				image for image in os.listdir(self.images_path)
				if os.path.isfile(os.path.join(self.images_path, image))
			)
			path = self.images_path
		else:
			# We put in a list to be able to utilize the for loop
			images = [self.image]
			path = ""

		config = self.__resolve_config()

		for image in images:
			self.image = os.path.basename(image)

			processed_image = self.__run_algorithm(image, path, config)
			if processed_image is None:
				continue

			t = datetime.now()
			name = self.image.split(".")[0]
			filename = f"{t.hour}_{t.minute}_{t.second}_{name}_enhanced.png"
			imageio.imwrite(os.path.join(self.results_path, filename), processed_image)

	def __resolve_config(self):
		config = EnhancementConfig(**self.parameter_overrides)
		return MedicalEnhancement.resolve_config(config, prompt_for_missing=True)

	def __run_algorithm(self, image, path, config):
		'''Runs the algorithm in the image.

		Parameters:
			image: image filename.
			path: image directory.

		Returns the processed image.
		'''

		img = os.path.join(path, image)
		alg = MedicalEnhancement(
			img,
			self.results_path,
			config=config,
			prompt_for_missing=False,
		)

		try:
			result = alg.run()
		except Exception as e:
			print(e)
		else:
			return result["enhanced"]
