#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Yeryo
# datetime: 2022/10/24 21:32 
# func:


import cv2 as cv

path_jpg_raw1 = r'd:/need/all_picture/test.jpg'
img_raw = cv.imread(path_jpg_raw1, cv.IMREAD_UNCHANGED)
print(img_raw.shape)
