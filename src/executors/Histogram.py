"""
    Histogram Executor: Computes pixel intensity histograms for
    selected color channels (R, G, B, Gray) and optionally generates
    a histogram plot image.
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


class Histogram(Component):

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        # DEBUG: Dump request.data to file
        try:
            debug_data = {
                "executor": "Histogram",
                "data_keys": list(self.request.data.keys()) if isinstance(self.request.data, dict) else str(type(self.request.data)),
                "data": self.request.data
            }
            with open("/tmp/histogram_debug.json", "w") as f:
                json.dump(debug_data, f, indent=2, default=str)
        except Exception as e:
            with open("/tmp/histogram_debug.json", "w") as f:
                f.write(f"DEBUG ERROR: {e}")

        self.request.model = PackageModel(**(self.request.data))

        # Input
        self.image = self.request.get_param("inputImage")

        # Configs — channel toggles
        self.channelRed = self.request.get_param("configChannelRed")
        self.channelGreen = self.request.get_param("configChannelGreen")
        self.channelBlue = self.request.get_param("configChannelBlue")
        self.channelGray = self.request.get_param("configChannelGray")

        # Configs — pixel range
        self.pixelMin = int(self.request.get_param("configPixelMin"))
        self.pixelMax = int(self.request.get_param("configPixelMax"))

        # Configs — plot toggle
        self.plotImage = self.request.get_param("configPlotImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def compute_channel_histogram(self, img, channel_index):
        pixel_min = self.pixelMin
        pixel_max = self.pixelMax
        hist_size = pixel_max - pixel_min + 1
        hist = cv2.calcHist(
            [img], [channel_index], None,
            [hist_size], [float(pixel_min), float(pixel_max + 1)]
        )
        return hist.flatten().tolist()

    def compute_gray_histogram(self, img):
        pixel_min = self.pixelMin
        pixel_max = self.pixelMax
        hist_size = pixel_max - pixel_min + 1
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist(
            [gray], [0], None,
            [hist_size], [float(pixel_min), float(pixel_max + 1)]
        )
        return hist.flatten().tolist()

    def generate_plot_image(self, histogram_data):
        width = 640
        height = 480
        pixel_min = self.pixelMin
        pixel_max = self.pixelMax
        channel_colors = {
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0),
            "gray": (180, 180, 180),
        }
        plot_img = np.ones((height, width, 3), dtype=np.uint8) * 255
        margin_left = 50
        margin_bottom = 40
        margin_top = 20
        margin_right = 20
        plot_w = width - margin_left - margin_right
        plot_h = height - margin_top - margin_bottom
        global_max = 0.0
        for hist_values in histogram_data.values():
            if hist_values:
                local_max = max(hist_values)
                if local_max > global_max:
                    global_max = local_max
        if global_max == 0:
            global_max = 1.0
        cv2.line(plot_img, (margin_left, margin_top),
                 (margin_left, height - margin_bottom), (0, 0, 0), 1)
        cv2.line(plot_img, (margin_left, height - margin_bottom),
                 (width - margin_right, height - margin_bottom), (0, 0, 0), 1)
        cv2.putText(plot_img, str(pixel_min),
                    (margin_left, height - margin_bottom + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(plot_img, str(pixel_max),
                    (width - margin_right - 30, height - margin_bottom + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        for channel_name, hist_values in histogram_data.items():
            if not hist_values:
                continue
            color = channel_colors.get(channel_name, (0, 0, 0))
            num_bins = len(hist_values)
            points = []
            for i, val in enumerate(hist_values):
                x = margin_left + int((i / max(num_bins - 1, 1)) * plot_w)
                y = height - margin_bottom - int((val / global_max) * plot_h)
                points.append((x, y))
            if len(points) >= 2:
                pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(plot_img, [pts], False, color, 1, cv2.LINE_AA)
        legend_x = margin_left + 10
        legend_y = margin_top + 15
        for channel_name in histogram_data:
            color = channel_colors.get(channel_name, (0, 0, 0))
            cv2.rectangle(plot_img, (legend_x, legend_y - 8),
                          (legend_x + 12, legend_y + 2), color, -1)
            cv2.putText(plot_img, channel_name.capitalize(),
                        (legend_x + 18, legend_y + 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            legend_y += 18
        return plot_img

    def process(self, img):
        if img is None:
            return None, {}
        pixel_min = self.pixelMin
        pixel_max = self.pixelMax
        if pixel_min >= pixel_max:
            pixel_min, pixel_max = pixel_max, pixel_min
            self.pixelMin = pixel_min
            self.pixelMax = pixel_max
        histogram_data = {}
        if self.channelRed == "Enabled":
            histogram_data["red"] = self.compute_channel_histogram(img, 2)
        if self.channelGreen == "Enabled":
            histogram_data["green"] = self.compute_channel_histogram(img, 1)
        if self.channelBlue == "Enabled":
            histogram_data["blue"] = self.compute_channel_histogram(img, 0)
        if self.channelGray == "Enabled":
            histogram_data["gray"] = self.compute_gray_histogram(img)
        if self.plotImage == "Enabled" and histogram_data:
            output_img = self.generate_plot_image(histogram_data)
        else:
            output_img = img
        return output_img, histogram_data

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        processed_img, histogram_data = self.process(img.value)
        img.value = processed_img
        self.histogramData = histogram_data
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
