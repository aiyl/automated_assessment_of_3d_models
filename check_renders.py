import sys
import os
from json import loads
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


ERR_OK = 0
ERR_WA = 1
ERR_PE = 2
ERR_UH = 3

rootDir = os.path.dirname(os.path.abspath(__file__))
eps = 10e-3
maxPoint = 5
errweight = 10
class Check_renders:
	points = 0
	all_points = 0
	def __init__(self, imgOut, imgAns):
		self.imgOut = imgOut  # path to image эталон
		self.imgAns = imgAns  # решение участника
		for i  in range(len(imgOut)):
			self.points += self.compare(imgOut[i], imgAns[i])
		verh = 100 * self.points
		niz = maxPoint*len(imgAns)*10
		dif =int( verh/niz)
		self.all_points = 10 - dif

	def mse(self, imageA, imageB):
		err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
		err /= float(imageA.shape[0] * imageA.shape[1])
		return err


	def compare(self, imgAnsPath, imgOutPath):
		x1 = cv2.imread(imgAnsPath)
		x2 = cv2.imread(imgOutPath)

		x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2GRAY)
		x2 = cv2.cvtColor(x2, cv2.COLOR_BGR2GRAY)

		m = self.mse(x1, x2)
		s = ssim(x1, x2)
		ds = (1 - s) / 2

		#print("mse: %s, ssim: %s, dssim: %s" % (m, s, ds))

		if ds < eps:
			#print(ds)
			return ds
			#self.points = ds
			#exit(ERR_OK)
		else:
			#self.points = max(int((1 - ds*errweight)*maxPoint), 0)
			return max(int((1 - ds*errweight)*maxPoint), 0)
			#print(max(int((1 - ds*errweight)*maxPoint), 0))
			#exit(ERR_OK)

