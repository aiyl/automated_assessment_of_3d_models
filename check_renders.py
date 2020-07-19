import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

ERR_OK = 0
ERR_WA = 1
ERR_PE = 2
ERR_UH = 3
eps = 10e-3

class Check_renders:
	ds_list = []
	def __init__(self, imgOut, imgAns):
		self.imgOut = imgOut  # path to image эталон
		self.imgAns = imgAns  # решение участника
		for i  in range(len(imgOut)):
			self.ds_list.append(self.compare(imgOut[i], imgAns[i]))

	def mse(self, imageA, imageB):
		err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
		err /= float(imageA.shape[0] * imageA.shape[1])
		return err

	def compare(self, imgAnsPath, imgOutPath):
		x1 = cv2.imread(imgAnsPath)
		x2 = cv2.imread(imgOutPath)
		b1, g1, r1 = cv2.split(x1)
		b2, g2, r2 = cv2.split(x2)
		b = ssim(b1, b2)
		g = ssim(g1, g2)
		r = ssim(r1, r2)
		ds = (1.0 - (b + g + r) * 0.333333) / 2.0
		return ds