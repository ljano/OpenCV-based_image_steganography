# func: 压缩主函数

import os
import cv2 as cv
from PIL import Image
import tinify
import main
import main_2
import main_3
import main_4
import main_5
import encode as e
import decode as d
import numpy as np


class CV:
    """
    openCV压缩
    """
    def get_m_size(self, path):
        img_size = os.path.getsize(path)
        img_size /= 1024  # 除以1024是代表Kb
        # print(img_size)
        return img_size

    def compress_png(self, path_raw, path_save, val):
        """
        将图片压缩为png。
        若需要重复压缩必须要修改val参数值，否则输出图片大小不会变化。
        :param path_raw: 待压缩的原始图片路径
        :param path_save: 压缩后的图片的保存路径
        :param val: 压缩比，取值范围0-9，越大代表压缩力度越大
        :return:
        """
        size_png_raw = self.get_m_size(path_raw)
        img_png = cv.imread(path_raw, cv.IMREAD_UNCHANGED)
        # 保存为png时可以设置压缩比，0-9，最大为9，越大代表压缩力度越大。
        cv.imwrite(path_save, img_png, [cv.IMWRITE_PNG_COMPRESSION, val])
        size_png_new = self.get_m_size(path_save)
        print(f"压缩前png大小为：{size_png_raw}\n压缩后png大小为：{size_png_new}\n")

    def compress_jpg(self, path_raw, path_save, val):
        """
        将图片压缩为jpg。
        若需要重复压缩必须要修改val参数值，否则输出图片大小不会变化。
        :param path_raw: 待压缩的原始图片路径
        :param path_save: 压缩后的图片的保存路径
        :param val: 压缩比，取值范围0-100，越小代表压缩力度越大。【不建议低于50】
        :return:
        """
        size_jpg_raw = self.get_m_size(path_raw)
        img_jpg = cv.imread(path_raw, cv.IMREAD_UNCHANGED)
        # param2为压缩参数，数字代表压缩比例，该值范围在0-100，越小代表压缩力度越大
        cv.imwrite(path_save, img_jpg, [cv.IMWRITE_JPEG_QUALITY, val])
        size_jpg_new = self.get_m_size(path_save)
        print(f"压缩前jpg大小为：{size_jpg_raw}\n压缩后jpg大小为：{size_jpg_new}")

    def out_png(self, num_1, num_2, path_png_save, path_jpg_save):
        """
        理想（失败）：不断更换jpg输入，直到得到合适大小的png
        目前功能：选择合适参数可稳定输出某些大小的图像
        :param num_1: main_3.start_one的参数1。用于标识图片（单图&五图的话随便传个参数就行）
        :param num_2: main_2.start_one的参数，亦是main_3.start_one的参数2。用于标识图片（结合num_1标识十图）
        :param path_png_save: 所有png的存储路径。最后压缩合格的png的存储路径
        :param path_jpg_save: 所有jpg的存储路径
        :return:
        """
        i, mb, q, s = 75, 13, 75, 1
        pil = PIL(mb, q, s, path_png_save, path_jpg_save)

        # while True:  # 这玩意用来debug
        # 这里不用无限循环是因为前几轮循环png不降反增，而且多次调用pil压缩jpg会导致在某一轮循环里jpg严重受损，达不到我所期望的一轮循环减小几kb甚至零点几kb
        for k in range(1):
            png_size_raw = self.get_m_size(path_png_save)
            # 【1】.第一步压缩。调用PIL压缩，输入为大小为png_size_raw的png
            path_jpg_save, jpg_size_pil_1 = pil.compress_image()
            # if (k == 0) | (k == 1):
            #     path_jpg_save, jpg_size_pil_1 = pil.compress_image()

            # self.compress_png(path_png_save, path_png_save, 9)
            # 【2】.第二步压缩。调用openCV压缩，输入为第一步压缩得到的jpg
            self.compress_jpg(path_jpg_save, path_jpg_save, i)
            jpg_size_cv_2 = self.get_m_size(path_jpg_save)
            # if (k == 0) | (k == 1):
            #     self.compress_jpg(path_jpg_save, path_jpg_save, i)
            #     jpg_size_cv_2 = self.get_m_size(path_jpg_save)

            # img_new_png = cv.imread(path_jpg_save, cv.IMREAD_UNCHANGED)
            # cv.imwrite(path_png_save, img_new_png, [cv.IMWRITE_PNG_COMPRESSION, 9])
            # 【3】.复写数据。将由两轮压缩得到的jpg作为main的输入，再次写入数据。因为多轮压缩得到的jpg一定是重新变成灰度图像了，只是像素值发生了变化（可通过上面两行代码查看ndarray）
            '''
            1.单图的
            '''
            # main.main(path_jpg_save, path_png_save)
            '''
            2.五图的（阈值加密）
            '''
            # # 这里不能跑这个，因为每次传入一张图片进行压缩，故只能写那一张图片对应的数据。若跑start则5个全写进去了而且出来一堆。。。
            # # main_2.start_five(path_jpg_save, path_png_save)
            main_2.start_one(0, num_2, path_jpg_save, path_png_save)
            '''
            3.十图的（阈值加密）
            '''
            # main_3.start_one(num_1, num_2, path_jpg_save, path_png_save)
            '''
            4.十五图的（阈值加密）
            '''
            # main_4.start_one(num_1, num_2, path_jpg_save, path_png_save)
            '''
            5.三十图的（阈值加密）
            '''
            # main_5.start_one(num_1, num_2, path_jpg_save, path_png_save)

            # 读一下压缩后png大小并尝试利用循环输出指定大小范围的图片（失败。因为2次及以上的重复压缩大概率会导致图片失真严重）
            png_size_new = self.get_m_size(path_png_save)
            if png_size_new > 75.4:
                # 在这里修改cv和pil压缩函数里的一些参数，可能有用。
                pass
                # i没必要动，变化不大
                # i -= 5
                # j -= 1
                # pil = PIL(mb, path_png_save, path_jpg_save)


