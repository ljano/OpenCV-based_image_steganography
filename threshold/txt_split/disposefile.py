from threshold import hfmcode as hf
from threshold import opfile as opf
from threshold import spiltfile as spf

# func: 阈值加密恢复数据主函数


def need_hide_file(filename):
    """

    :param filename: 需要压缩的文件路径
    :return:
    """
    # 对需要隐藏的文件进行哈夫曼编码，减少文件大小
    file1 = hf.file_encode(filename)
    # 对压缩后的文件进行分割，默认按照512字节
    sub = opf.split_By_size(file1)
    # 对每个文件进行秘密分割
    for i in range(1, sub):
        spilt_filename = "secret_" + str(i) + ".cc"
        spf.splfile(spilt_filename, 3, 5, i)
    print(sub)


# 恢复出secret.py文件 没有损坏的图片list
def recover(nodamagefile, sub):
    """
    恢复文件函数
    :param nodamagefile: 没有损坏的图片列表
    :param sub: 文件分割数量（下标从1开始，分6份，故sub==7）
    :return:
    """
    # for i in (1,7):
    #     for filenumber in nodamagefile:
    # (3,5)门限
    spf.combinefile(3, 5, nodamagefile, sub)
    outfilename = opf.combine("recoverfile.cc", 7)
    hf.file_decode(outfilename)


if __name__ == '__main__':
    recover([1, 2, 5], 7)
