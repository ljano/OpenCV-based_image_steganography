import cv2 as cv
import numpy as np
import operator
import encode as e


def decode_pre(img: np.ndarray) -> [list, list]:
	"""
	写一个函数用以跳出嵌套循环。返回两种分隔符形式的ASCII值列表
	:param img: 新图
	:return: ASCII值列表以逗号分隔：['00100011, 00100001, 00101111, ...']。作用：用来和原图ASCII值列表比较，判断是否恢复成功
			ASCII值列表以空格分隔：['00100011 00100001 00101111 ...']。作用：用于恢复原字符串数据
	"""
	data_list_comma, data_list_space = [], []

	# 遍历整个图像，直到flag为奇时返回
	while True:
		for i in range(0, img.shape[0]):
			for j in range(0, img.shape[1]):
				for k in range(0, 3):
					# 判断flag值。3行为一个周期，3种情况：
					# 第一行判flag的方法。j=3*n+2, n=0,1,2...。j0 = 2
					f1 = (i % 3 == 0) & (j % 3 == 2) & (k == 2)
					# 第二行判flag的方法。j=3*n,n=0,1,2...。j0=0
					f2 = (i % 3 == 1) & (j % 3 == 0) & (k == 2)
					# 第三行判flag的方法。j=3*n+1,n=0,1,2...。j0=1
					f3 = (i % 3 == 2) & (j % 3 == 1) & (k == 2)
					if f1 | f2 | f3:
						# 还有数据要读，前进
						if (img.item(i, j, k) % 2) == 0:
							# pass
							# 每8个像素值后添一个","作为分隔符，以便后续split操作
							data_list_comma.append(',')
							data_list_space.append(' ')
						else:
							# flag为奇数，直接return。起到跳出循环的效果
							return data_list_comma, data_list_space
					# 不读flag。其余的 偶数->0，奇数->1
					else:
						if (img.item(i, j, k) % 2) == 0:
							# 这里追加string而非int是因为后续join参数只能传入字符串列表
							data_list_comma.append('0')
							data_list_space.append('0')
						elif (img.item(i, j, k) % 2) == 1:
							data_list_comma.append('1')
							data_list_space.append('1')


def type_change(data_list: list) -> list:
	"""
	将元素类型为str的列表 修改为 每8个str为一组字符串的列表
	:param data_list: 形如['0', '0', '1', '0', '0', '0', '1', '1', ...]
	:return: 形如：['00100011', ...]
	"""

	data_rec = []
	# str1 = ""

	# 以.join前的""作为分隔符，将data_list中所有的元素（的字符串表示）合并为一个新的字符串
	try:
		str1 = "".join(data_list)
	except TypeError as err:
		print(f"join的参数应为字符串列表，而非整型或其他列表。Error is {err}")
	else:
		data_rec.append(str1)

	# 上述操作后data_rec只有一个元素，即字符串str。故可直接用data_rec[0]访问，然后用之前做的“,”标记分隔即可
	data_rec = data_rec[0].split(",")

	return data_rec


def to_str(assci_rec: list) -> str:

	# 尝试用以逗号为分隔符的assci_rec恢复出原字符串数据。问题在于int(i)结果为二进制对应的十进制值。再加一个转二进制即可
	# data_str = []
	# for i in range(0, len(data_rec)):
	# 	# print(int(i))
	# 	data_str.append(chr(int(i)))

	# 网上找到的牛逼方法，刚好能用到。明天研究下
	data_str = ''.join([chr(i) for i in [int(b, 2) for b in assci_rec[0].split(' ')]])
	return data_str


