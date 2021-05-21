import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import resize
from skimage import io
import os

class ImageStuff():
    ORANGE = (0.9, .4, .11, 0.5)
    #ORANGE = (1,1,1,1)
    CYAN = (.0, 1.0, 1.0, 1.0)
    BLUE = (0,0,1.0,1.0)
    YELLOW = (0,1.0,1.0,1.0)
    GREY = (0.8,0.8,.8,1.0)

    def resize_image(self, path, scale):
        image = io.imread(path)
        output_dimension = (int(image.shape[0] * scale), int(image.shape[1] * scale))
        image = resize(image, output_dimension, preserve_range=True)
        io.imsave("tmp/resized.tif", image.astype("uint16"))
        return image

    def image_to_rgba_color(self, image, color, multiplier=1):
        res_rgba = np.zeros((image.shape[0], image.shape[1], 4))
        res_rgba[:, :, 0] = (image / image.max()) * color[0]
        res_rgba[:, :, 1] = (image / image.max()) * color[1]
        res_rgba[:, :, 2] = (image / image.max()) * color[2]
        res_rgba[:, :, 3] = (image / image.max()) * color[3]
        res_rgba = np.clip(multiplier * res_rgba, 0, 1.0)
        return res_rgba

    def show_overlay(self, im1, im2, scale=1, TP=None, vec_map=None):
        im_rgba = self.image_to_rgba_color(im1, self.ORANGE, multiplier=3)
        res_rgba = self.image_to_rgba_color(im2, self.CYAN , multiplier=3)

        plt.imshow(np.zeros_like(im1)*255)
        plt.imshow(res_rgba)
        plt.imshow(im_rgba)
        if TP:
            plt.title(f"Expansion = {scale/float(TP['TransformParameters'][0]):.2f}")
        if vec_map:
            plt.quiver(vec_map.XY, vec_map.YX, -vec_map.XY_final,vec_map.YX_final,
                       color="red", scale_units='xy',scale=1)
        plt.show()