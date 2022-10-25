#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Yeryo
# datetime: 2022/10/17 15:21
# func: 十五图

import cv2 as cv
import numpy as np
import encode as e
import decode as d
# import tinify
# import compress as cp
# import compress_CV
# from compress_all import CV, PIL, Tinify
# import operator
# from typing import List, Union


def data_init() -> list:
    """
    初始化要嵌入的数据，存储至列表中返回
    :return:
    """
    try:
        path_text: np.ndarray = np.array([[str] * 3] * 5)
        path_text[0][0] = r'd:\need\txt\fifteen\share_all_0_0.txt'
        path_text[0][1] = r'd:\need\txt\fifteen\share_all_0_1.txt'
        path_text[0][2] = r'd:\need\txt\fifteen\share_all_0_2.txt'
        path_text[1][0] = r'd:\need\txt\fifteen\share_all_1_0.txt'
        path_text[1][1] = r'd:\need\txt\fifteen\share_all_1_1.txt'
        path_text[1][2] = r'd:\need\txt\fifteen\share_all_1_2.txt'
        path_text[2][0] = r'd:\need\txt\fifteen\share_all_2_0.txt'
        path_text[2][1] = r'd:\need\txt\fifteen\share_all_2_1.txt'
        path_text[2][2] = r'd:\need\txt\fifteen\share_all_2_2.txt'
        path_text[3][0] = r'd:\need\txt\fifteen\share_all_3_0.txt'
        path_text[3][1] = r'd:\need\txt\fifteen\share_all_3_1.txt'
        path_text[3][2] = r'd:\need\txt\fifteen\share_all_3_2.txt'
        path_text[4][0] = r'd:\need\txt\fifteen\share_all_4_0.txt'
        path_text[4][1] = r'd:\need\txt\fifteen\share_all_4_1.txt'
        path_text[4][2] = r'd:\need\txt\fifteen\share_all_4_2.txt'

        data_raw = [[e.get_text(path_text[i][j]) for j in range(3)] for i in range(5)]
    except IOError as err:
        print(f"没有找到文件或读取文件失败。Error is {err}")
    else:
        print("读取数据文件成功！")
        return data_raw


def start_fifteen(path_raw, path_save):
    """
    将path_raw中的数图片拷贝十五份，然后将十五份数据分别写入，再初步压缩，得到十五张图片，分别存储于对应路径path_save(见compress_all)。
    :param path_raw: 输入图片的路径（jpg）
    :param path_save: 保存图片的路径（png）
    :return:
    """
    img_raw = cv.imread(path_raw, cv.IMREAD_UNCHANGED)
    a, b, c = img_raw.shape[2], img_raw.shape[1], img_raw.shape[0]
    # 【方法一】用numpy声明三维数组
    # img_new_png: list[np.ndarray] = [np.array([[[int] * a] * b] * c)]
    img_new_png = [np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
                   np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray,
                   np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]  # 必须显式声明个数。还不能直接*5，若更多怎么写？？？
    for i in range(15):
        img_new_png[i]: np.ndarray = np.array([[[int] * a] * b] * c)
    # 【方法二】用list声明三维数组ten\
    # img_new_png: list[list[list[int]]] = [[[0 for col in range(a)] for row in range(b)] for row1 in range(c)]

    print("\n>>>开始读取数据文件和图片...")

    data = data_init()

    try:
        img = [cv.imread(path_raw, cv.IMREAD_UNCHANGED) for i in range(15)]
    except IOError as err:
        print(f"没有找到文件或读取文件失败，图片路径不要有中文哦。Error is {err}")
    else:
        print("读取图片成功！")
        pix_raw: np.ndarray = np.array([[int] * 3] * 5)
        pix_new: np.ndarray = np.array([[int] * 3] * 5)
        img_new = [[np.ndarray([1])] * 3] * 5
        for i in range(5):
            for j in range(3):
                pix_raw[i][j] = e.get_pix(img[i], data[i][j])
                pix_new[i][j] = e.encode(pix_raw[i][j], data[i][j])
                img_new[i][j] = e.encode_write(img[i], pix_new[i][j], data[i][j])
                cv.imwrite(path_save[i][j], img_new[i][j], [cv.IMWRITE_PNG_COMPRESSION, 9])
                # cv.imencode(path_save[i], img_new[i])[1].tofile(path_save[i])

    print("\n>>>开始显示图片...")
    # cv.imshow("new", img_new[0])
    # # print("在这个地方卡死，程序停不下来。。。")
    # cv.waitKey(0)
    # # print("在这个地方卡死，程序停不下来。。。")
    # cv.destroyAllWindows()


def start_one(num_1, num_2, path_raw, path_save):
    """
    对上述图片进行复写操作。一次只输入一张图片，只复写对应的一份数据，再初步压缩，存储于对应路径(见compress_all)。
    用于压缩图片里的循环压缩时调用(compress_all.out_png)
    :param num_1: 输入图片的编号
    :param num_2: 输入图片的编号
    :param path_raw: 输入图片的路径（jpg）
    :param path_save: 保存图片的路径（png）
    :return:
    """

    print("\n>>>开始读取数据文件和图片...")

    data = data_init()

    try:
        # path_img = r'd:\need\all_picture\test.jpg'
        # 这里一定要保证传入的是压缩后的图片path_raw而非上面指定的path_img，否则图片得不到压缩
        img = cv.imread(path_raw, cv.IMREAD_UNCHANGED)
    except IOError as err:
        print(f"没有找到文件或读取文件失败，图片路径不要有中文哦。Error is {err}")
    else:
        print("读取图片成功！")

        # 将对应数据写入对应编号的图片中
        pix_raw = e.get_pix(img, data[num_1][num_2])
        pix_new = e.encode(pix_raw, data[num_1][num_2])
        img_new = e.encode_write(img, pix_new, data[num_1][num_2])

        # png初步压缩
        cv.imwrite(path_save, img_new, [cv.IMWRITE_PNG_COMPRESSION, 9])

        # 验证压缩后的图片是否仍可恢复数据
        img_new_png = cv.imread(path_save, cv.IMREAD_UNCHANGED)
        d.decode(e.to_ascii(data[num_1][num_2]), img_new_png)


if __name__ == '__main__':
    path_png_save1 = [["d:/need/all_picture/threshold/fifteen/share_{}_{}.png".format(i, j) for j in range(3)]
                      for i in range(5)]
    path_jpg_save1 = [["d:/need/all_picture/threshold/fifteen/share_{}_{}.jpg".format(i, j) for j in range(3)]
                      for i in range(5)]
    path_jpg_raw1 = r'd:/need/all_picture/test.jpg'
    start_fifteen(path_jpg_raw1, path_png_save1)

    data = data_init()
    img_raw = cv.imread(path_jpg_raw1, cv.IMREAD_UNCHANGED)
    d.get_rec_fifteen(img_raw, data, path_png_save1)