def decode(assic_raw: list, img: np.ndarray) -> str:
	"""
	解码主函数。
	:param assic_raw: 这里传入原图的ASSCI值列表仅仅是为了判断与解码得到的是否相同，无其他任何作用。
	:param img: 编码得到的图像
	:return:
	"""
	print("\n>>>开始读取新图中的像素值...")
	data_list_comma, data_list_space = decode_pre(img)
	# print(f"以逗号为分隔符的data_list_comma为：{data_list_comma}")
	# print(f"以空格为分隔符的data_list_space为：{data_list_space}")

	assci_rec_comma = type_change(data_list_comma)
	assci_rec_space = type_change(data_list_space)
	# print(f"以逗号为分隔符的assci_rec_comma为：{assci_rec_comma}")
	# print(f"以空格为分隔符的assci_rec_space为：{assci_rec_space}")

	print(f"原ASSCI值列表的长度为{len(assic_raw)}\n恢复的ASSCI值列表的长度为{len(assci_rec_comma)}")

	data_rec = to_str(assci_rec_space)
	# data_rec = to_str(assci_rec_comma)
	# print(f"为：\n{data_rec}")

	if operator.eq(assic_raw, assci_rec_comma):
		print(f"【恢复成功！】\n隐藏的数据data_rec如下：\n{data_rec}")
		# print(f"【恢复成功！】\n")
	else:
		print(f"【不匹配，恢复失败！】\n恢复的部分数据data_rec如下：\n{data_rec}")

	return data_rec


def get_rec(img_raw: np.ndarray, data: list, path_save):
	"""
	用于(3,5)门限的阈值加密模块（恢复出的txt作为其输入）。
	读取图片中隐藏的数据并将其恢复，写入txt文件中（当前项目文件目录），或者返回txt/其路径.
	:param img_raw: 仅用来显示声明图片的像素（调用shape读取其像素）
	:param data: len=5的列表。存储阈值加密中需要写入每张图片的数据。仅用作decode的输入，用于判断解码是否成功。
	:param path_save: len=5的列表。写入数据后的每张图片的存储路径
	:return:
	"""

	'''
	1. img_new_png是一个列表，存的是五张写入数据的图片
	2. data_rec是一个列表，存的是所有图片恢复的数据（5张图，每个图6行数据）。[str, str, str, str, str]
	3. rec_array是一个5*6二维数组，存的是所有的按行读出的数据。即后续阈值加密需要的输入。[[str, str...],[str, str...],...]
	'''
	# 必须显式声明个数。还不能直接*5，若更多怎么写？？？
	img_new_png = [np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]
	for i in range(5):
		img_new_png[i]: np.ndarray = np.array([[[int] * img_raw.shape[2]] * img_raw.shape[1]] * img_raw.shape[0])

	# data_rec = [str] * 5  # 若如此下面的splitlines会警告，因为类型不匹配，但不影响使用。正确方式为使用具体实例，比如字符串就用'0'，int就用0.等等
	data_rec: list[str] = [''] * 5  # 显式声明list[str]是可以省略的
	# 【方法一】利用list创建二维数组
	# rec_list: list[list[str]] = [['' for col in range(5)] for row in range(6)]
	# 【方法二】利用numpy创建二维数组
	rec_array: np.ndarray = np.array([[str] * 5] * 6)  # 这里就不能像上面一样用实例了，必须为数据类型，否则索引超界

	for i in range(5):
		img_new_png[i] = cv.imread(path_save[i], cv.IMREAD_UNCHANGED)
		# img_new_png[i] = cv.imdecode(np.fromfile(path_save[i], dtype=np.uint8), -1)  # 读中文路径
		# 一个i对应一张图。验证每一张图的数据是否写入成功，并用列表data_rec存储每一张图片恢复的数据
		data_rec[i]: str = decode(e.to_ascii(data[i]), img_new_png[i])
		for j in range(6):
			# str.splitlines()返回的是字符串str按行\n分割的长度为6的列表
			# 将每张图片的数据分割（各取
			# 【方法一】下面两行为利用list创建二维数组的索引读取方法
			# rec_list[j][i] = data_rec[i].splitlines()[j]
			# print(rec_list[j][i])
			# 【方法二】下面两行为利用numpy创建二维数组的索引读取方法
			rec_array[j, i] = data_rec[i].splitlines()[j]
			print(rec_array[j, i])
			# 将单串密文写入文件
			with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(j+1, i+1), "w") as f:
				f.write(str(rec_array[j, i]))


