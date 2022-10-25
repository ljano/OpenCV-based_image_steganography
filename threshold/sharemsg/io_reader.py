import random
import sys
from threshold.sharemsg import shamir


def decode_secret(finaldictionary):
    """
    将恢复的秘密写入文件
    :param finaldictionary:
    :return:
    """
    for key, value in finaldictionary.items():
        outrecoverfilename = "recoverfile_" + str(key) + ".cc"
        with open(outrecoverfilename, 'wb') as f:
            f.write(value.to_bytes(((value.bit_length() + 7) // 8), byteorder="big"))
            print("recover success")
    # return num.to_bytes(((num.bit_length() + 7) // 8), byteorder="big").decode("ascii")


def parse_secret(threshold, total_shares, filename):
    print('Generating shares using a ({},{}) scheme.'.format(threshold, total_shares))
    # The secret has to be smaller than the prime number
    # Since we're encoding the text as a number, with 8 bits per character,
    # we have to fit in the bit length of the chosen prime
    chosen_prime = shamir.PRIME
    prime_width = (chosen_prime.bit_length() // 8) - 1
    # data_str = input('Enter the secret, at most {} ASCII characters: '.format(prime_width))
    with open(filename, 'rb') as f:
        data = f.read()
    # data_str = int.from_bytes(data,byteorder="big")
    # if len(data_str) > prime_width:
    #     print("Error: Secret too large", file=sys.stderr)
    #     sys.exit(1)

    # encoded = encode_secret(data_str)
    encoded = int.from_bytes(data, byteorder="big")
    if encoded >= chosen_prime:
        print("Error: Secret too large", file=sys.stderr)
        sys.exit(1)

    return encoded


def parse_shares(threshold, choosenfile, sub):
    """

    :param threshold: 阈值
    :param choosenfile: 选择的文件列表
    :param sub:文件分割数量
    :return: 返回一个字典，键每个文件的编号，值 每个文件恢复的列表
    """
    mesdiction = {}
    for j in range(1, sub):
        print("Enter {} shares below:".format(threshold))
        shares = []
        for i in choosenfile:
            # 此处是选择恢复的文件，如果文件被裁剪掉了，可以使用剩下大于等于t的文件数量进行恢复
            filename = "share_" + str(j) + "_" + str(i) + ".txt"
            print("选择" + filename + "文件")
            with open(filename, 'r') as f:
                bare_share = f.read()
            # bare_share = input("Share [{}/{}]: ".format(i+1, threshold))
            matches = bare_share.split('-')
            if len(matches) != 2:
                print("Syntax Error: Bad share format")
                sys.exit(1)

            [x, y] = matches
            try:
                shares.append((int(x, 16), int(y, 16)))
            except ValueError:
                print("Syntax Error: Non-numeric share")
                sys.exit(1)
        # 每个子文件的shares
        mesdiction.update({j: shares})
    return mesdiction


def print_shares(shares, number):
    # Print as hex strings
    for x, y in shares:
        # print("{:1x}-{:2x}".format(x,y))
        filename = "share_" + str(number) + "_" + str(x) + ".txt"
        with open(filename, 'w') as f:
            f.write("{:1x}-{:2x}".format(x, y))


def print_secret(finaldictionary):
    # Convert back to a string, then print it
    print(finaldictionary)
    # print("Resulting secret: {}".format(decode_secret(secret)))
    decode_secret(finaldictionary)


def choosefile():
    pass
