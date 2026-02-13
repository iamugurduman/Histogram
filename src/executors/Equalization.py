"""
    Equalization Executor: Applies CLAHE (Contrast Limited Adaptive
    Histogram Equalization) to enhance local contrast of input images.
"""
import os
import cv2
import sys
import json
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.HistogramUpdate.src.utils.response import build_response
from components.HistogramUpdate.src.models.PackageModel import PackageModel


class Equalization(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        # DEBUG: Dump request.data to file
        try:
            debug_data = {
                "executor": "Equalization",
                "data_keys": list(self.request.data.keys()) if isinstance(self.request.data, dict) else str(type(self.request.data)),
                "data": self.request.data
            }
            with open("/tmp/equalization_debug.json", "w") as f:
                json.dump(debug_data, f, indent=2, default=str)
        except Exception as e:
            with open("/tmp/equalization_debug.json", "w") as f:
                f.write(f"DEBUG ERROR: {e}")

        self.request.model = PackageModel(**(self.request.data))

        # Input
        self.image = self.request.get_param("inputImage")

        # Configs
        try:
            self.clipLimit = float(self.request.get_param("configClipLimit"))
        except (TypeError, ValueError):
            self.clipLimit = 2.0

        self.tileGridSize = self.request.get_param("configTileGridSize")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def parse_tile_grid_size(self):
        grid_str = self.tileGridSize
        if grid_str is None:
            return 8
        if isinstance(grid_str, (int, float)):
            return int(grid_str)
        try:
            return int(str(grid_str).split("x")[0])
        except (ValueError, IndexError):
            return 8

    def apply_clahe(self, img):
        if img is None:
            return None
        if img.dtype != np.uint8:
            if img.max() <= 1.0:
                img = (img * 255).astype(np.uint8)
            else:
                img = np.clip(img, 0, 255).astype(np.uint8)
        grid_size = self.parse_tile_grid_size()
        clip_limit = self.clipLimit
        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=(grid_size, grid_size)
        )
        if len(img.shape) == 2:
            return clahe.apply(img)
        elif len(img.shape) == 3 and img.shape[2] == 3:
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            l_enhanced = clahe.apply(l_channel)
            lab_enhanced = cv2.merge([l_enhanced, a_channel, b_channel])
            return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
        elif len(img.shape) == 3 and img.shape[2] == 4:
            bgr = img[:, :, :3]
            alpha = img[:, :, 3]
            lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            l_enhanced = clahe.apply(l_channel)
            lab_enhanced = cv2.merge([l_enhanced, a_channel, b_channel])
            bgr_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
            return cv2.merge([
                bgr_enhanced[:, :, 0],
                bgr_enhanced[:, :, 1],
                bgr_enhanced[:, :, 2],
                alpha
            ])
        else:
            return img

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.apply_clahe(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
