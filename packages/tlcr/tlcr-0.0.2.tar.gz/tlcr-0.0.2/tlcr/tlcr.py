from tlcr.tlcr.Video import Video
from tlcr.tlcr.Lane import Lane
from tlcr.tlcr.ImageNet import ImageNet
from skimage.util import img_as_float
import numpy as np


class Tlcr:
    intensity_k = 0.155

    @staticmethod
    def get_params(url, weights, coords):
        images = []
        Video.fill_images(url, images)
        line = Lane(coords)
        images = images[::5]
        size = len(images)
        x = np.zeros((size, ImageNet.size_img, ImageNet.size_img, 3), dtype='float32')
        for i in range(0, len(images)):
            x[i] = np.array(img_as_float(line.get_image(images[i])))
        image_net = ImageNet()
        image_net.init()
        image_net.load_weights(weights)
        predictions = image_net.predict(x)
        size_predictions = len(predictions)
        tlcr_arr = []
        vehicles = 0
        wait_next_vehicle = True
        for i in range(0, size_predictions):
            local_tlcr = line.get_tlcr(predictions[i])
            if local_tlcr > Tlcr.intensity_k and wait_next_vehicle:
                vehicles += 1
            wait_next_vehicle = local_tlcr < Tlcr.intensity_k
            tlcr_arr.append(local_tlcr)
        # tlcr = tlcr / size_predictions
        return tlcr_arr, vehicles