def get_rec_ten(img_raw: np.ndarray, data, path_save):
	"""
	用于(3,5)门限的阈值加密模块（恢复出的txt作为其输入）。
	读取图片中隐藏的数据并将其恢复，写入txt文件中（当前项目文件目录），或者返回txt/其路径.
	:param img_raw: 仅用来显示声明图片的像素（调用shape读取其像素）
	:param data: 列表。存储阈值加密中需要写入每张图片的数据。仅用作decode的输入，用于判断解码是否成功。
	:param path_save: 列表。写入数据后的每张图片的存储路径
	:return:
	"""

	# 必须显式声明个数。还不能直接*5，若更多怎么写？？？  # 逆天的解决方式，就是不能乘，我不理解。。。
	img_new_png = np.array([[np.ndarray, np.ndarray], [np.ndarray, np.ndarray], [np.ndarray, np.ndarray], [np.ndarray, np.ndarray], [np.ndarray, np.ndarray]])
	# img_new_png = np.array([[img_raw.dtype * 2] * 5])  # 牛，用type或者直接用np.ndarray都不好使。调用dtype变量解决。！！解决个屁还是得像上面那样
	# img_new_png = np.array([[np.ndarray, np.ndarray] * 5])  # 只能向上面那样枚举法声明，麻了。。
	for i in range(5):
		for j in range(2):
			img_new_png[i][j]: np.ndarray = np.array([[[int] * img_raw.shape[2]] * img_raw.shape[1]] * img_raw.shape[0])

	data_rec: np.ndarray = np.array([[str] * 2] * 5)
	rec_array: np.ndarray = np.array([[[str] * 3] * 2] * 5)  # 这里就不能像上面一样用实例了，必须为数据类型，否则索引超界

	for i in range(5):
		for j in range(2):
			img_new_png[i][j] = cv.imread(path_save[i][j], cv.IMREAD_UNCHANGED)
			# img_new_png[i] = cv.imdecode(np.fromfile(path_save[i], dtype=np.uint8), -1)  # 读中文路径
			# 一对(i,j)对应一张图。验证每一张图的数据是否写入成功，并用列表data_rec存储每一张图片恢复的数据
			data_rec[i][j]: str = decode(e.to_ascii(data[i][j]), img_new_png[i][j])
			for k in range(3):
				# 将数据读取到rec_array里
				rec_array[i, j, k] = data_rec[i][j].splitlines()[k]
				print(f"{i, j, k}的数据为{rec_array[i, j, k]}")
				# 将单串密文写入txt文件
				# with open(r"D:\pythonProjects\opencv_test\threshold\txt_temp\share_{}_{}_{}.txt".format(i+1, j+1, k+1), "w") as f:
				# 	f.write(str(rec_array[i, j, k]))
				# 按照阈值加密需要的格式写入txt文件
				n = i + 1
				if j == 0:
					m = k + 1
					with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(m, n), "w") as f:
						f.write(str(rec_array[i, j, k]))
				elif j == 1:
					m = k + 1 + 3
					with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(m, n), "w") as f:
						f.write(str(rec_array[i, j, k]))


