import numpy as np
import matplotlib.pyplot as plt
from facade import TransformElastix
from image_operations import ImageStuff

def create_chessboard(shape=200):
    image = np.zeros((shape,shape))
    for i in range(shape):
        if i%10 == 0:
            image[i:i+1,:] = 255
            image[:,i:i+1] = 255
    return image

path1 = r"D:\Daten\Nora\Pre-post\data\crops\crops_21_04\10_1_POST_c1.tif"

if __name__ == '__main__':
    chess = create_chessboard()
    t = TransformElastix()
    t.fixed_image = path1

    s = ImageStuff()
    t.apply_b_spline_transform(chess)
    chess_d = t.t_result_image

    v = t.get_distortion_map()
    s.show_overlay(chess,chess_d[:200,:200], vec_map=v)
    #apply random bspline tranform and register back...
