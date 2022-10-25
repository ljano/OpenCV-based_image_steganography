from typing import Tuple

import cv2 as cv
import numpy as np
import math


def get_text(path) -> str:
    """
    读取文本
    :param path: 文本路径
    :return:
    """
    # path = input(f"请输入文件路径")
    f1 = open(path, 'r')
    return f1.read()  # 类型是<class 'str'>
    # f1 = open(path, 'rb')
    # return str(f1.read())  # 类型是<class 'str'>


def to_ascii(text: str) -> list:
    """
    字符串转ASCII值（二进制形式）
    :param text: 要隐藏的字符串文本数据
    :return: 形如['00110001', '00110010', '00110011']
    """
    # ascii_values = [ord(s) for s in text]
    ascii_values = [format(ord(s), '08b') for s in text]

    # ascii_values = []
    # for s in text:
    #     ascii_values.append(format(ord(s), '08b'))
    return ascii_values


def count(data: str) -> [int, int, int]:
    """
    计算要嵌入数据的比特串长度、需要的像素点个数、需要的像素值个数
    :param data: 要隐藏的字符串文本数据
    :return: 依次返回length, all_point, all_value
    """
    # 要嵌入数据的比特串长度
    length = 8 * len(data)
    # 需要的像素点个数
    all_point = len(data) * 3
    # 需要的像素值个数
    all_value = len(data) * 3 * 3
    return length, all_point, all_value


def get_pix(img: np.ndarray, data: str) -> list:
    """
    获取图像的BGR值。作为参数传入encode函数
    # 读取方式为从上至下，从左至右。故采取img.shape[0]控制不溢出（也可直接用二者相乘计算）
    # 题目给定图片像素为600*800（最大存储二进制数为 600 * 800 * 3 = 1440000，字符数再除以8=180000），理论上存储题目要求的py文件绰绰有余（3329字符再加上空格&换行也不会超过5000）
    :param img: 原图
    :param data: 要隐藏的字符串文本数据
    :return: img.item返回int类型，存入列表pix_raw中返回
    """
    print("\n>>>开始读取原图中需要的像素值...")

    length, all_point, all_value = count(data)
    pix_raw = []

    print(f"1.要存储的字符个数（亦即需要的flag个数）为：{len(data)}\n"
          f"2.对应的二进制串长度为：{len(data)}*8 = {length}\n"
          f"3.需要的像素点个数为；{len(data)}*3 = {all_point}\n"
          f"4.总计需要的像素值个数为：{len(data)}+{length} = {all_point}*3 = {all_value}")
    print(f"5.图片像素为：{img.shape[0]}*{img.shape[1]}")
    # m = 0

    num = math.modf(all_value / (3 * img.shape[1]))
    # num[0]为小数部分，num[1]为整数部分。且均为float。 存储所有字符需要的行数为{1}或{num[1]+1}
    # 存满的行数
    row = int(num[1])

    if row == 0:
        # 说明一行足矣
        print(f"6.存储所有字符需要的行数为：{1}")
        i = 0
        # pix_raw = [img.item(i, j, k)
        #            for j in range(0, all_point)
        #            for k in range(0, 3)]
        # 上述为列表解析式法，下面为for循环法。下同。
        pix_raw = []
        for j in range(0, all_point):  # 我说怎么进不去循环，原来这里之前写的取余，超
            for k in range(0, 3):
                # 可打印每个点的像素值看看
                print(f"({i}, {j}, {k})的像素值为：{img.item(i, j, k)}")
                pix_raw.append(img.item(i, j, k))

    else:
        # 需要的行数是num[1]+1，其中num[1]行存满，余一行大概率存不满
        print(f"6.存储所有字符需要的行数为：{int(num[1]+1)}")
        # 1.将前row行的像素值读出来
        pix_raw_1 = [img.item(i, j, k)
                     for i in range(0, row)
                     for j in range(0, img.shape[1])
                     for k in range(0, 3)]
        # print(pix_raw_1)
        # for i in range(0, row):
        #     for j in range(0, img.shape[1]):
        #         for k in range(0, 3):
        #             pix_raw.append(img.item(i, j, k))

        # 2.将最后一行需要的的像素值读出来
        i = row  # 妈的这里忘改了
        val_rest = all_value - row * img.shape[1] * 3  # 之前这里没*3一直报错，长度溢出
        print(f"7.已存像素值个数为：{row * img.shape[1] * 3}，"
              f"剩余待存像素值个数为：{val_rest}，即还需要{val_rest}/3 = {int(val_rest / 3)}个像素点")

        try:
            pix_raw = pix_raw_1 + [img.item(i, j, k)
                                   for j in range(0, int(val_rest / 3))  # 这里的val_rest应该要除以3
                                   for k in range(0, 3)]
        except IndexError as err:
            print(f"索引超啦！Error is {err}")
        else:
            print("获取原图像素值完毕！")
        # print(f"哥们开始存第{row + 1}行了，他们的像素依次是：")
        # pix_raw_2 = []
        # for j in range(0, int(val_rest / 3)):
        #     for k in range(0, 3):
        #         pix_raw_2.append(img.item(i, j, k))
        #         print(img.item(i, j, k))
        # pix_raw = pix_raw_1 + pix_raw_2

    if all_value == len(pix_raw):
        print("获取的像素值个数和需要的相等，成功！")
        # print(f"原图像素值为{pix_raw}\n原图像素值列表长度为：{len(pix_raw)}")

    return pix_raw


