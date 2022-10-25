from threshold.sharemsg import shamir, io_reader


# import shamir,io_reader


def splfile(splfilename, threshold, shares, number):
    """
    对文件进行分割
    :param splfilename:需要分割的文件名
    :param threshold: 阈值
    :param shares: 分割数量
    :param number: 正在分割第几个.cc文件
    :return:
    """
    thre = threshold
    sha = shares
    io_reader.print_shares(
        shamir.encrypt(io_reader.parse_secret(threshold, shares, splfilename), thre, sha), number)


def combinefile(threshold, shares, choosenfile, sub):
    """
    对文件进行合并
    :param threshold:
    :param shares:
    :param choosenfile:
    :return:
    """
    io_reader.print_secret(
        shamir.decrypt(io_reader.parse_shares(threshold, choosenfile, sub), threshold, shares))


if __name__ == "__main__":
    splfile(1, "secret_1.cc", 3, 5)