class PIL:
    """
    PIL压缩。可重复压缩，不必改参。
    """
    def __init__(self, mb, q, s, infile, outfile):
        """
        初始化一些参数，给后面的方法使用
        :param mb: 压缩目标，KB。【当q较小时，不建议低于16，否则受损严重.倒也不是】
        :param q: 初始压缩比率，q的范围从1（最差）到95（最佳），默认值为75，使用中应尽量避免高于95的值;100会禁用部分JPEG压缩算法，并导致大文件图像质量几乎没有任何增益。
                  【当mb较小时，不建议低于20，否则受损严重】
        :param s: 每次调整的压缩比率。越小越精确，使压缩结果更趋近于mb。因此当s足够小（最小取1），q的值小一点并不影响结果（50-90效果一样，再低没测过）
        :param infile: 压缩源文件地址
        :param outfile: 压缩文件保存地址
        """
        self.mb = mb
        self.step = s
        self.quality = q
        self.infile = infile
        self.outfile = outfile

    def get_outfile(self):
        if self.outfile:
            return self.outfile
        dire, suffix = os.path.splitext(self.infile)
        self.outfile = '{}-out{}'.format(dire, suffix)
        return self.outfile

    def compress_image(self):
        """
        不改变图片尺寸压缩到指定大小
        :return: 压缩文件地址，压缩文件大小
        """
        cv1 = CV()
        o_size = cv1.get_m_size(self.infile)
        if o_size <= self.mb:
            return self.infile
        outfile = self.get_outfile()
        while o_size > self.mb:
            im = Image.open(self.infile)
            im.save(self.outfile, quality=self.quality)
            if self.quality - self.step < 0:
                break
            self.quality -= self.step
            o_size = cv1.get_m_size(self.outfile)
        return self.outfile, cv1.get_m_size(self.outfile)


class Tinify:
    """
    tinify压缩
    """
    def __init__(self):
        # 申请的密钥。一个月免费调用500次
        tinify.key = "WcXCF4ZYlPv47h3jWG6HmTBmLZSgm7qM"
        # saveFile_path = r'd:/need/all_picture/test.jpg'
        save_path = r'd:/pythonProjects/opencv_test/compress_img.png'
        # 从本地读取
        source = tinify.from_file(save_path)
        # 默认存在当前python项目文件目录下
        source.to_file("compress_img_2.png")


def one():
    """
    1.单图。对应main
    :return:
    """
    cv2_1 = CV()
    # 待压缩的原始图片路径
    path_jpg_raw1 = r'd:/need/all_picture/test.jpg'

    # 压缩后的图片的保存路径
    path_png_save1 = r'd:/need/all_picture/new1.png'
    path_jpg_save1 = r'd:/need/all_picture/new1.jpg'
    # 先跑一遍。输入题目所给图片，得到301kb的png存储于path_png_save1
    main.main(path_jpg_raw1, path_png_save1)
    # c.compress_jpg(path_png_raw, path_jpg_save, 50)
    cv2_1.out_png(0, 0, path_png_save1, path_jpg_save1)