def type_change(pix: list) -> list:
    """
    将像素值列表内元素类型由int转为tuple，每3个int转为一个tuple:[int, int, int]
    弃用。直接输入输出一个存储元素类型为int的列表即可。
    :param pix: [int, int, ...]
    :return: [tuple, tuple, ...]
    """


def encode(pixel: list, data: str) -> list:
    """
    编码，修改像素值列表，1则变奇数，0则变偶数。第9位未读完变偶数，反之奇数。
    详见 一些记录.md
    :param pixel: 像素值，一个长度为len(text) * 8的列表。
                  参考格式；[int, int, ...]
    :param data: 要隐藏的字符串文本数据
    :return: 修改后的像素值列表
    """

    print("\n>>>开始修改像素值...")

    # 注意复制列表不能直接采用赋值法，否则对列表的任何修改都是永久的，无法保留原列表。
    pix_new = pixel.copy()  # 等价于切片法复制：pix_new = pixel[:]

    # 获得text的二进制ASCII值
    data_list = to_ascii(data)
    # length, all_point, all_value = count(data)
    # print(len(data_list))  # 3

    # 这一部分是用来改格式的，现在换了输入格式，弃用。
    # 创建迭代器对象用于遍历
    # pix_iter = iter(pixel)
    # 将pixel内的元素类型由元组转为整型（即提取出来，便于后续访问）：[12, 34, 65, 32, 45, 89, 23, 55, 76]
    # pixel = [value for value in pix_iter.__next__()[:3] + pix_iter.__next__()[:3] + pix_iter.__next__()[:3]]
    try:
        # 这个m一定要在循环外。一开始写循环里了，debug才发现每次进内循环都置0了。。。
        m = 0
        for i in range(0, len(data_list)):
            for j in range(0, 8):
                # 测试数据为123：['00110001', '00110010', '00110011']。water_0、1、2、3、4均已通过。
                # 只有 “0/奇” 和 “1/偶” 需要变，且均执行减1操作。对于本实验不存在加1可能，因为原图不存在像素值为0的情况。

                # 第i个数据的第j位ASCII值为0，且像素值为奇数
                if data_list[i][j] == '0' and pixel[i * 8 + j + m] % 2 != 0:
                    pix_new[i * 8 + j + m] -= 1
                # 第i个数据的第j位ASCII值为1，且像素值为偶数
                elif data_list[i][j] == '1' and pixel[i * 8 + j + m] % 2 == 0:
                    if pixel[i * 8 + j + m] != 0:
                        pix_new[i * 8 + j + m] -= 1
                    else:
                        pix_new[i * 8 + j + m] += 1

                # 将前面的每一个flag置偶。依次是8、17、26...（3n-1，n=3k，k为整数），公差为9，每一轮加9（由 i * 8 + m 控制）
                flag = i * 8 + j + m + 1
                # debug发现是这个地方他丫的没加括号，python运算符优先级 & > %  下面的if同理。
                if (i != len(data_list) - 1) & (j == 7) & (pixel[flag] % 2 != 0):
                    '''
                    第一个括号用来防止最后一个flag为奇数时减2的情况出现（进入该if和下面的if各减1）
                    第二个和第三个用来将前面所有的非偶flag置偶
                    '''
                    pix_new[flag] -= 1
            # 外层循环每轮加1，以跳过flag，避免覆盖
            m += 1
            # 像素值列表最后一个flag应置奇，停止。之前的全置偶
            if (i == len(data_list) - 1) & (pixel[-1] % 2 == 0):
                pix_new[-1] -= 1

    except IndexError as err:
        print(f"索引超啦！Error is {err}")
    else:
        print("修改像素值完毕！")

    return pix_new


