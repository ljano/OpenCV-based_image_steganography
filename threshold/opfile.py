import os


# filename = "secret.cc"  # 需要进行分割的文件，请修改文件名
# size = 512  #按照字节进行分割


def mk_SubFile(srcName, sub, buf):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('正在生成子文件: %s' % filename)
    with open(filename, 'wb') as fout:
        fout.write(buf)
        return sub + 1


def split_By_size(filename, size=512):
    with open(filename, 'rb') as fin:
        buf = fin.read(size)
        sub = 1
        while len(buf) > 0:
            sub = mk_SubFile(filename, sub, buf)
            buf = fin.read(size)
    print("split ok")
    return sub


def combine(srcname, sub):
    # [des_filename, extname] = os.path.splitext(srcname)
    # bytes = []
    outfilename = "secret.cc"
    with open(outfilename, 'wb') as outf:
        for i in range(1, sub):
            [des_filename, extname] = os.path.splitext(srcname)
            filename = des_filename + '_' + str(i) + extname
            print('正在合并子文件: %s' % filename)
            with open(filename, 'rb') as f:
                bytes = f.read()
                outf.write(bytes)
    print("combine ok")
    return outfilename
    # outfilename = "secret2.cc"
    # with open(outfilename,'wb') as f:
    #     f.write(bytes)

# if __name__ == "__main__":
#     sub = split_By_size(filename, size)
#     # combine("secret.cc",13)
#     # # print(sub)
