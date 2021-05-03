import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import SimilarityTransform,warp, resize
from skimage import io
from tifffile.tifffile import TiffFile
import subprocess
import os
import SimpleITK as sitk

print(sitk.Elastix)
from PIL import Image
#with TiffFile(r"D:\Daten\Nora\Pre-post\post_cyan.tif") as tif:
#    image = tif.asarray()

SPACING = 20
EXPECTED_EXPASION = 4

#specify directories
path1 = r"D:\Daten\Nora\Pre-post\new_data\C2-MAX_NK_Af_preExp_atubulin_mitoRFP_snap_1_stack_5_POST.tif"
path2 = r"D:\Daten\Nora\Pre-post\new_data\C2-MAX_NK_Af_preExp_atubulin_mitoRFP_snap_1_stack_5-1.tif"#todo: resize this x 4
similarity_parameter_file = r"D:\Daten\Nora\Pre-post\similarity_parameters.txt"

b_spline_parameter_file = r"D:\Daten\Nora\Pre-post\b_spline_parameters.txt"


def resize_image():
    image = io.imread(path2)
    output_dimension = (int(image.shape[0]*EXPECTED_EXPASION),int(image.shape[1]*EXPECTED_EXPASION))
    image = resize(image,output_dimension, preserve_range=True)
    io.imsave("resized.tif", image.astype("uint16"))
    resized_path = os.getcwd()+r"\resized.tif"

resize_image()

fixedImage = sitk.ReadImage(path1)
movingImage = sitk.ReadImage('resized.tif')
similarityParameterMap = sitk.ReadParameterFile(similarity_parameter_file)
bSplineParameterMap = sitk.ReadParameterFile(b_spline_parameter_file)

elastixSimilarityFilter = sitk.ElastixImageFilter()
elastixSimilarityFilter.SetFixedImage(fixedImage)
elastixSimilarityFilter.SetMovingImage(movingImage)
elastixSimilarityFilter.SetParameterMap(similarityParameterMap)
elastixSimilarityFilter.Execute()

resultImage = elastixSimilarityFilter.GetResultImage()
transformParameterMap = elastixSimilarityFilter.GetTransformParameterMap()

resultImage = elastixSimilarityFilter.GetResultImage()
transformParameterMap = elastixSimilarityFilter.GetTransformParameterMap()

plt.imshow(sitk.GetArrayFromImage(resultImage), cmap=plt.cm.gray)
plt.imshow(sitk.GetArrayFromImage(fixedImage), cmap=plt.cm.viridis, alpha=0.5)
plt.show()

elastixSplineFilter = sitk.ElastixImageFilter()
elastixSplineFilter.SetFixedImage(fixedImage)
elastixSplineFilter.SetMovingImage(resultImage)
elastixSplineFilter.SetParameterMap(bSplineParameterMap)
elastixSplineFilter.Execute()

resultImage = elastixSplineFilter.GetResultImage()
transformParameterMap = elastixSplineFilter.GetTransformParameterMap(0)
sitk.WriteParameterFile(transformParameterMap, "b_spline.txt")

plt.imshow(sitk.GetArrayFromImage(resultImage), cmap=plt.cm.gray)
plt.imshow(sitk.GetArrayFromImage(fixedImage), cmap=plt.cm.viridis, alpha=0.5)
plt.show()
#
image = sitk.GetArrayFromImage(fixedImage)


transformParameterMap = sitk.ReadParameterFile("b_spline.txt")
X = np.arange(0,image.shape[0])
XY, YX = np.meshgrid(X,X)
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetTransformParameterMap(transformParameterMap)
transformixImageFilter.SetMovingImage(sitk.GetImageFromArray(XY))
transformixImageFilter.Execute()

XY_new = sitk.GetArrayFromImage(transformixImageFilter.GetResultImage())

transformixImageFilter.SetMovingImage(sitk.GetImageFromArray(YX))
transformixImageFilter.Execute()
YX_new = sitk.GetArrayFromImage(transformixImageFilter.GetResultImage())


#todo: run elastics command line interface (bspline transform)
#todo: compute point transformation and plot overlay with vectormap

#todo: another working directory?

XY_final = XY_new-XY
YX_final = YX_new-YX
XY_final[np.where(XY_new==0)] = 0
YX_final[np.where(YX_new==0)] = 0
XY = XY[::SPACING,::SPACING]
YX = YX[::SPACING,::SPACING]

def get_c_map(array):
    lower = array.min()
    upper = array.max()
    colors = plt.cm.jet((array-lower)/(upper-lower))
    return colors


XY_final = XY_final[::SPACING,::SPACING]
YX_final = YX_final[::SPACING,::SPACING]
I = image[::SPACING, ::SPACING]
values = np.abs(XY_final)+np.abs(YX_final)
values[np.where(I<=0.1*I.max())] =0
C = get_c_map(values)
#C = np.swapaxes(C,0,1)

plt.quiver(XY, YX, -XY_final, YX_final, values, cmap=plt.cm.jet)
plt.imshow(image, cmap=plt.cm.viridis)
plt.show()
