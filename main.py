# func: 单图

import cv2 as cv
import numpy as np
import encode as e
import decode as d
import tinify

# if __name__ == '__main__':


def main(path_raw, path_save):
    """

    :param path_raw: 输入图片的路径（jpg）
    :param path_save: 保存图片的路径（png）
    :return:
    """
    import encode as e
    # 初始化一下，免得警告
    img, img_new, data = None, None, None
    pix_raw, pix_new = [], []

    # print("\n>>>开始读取数据文件和图片...")

    try:
        path_text = r'd:\need\txt\water_long.txt'
        # path_text = r'd:\need\txt\water_0.txt'
        # path_text = r'd:\need\txt\1.txt'
        data = e.get_text(path_text)
    except IOError as e:
        print(f"没有找到文件或读取文件失败。Error is {e}")
    # else:
        # print("读取数据文件成功！")
        # print(f"前20个字符的二进制格式ASCII值为：{e.to_ascii(data)[:20]}\n"
        #       f"后20个字符的二进制格式ASCII值为：{e.to_ascii(data)[-20:]}")
        # print(f"嵌入字符串的所有的的二进制格式ASCII值为：{e.to_ascii(data)[:]}")
        # print(f"嵌入的文本内容为：{str1}")

    try:
        # path_img = r'd:\need\all_picture\new1.jpg'
        # path_img = r'd:\need\all_picture\start.jpg'
        # path_img = r'd:/pythonProjects/opencv_test/compress_img.png'
        img = cv.imread(path_raw, cv.IMREAD_UNCHANGED)
        # img = cv.imread(path_img)

    except IOError as err:
        print(f"没有找到文件或读取文件失败，图片路径不要有中文哦。Error is {err}")
    else:
        # print("读取图片成功！")
        pix_raw = e.get_pix(img, data)
        pix_new = e.encode(pix_raw, data)
        img_new = e.encode_write(img, pix_new, data)
        # path_save = r'd:/need/all_picture/new1.png'
        cv.imwrite(path_save, img_new, [cv.IMWRITE_PNG_COMPRESSION, 9])

    # return save_path_png

    '''
    测试能否恢复指定png
    '''
    # path_img_png = r'd:/need/all_picture/rec_1.png'
    # path_img_png = r'd:/need/all_picture/new1.png'
    img_new_png = cv.imread(path_save, cv.IMREAD_UNCHANGED)
    d.decode(e.to_ascii(data), img_new_png)



    # print(f"原图像素值为：{pixel[:]}")
    # print(f"修改后的像素值为：{pix_new[:]}")
    # print(f"凑字原图前160个像素值为：{pix_raw[:160]}")
    # print(f"修改后的前160个像素值为：{pix_new[:160]}\n")
    # print(f"凑字原图后160个像素值为：{pix_raw[-160:]}")
    # print(f"修改后的后160个像素值为：{pix_new[-160:]}")

    # print("\n>>>开始显示图片...")
    # cv.imshow("new", img_new)
    # # print("在这个地方卡死，程序停不下来。。。")
    # cv.waitKey(0)
    # # print("在这个地方卡死，程序停不下来。。。")
    # cv.destroyAllWindows()

    '''
    打印并保存ndarray
    '''
    # print(f"ndarray_1 is:{img_new}")
    # # 1.savetxt只能保存至多二维数组。
    # # np.savetxt('my_array')
    # # 2.savez可以保存多维数组
    # np.savez('img_array', img_new)
    # # 3.load读取
    # rec = np.load('img_array.npz')
    # print(f"ndarray_2 is:{rec['arr_0']}")

    # 恢复产生的png。该png与imwrite手动保存的png一致，也能恢复数据
    # d.decode(e.to_ascii(data), img_new)

    '''
    保存图片。可选格式和参数。
    '''
    # 默认保存路径为该python项目文件目录
    # saveFile_path = r'D:/pythonProjects/opencv_test/new.jpeg'
    # 指定保存文件的路径以及文件名（带扩展名！！）
    # saveFile_path = r'd:/need/all_picture/new.png'
    # cv.imwrite(saveFile_path, img_new)
    # 保存为png时可以设置压缩比，0-9，最大为9，越小代表压缩力度越大。water_0可达到290kb；water_long可达到301kb，不能再小了。。。
    # saveFile_path_png = r'd:/need/all_picture/new1.png'
    # cv.imwrite(saveFile_path_png, img_new, [cv.IMWRITE_PNG_COMPRESSION, 9])
    # # param2为压缩参数，数字代表压缩比例，该值范围在0-100，越小代表压缩力度越大
    # saveFile_path_jpg = r'd:/need/all_picture/new1.jpg'
    # cv.imwrite(saveFile_path_jpg, img_new, [cv.IMWRITE_JPEG_QUALITY, 98])


    # path_raw = r'd:/need/all_picture/test.jpg'
    # saveFile_path_png = r'd:/need/all_picture/new1.png'
    # saveFile_path_jpg = r'd:/need/all_picture/new1.jpg'
    # img_new = cv.imread(path_raw, cv.IMREAD_UNCHANGED)
    # cp.compress_result(path_raw, saveFile_path_png, saveFile_path_jpg, img_new)


    '''
    写个循环。当两张图片差值小于0.1kb时返回
    '''


    # tinify.key = "WcXCF4ZYlPv47h3jWG6HmTBmLZSgm7qM"
    # source = tinify.from_file(saveFile_path)
    # source.to_file("compress_img.png")

    # # 测试能否恢复jpg
    # # path_img_input = r'd:/need/all_picture/new.jpg'
    # path_img_input = r'd:/need/all_picture/new.png'
    # # path_img_input = r'd:/pythonProjects/opencv_test/compress_img.png'
    # img_new_input = cv.imread(path_img_input, cv.IMREAD_UNCHANGED)
    # # d.decode(e.to_ascii(data), img_new_input)


if __name__ == '__main__':
    pass



