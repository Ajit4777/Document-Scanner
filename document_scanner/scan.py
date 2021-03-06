import document_scanner.Transform.transform
from document_scanner.Transform.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

class ScanImage():
	def SetImage(self,imageName):
		print(imageName)
		self.image = cv2.imread(imageName)
		scannedImage = self.SetImageResolution(self.image)

		return scannedImage

	def SetImageResolution(self,image):
		ratio = image.shape[0] / 500.0
		self.orig = image.copy()
		self.image = imutils.resize(image, height = 500)
		scannedImage =  self.ConvertImage(ratio)
		return scannedImage
		
	def ConvertImage(self,ratio):
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)
		edged = cv2.Canny(gray, 75, 200)
		cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
		for c in cnts:
    		# approximate the contour
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)

			# if our approximated contour has four points, then we
			# can assume that we have found our screen
			if len(approx) == 4:
				screenCnt = approx
				break
		cv2.drawContours(self.image, [screenCnt], -1, (0, 255, 0), 2)
		warped = four_point_transform(self.orig, screenCnt.reshape(4, 2) * ratio)
		# convert the warped image to grayscale, then threshold it
		# to give it that 'black and white' paper effect
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
		T = threshold_local(warped, 11, offset = 10, method = "gaussian")
		warped = (warped > T).astype("uint8") * 255
		return warped,imutils.resize(warped, height = 1280)
