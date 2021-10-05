from image_operations import ImageStuff
from facade import TransformElastix
import os
import numpy as np


EXPECTED_EXPASION = 3.5
root = r"D:\Daten\Nora\Pre-post\data\test"+"\\"
path1 = r"1_1_POST.tif"
path2 = r"1_1.tif"
save_dir = root + r"\results"+"\\"
save_name = path2.split(".")[0]

if __name__ == '__main__':
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    image_op = ImageStuff()
    transform = TransformElastix()
    transform.fixed_image = root+path1
    resized = image_op.resize_image(root+path2, EXPECTED_EXPASION)
    transform.moving_image = resized
    #run similarity transform
    transform.similarity_transform()
    similarity_image = transform.result_image
    TP = transform.STP
    image_op.show_overlay(transform.fixed_image, similarity_image, scale=EXPECTED_EXPASION, TP=TP, save_path=save_dir+save_name+"similarity")
    print(np.corrcoef(transform.fixed_image.flatten(),similarity_image.flatten()))
    #run spline transform
    transform.moving_image = similarity_image
    transform.b_spline_tranform()
    b_spline_image = transform.result_image
    image_op.show_overlay(transform.fixed_image, b_spline_image, scale=EXPECTED_EXPASION, save_path=save_dir+save_name+"spline")


    image_op.show_overlay(transform.fixed_image, similarity_image,
                          scale=EXPECTED_EXPASION, vec_map=transform.get_distortion_map(), TP=TP, save_path=save_dir+save_name+"distortion")