def encode_write(img: np.ndarray, pixel_new: list, data: str) -> np.ndarray:
    """
    将修改好的像素值写入图片。
    :param img: 待写入的图片
    :param pixel_new: 待写入的像素值列表
    :param data: 要隐藏的文本字符串
    :return: 写入后的新图像
    """

    print("\n>>>开始将像素值写入图片...")

    img_new = img.copy()
    length, all_point, all_value = count(data)

    # 解释可见get_pix函数
    num = math.modf(all_value / (3 * img.shape[1]))
    row = int(num[1])
    try:
        # 参数加上数字便于debug
        if row == 0:
            # 说明一行足矣
            i0 = 0
            for j0 in range(0, all_point):
                for k0 in range(0, 3):
                    t0 = i0 * img.shape[1] * 3 + j0 * 3 + k0 + 1
                    for m0 in range(0, t0):
                        img_new.itemset((i0, j0, k0), pixel_new[m0])
        else:
            # 先写前row行像素
            for i1 in range(0, row):
                for j1 in range(0, img.shape[1]):
                    for k1 in range(0, 3):
                        t1 = i1 * img.shape[1] * 3 + j1 * 3 + k1
                        img_new.itemset((i1, j1, k1), pixel_new[t1])

            # 再写最后一行（第row+1行）
            i2 = row  # 应该存在第row+1行，i下标从0开始，下标置row
            val_rest = all_value - row * img.shape[1] * 3
            print(f"已经写入的像素值数为：{row * img.shape[1] * 3}\n剩余像素值数为：{val_rest}")
            for j2 in range(0, int(val_rest / 3)):
                for k2 in range(0, 3):
                    t2 = row * img.shape[1] * 3 + j2 * 3 + k2
                    img_new.itemset((i2, j2, k2), pixel_new[t2])
    except IndexError as err:
        print(f"索引超啦！Error is {err}")
    else:
        print("写入像素值完毕！")

    # # 先写前row行像素
    # for i in range(0, row):
    #     for j in range(0, img.shape[1]):
    #         for k in range(0, 3):
    #             for m in range(0, i * img.shape[1] * 3 + j * 3 + k):
    #                 img_new.itemset((i, j, k), pixel_new[m])
    # # 再写最后一行（row + 1）
    # i = row + 1
    # val_rest = all_value - row * img.shape[1] * 3
    # print(f"已经写入的像素值数为：{row * img.shape[1] * 3}\n剩余像素值数为：{val_rest}")
    # for j in range(0, int(val_rest / 3)):
    #     for k in range(0, 3):
    #         for m in range(row * img.shape[1] * 3, all_value):
    #             img_new.itemset((i, j, k), pixel_new[m])

    # # 测试用例
    # i = 0
    # for j in range(0, len(pixel_new) % 3):
    #     for k in range(0, 3):
    #         for m in range(0, i * 800 + j * 3 + k):
    #             img_new.itemset((i, j, k), pixel_new[m])

    return img_new


if __name__ == '__main__':
    pass






