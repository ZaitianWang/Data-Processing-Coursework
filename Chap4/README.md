# Chapter 2 Homework

## Purpose

Image Processing

## Main Supporting Libs

- **OpenCV**
- Numpy
- matplotlib

## Algorithms

- Histogram Equalization: `cv2.equalizeHist()`
- Binarization: `cv2.threshold()`
- Noise Addition: White Gaussian Noise
- Noise Reduction: `cv2.fastNlMeansDenoisingColored()`
- Edge Detection: `cv2.Canny()`

## Special Discovery

_Do noise reduction before edge detection can sometimes gives surprising performance._

For "Lena", texture of the hat is easily recognized as edge, and noise reduction can help.
