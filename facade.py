import SimpleITK as sitk
from collections import namedtuple
import numpy as np

class TransformElastix():
    ECPECTED_EXPANSION = 3.5
    SPACING = 40
    INITIAL_SIMILARITY_PF = "static/similarity_parameters.txt"
    INITIAL_SPLINE_PF = "static/b_spline_parameters.txt"
    QUIVER = namedtuple("Quiver", "XY YX XY_final YX_final cm")

    def __init__(self):
        self._fixed_i = None
        self._move_i = None
        self.BTP = None
        self.STP = None
        self.similarityParameterMap = sitk.ReadParameterFile(self.INITIAL_SIMILARITY_PF)
        self.bSplineParameterMap = sitk.ReadParameterFile(self.INITIAL_SPLINE_PF)

        self.process = sitk.ElastixImageFilter()
        self.process.SetOutputDirectory("tmp")
        self.t_process = sitk.TransformixImageFilter()
        self.t_process.SetOutputDirectory("tmp")


    def similarity_transform(self):
        if not self._fixed_i or not self._move_i:
            raise ValueError("Set fixed and moving image before transform")
        self.process.SetFixedImage(self._fixed_i)
        self.process.SetMovingImage(self._move_i)
        self.process.SetParameterMap(self.similarityParameterMap)
        self.process.Execute()
        self.STP = self.process.GetTransformParameterMap(0)
        sitk.WriteParameterFile(self.STP, "tmp/similarity.txt")



    def b_spline_tranform(self):
        if not self._fixed_i or not self._move_i:
            raise ValueError("Set fixed and moving image before transform")
        self.process.SetFixedImage(self._fixed_i)
        self.process.SetMovingImage(self._move_i)
        self.process.SetParameterMap(self.bSplineParameterMap)
        self.process.Execute()

        self.BTP = self.process.GetTransformParameterMap(0)
        sitk.WriteParameterFile(self.BTP, "tmp/b_spline.txt")

    def apply_b_spline_transform(self, image):
        if not self.BTP:
            self.BTP = sitk.ReadParameterFile("tmp/b_spline.txt")
        self.t_process.SetTransformParameterMap(self.BTP)
        self.t_process.SetMovingImage(sitk.GetImageFromArray(image))
        self.t_process.Execute()

    def get_distortion_map(self):
        if not self.BTP:
            self.BTP = sitk.ReadParameterFile("tmp/b_spline.txt")
        self.t_process.SetTransformParameterMap(self.BTP)
        X = np.arange(0, self.fixed_image.shape[1])
        Y = np.arange(0, self.fixed_image.shape[0])
        XY, YX = np.meshgrid(X, Y)
        self.t_process.SetMovingImage(sitk.GetImageFromArray(XY))
        self.t_process.Execute()
        XY_new = self.t_result_image

        self.t_process.SetMovingImage(sitk.GetImageFromArray(YX))
        self.t_process.Execute()
        YX_new = self.t_result_image

        XY_final = XY - XY_new
        YX_final = YX - YX_new
        XY_final[np.where(XY_new == 0)] = 0
        YX_final[np.where(YX_new == 0)] = 0
        XY = XY[::self.SPACING, ::self.SPACING]
        YX = YX[::self.SPACING, ::self.SPACING]
        XY_final = XY_final[::self.SPACING, ::self.SPACING]
        YX_final = YX_final[::self.SPACING, ::self.SPACING]

        values = np.abs(XY_final) + np.abs(YX_final)

        return self.QUIVER(XY, YX, XY_final, YX_final, values)

    @property
    def fixed_image(self):
        return sitk.GetArrayFromImage(self._fixed_i)

    @fixed_image.setter
    def fixed_image(self, value):
        if isinstance(value, str):
            self._fixed_i = sitk.ReadImage(value)
        else:
            self._fixed_i = sitk.GetImageFromArray(value)

    @property
    def moving_image(self):
        return sitk.GetArrayFromImage(self._move_i)

    @moving_image.setter
    def moving_image(self, value):
        if isinstance(value, str):
            self._move_i = sitk.ReadImage(value)
        else:
            self._move_i = sitk.GetImageFromArray(value)

    @property
    def result_image(self):
        return sitk.GetArrayFromImage(self.process.GetResultImage())

    @property
    def t_result_image(self):
        return sitk.GetArrayFromImage(self.t_process.GetResultImage())