def five():
    """
    2.五图。阈值加密。对应main_2
    :return:
    """
    cv2_5 = CV()
    # 待压缩的原始图片路径
    path_jpg_raw1 = r'd:/need/all_picture/test.jpg'

    # 压缩后的图片的保存路径【报错已解决】
    path_png_save1 = ["d:/need/all_picture/threshold/five/share_{}.png".format(i) for i in range(5)]
    path_jpg_save1 = ["d:/need/all_picture/threshold/five/share_{}.jpg".format(i) for i in range(5)]

    # 1.先跑一遍。输入题目所给图片，得到307kb的png存储于path_png_save1
    main_2.start_five(path_jpg_raw1, path_png_save1)
    # c.compress_jpg(path_png_raw, path_jpg_save, 50)

    # 2.依次压缩每张图片并保存至对应路径
    for i in range(5):
        cv2_5.out_png(0, i, path_png_save1[i], path_jpg_save1[i])
    # print("没到这。输出第一个jpg就挂了")

    # 为下一步提供输入
    data = main_2.data_init()
    img_raw = cv.imread(path_jpg_raw1, cv.IMREAD_UNCHANGED)
    # 3.读取压缩后图片中隐藏的数据并将其恢复，写入txt文件中
    d.get_rec(img_raw, data, path_png_save1)


def ten():
    """
    3.十图。阈值加密。对应main_3
    :return:
    """
    cv2_10 = CV()
    # 待压缩的原始图片路径
    path_jpg_raw1 = r'd:/need/all_picture/test.jpg'

    # 压缩后的图片的保存路径
    path_png_save1 = [["d:/need/all_picture/threshold/ten/share_{}_{}.png".format(i, j) for j in range(2)]
                      for i in range(5)]
    path_jpg_save1 = [["d:/need/all_picture/threshold/ten/share_{}_{}.jpg".format(i, j) for j in range(2)]
                      for i in range(5)]

    # 1.先跑一遍。输入题目所给图片，得到300kb的png存储于path_png_save1
    main_3.start_ten(path_jpg_raw1, path_png_save1)

    # 2.依次压缩每张图片并保存至对应路径
    for i in range(5):
        for j in range(2):
            cv2_10.out_png(i, j, path_png_save1[i][j], path_jpg_save1[i][j])

    # 为下一步提供输入
    data = main_3.data_init()
    img_raw = cv.imread(path_jpg_raw1, cv.IMREAD_UNCHANGED)
    # 3.读取压缩后图片中隐藏的数据并将其恢复，写入txt文件中
    d.get_rec_ten(img_raw, data, path_png_save1)


def fifteen():
    """
    4.十五图。阈值加密。对应main_4
    :return:
    """
    cv2_15 = CV()
    # 待压缩的原始图片路径
    path_jpg_raw1 = r'd:/need/all_picture/test.jpg'

    # 压缩后的图片的保存路径
    path_png_save1 = [["d:/need/all_picture/threshold/fifteen/share_{}_{}.png".format(i, j) for j in range(3)]
                      for i in range(5)]
    path_jpg_save1 = [["d:/need/all_picture/threshold/fifteen/share_{}_{}.jpg".format(i, j) for j in range(3)]
                      for i in range(5)]

    # 1.先跑一遍。输入题目所给图片，得到298kb的png存储于path_png_save1
    main_4.start_fifteen(path_jpg_raw1, path_png_save1)

    # 2.依次压缩每张图片并保存至对应路径
    for i in range(5):
        for j in range(3):
            cv2_15.out_png(i, j, path_png_save1[i][j], path_jpg_save1[i][j])

    # 为下一步提供输入
    data = main_4.data_init()
    img_raw = cv.imread(path_jpg_raw1, cv.IMREAD_UNCHANGED)
    # 3.读取压缩后图片中隐藏的数据并将其恢复，写入txt文件中
    d.get_rec_fifteen(img_raw, data, path_png_save1)


def thirty():
    """
    4.三十图。阈值加密。对应main_5
    :return:
    """
    cv2_30 = CV()
    # 待压缩的原始图片路径
    path_jpg_raw1 = r'd:/need/all_picture/test.jpg'

    # 压缩后的图片的保存路径
    path_png_save1 = [["d:/need/all_picture/threshold/thirty/share_{}_{}.png".format(i, j) for j in range(6)]
                      for i in range(5)]
    path_jpg_save1 = [["d:/need/all_picture/threshold/thirty/share_{}_{}.jpg".format(i, j) for j in range(6)]
                      for i in range(5)]

    # 1.先跑一遍。输入题目所给图片，得到294kb的png存储于path_png_save1
    main_5.start_thirty(path_jpg_raw1, path_png_save1)

    # 2.依次压缩每张图片并保存至对应路径
    for i in range(5):
        for j in range(6):
            cv2_30.out_png(i, j, path_png_save1[i][j], path_jpg_save1[i][j])

    # 为下一步提供输入
    data = main_5.data_init()
    img_raw = cv.imread(path_jpg_raw1, cv.IMREAD_UNCHANGED)
    # 3.读取压缩后图片中隐藏的数据并将其恢复，写入txt文件中
    d.get_rec_thirty(img_raw, data, path_png_save1)


if __name__ == '__main__':
    # one()
    five()
    # ten()
    # fifteen()
    # thirty()
