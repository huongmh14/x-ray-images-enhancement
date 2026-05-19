from dataclasses import dataclass
from pathlib import Path
import timeit

import cv2
import imageio.v2 as imageio
import numpy as np

from .base import BaseAlgorithm


@dataclass(slots=True)
class EnhancementConfig:
	log_gain: float = 4.0
	clip_limit: float = 2.5
	tile_grid_size: int = 8
	sharpen_amount: float = 0.6


class MedicalEnhancement(BaseAlgorithm):
	'''Pipeline: log transform -> CLAHE -> unsharp masking.'''

	def __init__(self, filename, results_path, config=None, prompt_for_missing=True):
		self.filename = filename
		self.results_path = results_path
		self.config = self.resolve_config(config, prompt_for_missing=prompt_for_missing)

	def get_input(self):
		self.config = self.resolve_config(None, prompt_for_missing=True)
		return self.config

	def run(self):
		image = imageio.imread(self.filename)
		return self.run_on_image(image, export_outputs=True)

	def run_on_image(self, image, export_outputs=False):
		original = self.normalize_to_uint8(image)
		start = timeit.default_timer()
		log_image = self.apply_log_transform(original, self.config.log_gain)
		clahe_image = self.apply_clahe(log_image, self.config.clip_limit, self.config.tile_grid_size)
		enhanced_image = self.apply_unsharp_mask(clahe_image, self.config.sharpen_amount)
		stop = timeit.default_timer()

		if export_outputs:
			self.export_stages(original, log_image, clahe_image, enhanced_image)
			self.export_run_info(stop - start)

		return {
			"original": original,
			"log": log_image,
			"clahe": clahe_image,
			"enhanced": enhanced_image,
			"runtime": stop - start,
		}

	def get_processed_image(self, image):
		return self.run_on_image(image)["enhanced"]

	def normalize_to_uint8(self, image):
		array = np.asarray(image)

		if array.ndim == 3:
			array = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)

		if array.dtype == np.uint8:
			return array

		array = array.astype(np.float32)
		min_value = float(array.min())
		max_value = float(array.max())
		if max_value <= min_value:
			return np.zeros_like(array, dtype=np.uint8)

		normalized = (array - min_value) / (max_value - min_value)
		return np.clip(normalized * 255.0, 0, 255).astype(np.uint8)

	def apply_log_transform(self, image, gain):
		normalized = image.astype(np.float32) / 255.0
		transformed = np.log1p(gain * normalized) / np.log1p(gain)
		return np.clip(transformed * 255.0, 0, 255).astype(np.uint8)

	def apply_clahe(self, image, clip_limit, tile_grid_size):
		clahe = cv2.createCLAHE(
			clipLimit=float(clip_limit),
			tileGridSize=(int(tile_grid_size), int(tile_grid_size)),
		)
		return clahe.apply(image)

	def apply_unsharp_mask(self, image, amount):
		if amount <= 0:
			return image.copy()

		blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=1.1)
		sharpened = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)
		return np.clip(sharpened, 0, 255).astype(np.uint8)

	def export_stages(self, original, log_image, clahe_image, enhanced_image):
		stem = Path(self.filename).stem
		imageio.imwrite(Path(self.results_path) / f"{stem}_original.png", original)
		imageio.imwrite(Path(self.results_path) / f"{stem}_log.png", log_image)
		imageio.imwrite(Path(self.results_path) / f"{stem}_clahe.png", clahe_image)
		imageio.imwrite(Path(self.results_path) / f"{stem}_enhanced.png", enhanced_image)

	def export_run_info(self, runtime):
		stem = Path(self.filename).stem
		with open(Path(self.results_path) / f"{stem}_runinfo.txt", "w", encoding="utf-8") as handle:
			handle.write(f"Pipeline: log transform -> CLAHE -> unsharp masking\n")
			handle.write(f"Runtime: {runtime:.4f}s\n")
			handle.write(f"Log gain c: {self.config.log_gain}\n")
			handle.write(f"CLAHE clip limit: {self.config.clip_limit}\n")
			handle.write(f"CLAHE tile grid size: {self.config.tile_grid_size}\n")
			handle.write(f"Unsharp amount: {self.config.sharpen_amount}\n")

	@classmethod
	def resolve_config(cls, config, prompt_for_missing):
		if config is None:
			config = EnhancementConfig()
		elif isinstance(config, dict):
			config = EnhancementConfig(**config)

		if prompt_for_missing:
			config.log_gain = cls._prompt_float_if_missing(
				"Log gain c", config.log_gain, default=4.0, min_value=0.01
			)
			config.clip_limit = cls._prompt_float_if_missing(
				"CLAHE clip limit", config.clip_limit, default=2.5, min_value=0.01
			)
			config.tile_grid_size = cls._prompt_int_if_missing(
				"CLAHE tile grid size", config.tile_grid_size, default=8, min_value=2
			)
			config.sharpen_amount = cls._prompt_float_if_missing(
				"Unsharp amount", config.sharpen_amount, default=0.6, min_value=0.0
			)

		cls._validate_config(config)
		return config

	@staticmethod
	def _validate_config(config):
		if config.log_gain <= 0:
			raise ValueError("log_gain must be > 0.")
		if config.clip_limit <= 0:
			raise ValueError("clip_limit must be > 0.")
		if config.tile_grid_size < 2:
			raise ValueError("tile_grid_size must be >= 2.")
		if config.sharpen_amount < 0:
			raise ValueError("sharpen_amount must be >= 0.")

	@classmethod
	def _prompt_float_if_missing(cls, label, current_value, default, min_value):
		if current_value is not None:
			return float(current_value)
		return cls._prompt_float(label, default, min_value)

	@classmethod
	def _prompt_int_if_missing(cls, label, current_value, default, min_value):
		if current_value is not None:
			return int(current_value)
		return cls._prompt_int(label, default, min_value)

	@staticmethod
	def _prompt_float(label, default, min_value):
		while True:
			print(f"{label} [{default}]: ")
			raw = input().strip()
			if raw == "":
				return default

			try:
				value = float(raw)
			except ValueError:
				print("Please enter a valid number.")
				continue

			if value < min_value:
				print(f"Value must be >= {min_value}.")
				continue

			return value

	@staticmethod
	def _prompt_int(label, default, min_value):
		while True:
			print(f"{label} [{default}]: ")
			raw = input().strip()
			if raw == "":
				return default

			try:
				value = int(raw)
			except ValueError:
				print("Please enter a valid integer.")
				continue

			if value < min_value:
				print(f"Value must be >= {min_value}.")
				continue

			return value