def get_rec_fifteen(img_raw: np.ndarray, data, path_save):
	"""
	用于(3,5)门限的阈值加密模块（恢复出的txt作为其输入）。
	读取图片中隐藏的数据并将其恢复，写入txt文件中（当前项目文件目录），或者返回txt/其路径.
	:param img_raw: 仅用来显示声明图片的像素（调用shape读取其像素）
	:param data: 列表。存储阈值加密中需要写入每张图片的数据。仅用作decode的输入，用于判断解码是否成功。
	:param path_save: 列表。写入数据后的每张图片的存储路径
	:return:
	"""

	# 必须显式声明个数。还不能直接*5，若更多怎么写？？？  # 逆天的解决方式，就是不能乘，我不理解。。。
	img_new_png = np.array([[np.ndarray, np.ndarray, np.ndarray], [np.ndarray, np.ndarray, np.ndarray], [np.ndarray, np.ndarray, np.ndarray], [np.ndarray, np.ndarray, np.ndarray], [np.ndarray, np.ndarray, np.ndarray]])
	# img_new_png = np.array([[img_raw.dtype * 3] * 5])  # 牛，用type或者直接用np.ndarray都不好使。调用dtype变量解决。！！解决个屁还是得像上面那样
	# img_new_png = np.array([[np.ndarray, np.ndarray, np.ndarray] * 5])  # 只能向上面那样枚举法声明，麻了。。
	for i in range(5):
		for j in range(3):
			img_new_png[i][j]: np.ndarray = np.array([[[int] * img_raw.shape[2]] * img_raw.shape[1]] * img_raw.shape[0])

	data_rec: np.ndarray = np.array([[str] * 3] * 5)
	rec_array: np.ndarray = np.array([[[str] * 2] * 3] * 5)  # 这里就不能像上面一样用实例了，必须为数据类型，否则索引超界

	for i in range(5):
		for j in range(3):
			img_new_png[i][j] = cv.imread(path_save[i][j], cv.IMREAD_UNCHANGED)
			# img_new_png[i] = cv.imdecode(np.fromfile(path_save[i], dtype=np.uint8), -1)  # 读中文路径
			# 一对(i,j)对应一张图。验证每一张图的数据是否写入成功，并用列表data_rec存储每一张图片恢复的数据
			data_rec[i][j]: str = decode(e.to_ascii(data[i][j]), img_new_png[i][j])
			for k in range(2):
				# 将数据读取到rec_array里
				rec_array[i, j, k] = data_rec[i][j].splitlines()[k]
				print(f"{i, j, k}的数据为{rec_array[i, j, k]}")
				# # 将单串密文写入txt文件
				# with open(r"D:\pythonProjects\opencv_test\threshold\txt_temp\share_{}_{}_{}.txt".format(i+1, j+1, k+1), "w") as f:
				# 	f.write(str(rec_array[i, j, k]))
				# # 按照阈值加密需要的格式写入txt文件
				n = i + 1
				if j == 0:
					m = k + 1
					with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(m, n), "w") as f:
						f.write(str(rec_array[i, j, k]))
				elif j == 1:
					m = k + 1 + 2
					with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(m, n), "w") as f:
						f.write(str(rec_array[i, j, k]))
				elif j == 2:
					m = k + 1 + 2 + 2
					with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(m, n), "w") as f:
						f.write(str(rec_array[i, j, k]))


def get_rec_thirty(img_raw: np.ndarray, data, path_save):
	"""
	用于(3,5)门限的阈值加密模块（恢复出的txt作为其输入）。
	读取图片中隐藏的数据并将其恢复，写入txt文件中（当前项目文件目录），或者返回txt/其路径.
	:param img_raw: 仅用来显示声明图片的像素（调用shape读取其像素）
	:param data: 列表。存储阈值加密中需要写入每张图片的数据。仅用作decode的输入，用于判断解码是否成功。
	:param path_save: 列表。写入数据后的每张图片的存储路径
	:return:
	"""

	img_new_png = np.array([[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
							[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
							[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
							[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
							[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]])
	for i in range(5):
		for j in range(6):
			img_new_png[i][j]: np.ndarray = np.array([[[int] * img_raw.shape[2]] * img_raw.shape[1]] * img_raw.shape[0])

	data_rec: np.ndarray = np.array([[str] * 6] * 5)
	rec_array: np.ndarray = np.array([[str] * 6] * 5)

	for i in range(5):
		for j in range(6):
			img_new_png[i][j] = cv.imread(path_save[i][j], cv.IMREAD_UNCHANGED)
			# img_new_png[i] = cv.imdecode(np.fromfile(path_save[i], dtype=np.uint8), -1)  # 读中文路径
			# 一对(i,j)对应一张图。验证每一张图的数据是否写入成功，并用列表data_rec存储每一张图片恢复的数据
			data_rec[i][j]: str = decode(e.to_ascii(data[i][j]), img_new_png[i][j])
			# 将数据读取到rec_array里
			rec_array[i, j] = data_rec[i][j].splitlines()[0]
			print(f"{i, j}的数据为{rec_array[i, j]}")
			# 将单串密文写入txt文件
			# with open(r"D:\pythonProjects\opencv_test\threshold\txt_temp\share_{}_{}.txt".format(i+1, j+1), "w") as f:
			# 	f.write(str(rec_array[i, j]))
			# 按照阈值加密需要的格式写入txt文件
			with open(r"D:\pythonProjects\opencv_test\threshold\txt_split\share_{}_{}.txt".format(j+1, i+1), "w") as f:
				f.write(str(rec_array[i, j]))
