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
		self.all_points = dif

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
		points = max(int(round((1 - ds * errweight) * maxPoint, 0)), 0)
		return points