[TOC]

#### **一、序**

1. 一些可能有用的概念

   - 灰度即没有色彩，RGB像素值全部相等，该值称为灰度值。

   - 灰度值指的是单个像素点的亮度。灰度值越大表示越亮

   - 灰度级表明图像中不同灰度的最大数量。灰度级越大，图像的亮度范围越大。

   - 图像分辨率是指每英寸图像内的像素点数。图像分辨率是有单位的，叫ppi（像素每英寸）。分辨率越高，像素的点密度越高，图像越逼真

   - 屏幕分辨率是屏幕每行的像素点数*每列的像素点数。屏幕分辨率越高，所呈现的色彩越多，清晰度越高。

   ```python
   # 以下两种方式等价，均是访问图片[11, 11]像素点的R像素值
   # 1.直接用opencv库方法读取
   p = img[11, 11, 2]  
   p = img[11, 11]  # 灰度图像可省略通道参数，彩色图没试过
   # 2.使用numpy库方法读取
   p = img.item(11, 11, 2)  # Care!输入参数只能为3个或1个，若为2个报错如下：
   """
   Traceback (most recent call last):
     File "D:\pythonProject\opencv_test\test\1.py", line 62, in <module>
       print(img.item(11, 11))
   ValueError: incorrect number of indices for array
   """
   
   print(p)
   
   
   
   ```

   [^疑点一]: 采用numpy库方法读取时，不导入numpy库也能读取，可能是python3.9更新了？
   [^疑点二]: `img = cv2.imread(path, cv2.IMREAD_UNCHANGED)`读取图像时若不加后面那个参数会导致`img.item（1，1，2）`与`img.item（1）`输出不一样.但好像仅限于参数为1时？

   <img src="D:\need\all_picture\用于隐藏水印的黑白图片.jpg" style="zoom: 25%;" />

2. 报错卸载重装opencv-python

   可能需要依赖opencv-contrib-python

   二者版本最好一致（目前为4.6.0.66）
   
3. `cv.imread`的路径参数一定要全英文，否则报错。



#### **二、编码方式**

1. 对数据中的每个字符，取其ASCII值，并将其转换为8位二进制。

   ```python
   # 1
   def to_ascii(text: str) -> list
   ```

2. 一次读取三个像素，总共有3 * 3 = 9个BGR值。前8个BGR值用于存储一个8位二进制（即一个字符）。

   ```python
   # 2
   def get_pix(img: np.ndarray, text: str) -> list
   ```

   > 注意，此后有两个思路：
   >
   > 1. 修改&写入同时进行：在修改像素值时同时修改图片中对应的像素值
   > 2. 修改&写入分开进行：拆分为两步，①按下面3、4先直接修改上面2中读出的列表类型的像素 ②再将4中的修改后的像素值写入图片，采用的是5中的函数

3. 根据二进制数据修改BGR值。如果二进制数字为1，则BGR值将转换为邻近的奇数，否则将转换为偶数（即均采取+1或-1或+0的操作）。

4. 第9个值用于判断是否需要读取更多像素，暂且称之为标识位flag。如果还有更多数据要读取（即编码或解码），则第9个像素变为偶数。反之若想停止进一步读取像素（即数据读完了），则将其设为奇数。

   ```python
   # 3 & 4
   def encode(pixel: list, text: str) -> list
   ```

5. 将上述修改后的像素值写入图片。

   ```python
   # 5
   def encode_write(img: np.ndarray, pixel_new: list, text: str) -> np.ndarray
   ```

##### 关于读取原图片的BGR值&将修改后的BGR值写入图片中的注解和算法

```python
# i, j定位一个像素点（i行j列）；k = [0, 1, 2]分别表示该像素点的BGR值
# 访问单个像素点的BGR值：
img.item(i, j, k)
# 修改单个像素点（i, j, k)的BGR值为pix：
img.itemset((i, j, k), pix)
# 获取行数，即一列的像素点个数(实验用图img.shape[0] = 600)
img.shape[0]
# 获取列数，即一行的像素点个数(实验用图img.shape[0] = 800)
img.shape[1]    
# 注：img.shape输出一个元组，包含三个值，依次为行数、列数、通道数（BGR图像一般都有有3个通道。灰度图像只有1个通道，理论上不会输出通道数，但实际输出还是会显示通道数为3，只不过灰度图像每个像素点的BGR值相等，自己跑个看看就知道了）
```

实验用图像素为600*800，故最大存储二进制数为 600 * 800 * 3 = 1440000，字符数=1440000/8=180000，理论上存储题目要求的py文件绰绰有余（总计3329字符再加上空格&换行也不会超过5000），**但题目的一个衡量指标是迭代次数**，即一张图片大概率是不足以存取所有数据的，猜测原因应该是我使用的这种算法可能无法满足题目的其他要求（代码写完就知道了）

> 【1016更新】确实有要求无法满足，在不考虑健壮性的前提下，图片大小于我们限制太多，这使得若达到指定大小就会使得安全性大大降低。若考虑健壮性，倒是需要五张图片。该算法的限制太多，正常应该用滤波来做或许会好一点。

```python
# 访问方式为 “从上至下，从左至右”。
# 故读取顺序依次为：(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 0)...
# 采用三层嵌套循环读取？还需要判断是否读完，否则溢出或多了均会报错。可以写个异常捕获。界限也是个问题....先用简单的文本跑通，再改代码吧...
```



#### **三、像素值存储方式**

暂且采用列表形式，其内元素类型为元组。

一个字符用一个列表存储（8+1个BGR值，即3个像素）

```python
# 弃用
[(12, 34, 65), (32, 45, 89), (23, 55, 76)]
```

##### 关于像素值输入格式问题

没有必要按照上述存储方式来输入输出。直接用一个列表存储即可。

之所以会出现上面这种存储方式是因为若采用`img[11, 11]`方式读取，会返回BGR三个像素值的元组，每个像素点再组合起来再构成一个列表。



#### **四、解码方式**

逆向编码步骤即可

1. 一次读取三个像素。

   > 前8个BGR值用于读取数据的信息（一个字符），第9个值用于判断是否继续前进。

2. 对于前8个值，如果该值为奇数，则二进制位为1，否则为0。这8位组成一个二进制串，即ASCII值，再转为对应字符即可。

3. 如果第9个值是偶数，那么将继续读取三个像素，否则停止。

```python
# 主要功能实现函数
def decode_pre(img: np.ndarray) -> [list, list]
def type_change(data_list: list) -> list
# 辅助功能函数
def to_str(assci_rec: list) -> str
# 主函数
def decode(assic_raw: list, img: np.ndarray) -> str
# 基于阈值加密的功能函数
def get_rec(img_raw: np.ndarray, data: list, path_save)
```



#### **五、一些问题（解决&未解决）**

##### 1.杂七杂八

1. <img src="D:\need\all_picture\问题1.png" alt="image-20220923205611770" style="zoom:50%;" />

   获取的像素值数要比存的二进制数多的原因：因为每三个像素点包含9个像素值，第9位是用来判断后面是否还有数据要存储的，并不存储要隐藏数据中的二进制值。可以验算一下：

   **40632 - 39144 = 1488个标识位，1488 * 8 = 11904个比特？？？？？坏了，差这么多？？还是我的计算方法有问题？**

   <原因已明确> 是因为代码本身就有问题。如果正常，理论上应有：

   ```python
   #（像素值个数-比特串长度）* 8 = 比特串长度
   # 也有可能不等，但差值一定在9以内。这个是我猜的，还没想太明白【就是如果3个3个像素点这样读，最后3个像素点不一定存的满，择日再想】
   ```

   ```python
   # 像素值个数获取方法为：
   len(pixel)
   # 比特串长度获取方法：
   len(text) * 8
   ```

2. 在新设备上我没有装opencv-python库和opencv-contrib-python库，神奇的是程序依然可以正常运行，甚至可以显示cv2库里的方法，不再像之前一样警告且无任何提示。但出现了一个新的问题，鼠标悬停无法显示函数具体解释（如下图），稍微查了下，Epydoc好像还没移植到python3里，因此应该没有什么好的解决办法。不过也不影响使用。

   <img src="D:\need\all_picture\问题2.png" alt="image-20220930162657803" style="zoom:50%;" />

   > 1.https://stackoverflow.com/questions/61976114/is-it-possible-to-change-the-way-pycharm-displays-the-opencv-documentation
   >
   > 2.https://blog.csdn.net/qq_42818011/article/details/124043311

3. 今天忽然发觉没必要把编码拆开写（我是拆成了一个修改像素值的函数encode和一个将像素值写入图片的函数encode_write），可以直接在修改像素值时顺便将其写入图片，但是按照我写的这个修改像素值的方法改起来似乎有点麻烦，懒得改了。后续有空可以优化一下。

4. 不太行，像素值虽然±1波动但为什么变化这么明显？？

   ![](D:\need\all_picture\修改后的图片1.png)

​		根据下文的分析，是因为像素值并非±1波动，所以明显，合理。

可以看到上方有很明显的横杠。。。。。而且程序显示图片后一直运行，停不下来。。。下午再		来看看。可以查查怎么debug。

​		哦对，还有个问题。我改了j后像素值和字符串值一致了。我怀疑是encode函数有问题？

```python
for j in range(0, int(col_rest / 3))  # 这里的col_rest应该要除以3
```



***重大发现，显示图片放大到一定程度后可看到每个像素点的BGR值！！！看颜色即可知对应像素值***

**① 先来看看原图的RGB值：**

<img src="D:\need\all_picture\原图RGB值.png" style="zoom: 50%;" />

> 符合灰度图像性质，且jpg与png格式的RGB值相同，经过测试，修改后的图像的BGR值也不会因为图片格式的更改而发生变化。

**② water_0.txt测试结果（3个字符/123）：**

```python
# 123
['00110001', '00110010', '00110011']
```

<img src="D:\need\all_picture\water_0测试结果.png" style="zoom: 25%;" />

<img src="D:\need\all_picture\water_0测试结果_RGB值.png" style="zoom:67%;" />

> 1. 存储方式倒没有问题，1个字符对应8个bit，存在3个像素点里（前8位）。但里面的数值有大问题。
>
> 2. 很显然，结果与算法矛盾，按照算法每个像素点的BGR值只会±1、±0变动，而图中许多像素值并非按此规则变动。而且若后续还有数据，每3个像素的第9位应该变为偶数，显然第1个157就不满足。
>
> 3. 按照算法，正确的值应该如下表所示：
>
>    |       | 0         |     1     |     2      |     3     |     4     |     5      |     6     |     7     |   8    |
>    | ----- | --------- | :-------: | :--------: | :-------: | :-------: | :--------: | :-------: | :-------: | :----: |
>    | **R** | **167/1** |   162/0   | **160/走** | **159/1** |   158/0   | **156/走** |   159/1   | **162/0** | 159/停 |
>    | **G** | 168/0     | **162/0** |   159/1    |   160/0   | **158/0** | **156/0**  | **158/0** | **162/0** | 159/1  |
>    | **B** | 168/0     | **163/1** | **160/0**  |   160/0   | **159/1** | **157/1**  | **158/0** | **163/1** | 159/1  |
>
>    表中`X/Y`为`理论值/比特值`。加粗的为测试中出现错误的值。下同。
>
>    Care! opencv的读取顺序为BGR
>
>    而`encode`函数的输出如下表所示
>
>    |       | 0     | 1     | 2      | 3     | 4     | 5      | 6     | 7     | 8      |       |
>    | ----- | ----- | ----- | ------ | ----- | ----- | ------ | ----- | ----- | ------ | ----- |
>    | **R** | 168/0 | 162/0 | 157/走 | 160/0 | 159/0 | 157/走 | 159/0 | 163/0 | 159/停 |       |
>    | **G** | 168/0 | 163/1 | 159/0  | 160/0 | 159/1 | 157/1  | 159/0 | 163/1 | 159/1  |       |
>       | **B** | None  | 167/1 | 162/0  | 160/1 | 160/1 | 159/0  | 157/0 | 159/1 | 163/0  | 157/1 |
>    
>    该表与encode_write的输出完全一致：
>    
>    <img src="D:\need\all_picture\water_0测试结果_RGB值_new.png" style="zoom: 50%;" />
>    
>       可以看到（0，0，0）点保留的是原图像素，并没有读进去，说明`encode_write`有问题。
>    
>       错位（均往前移一位）后结果为：
>    
>       |       | 0     | 1     | 2         | 3         | 4         | 5          | 6         | 7         | 8          |
>    | ----- | ----- | ----- | --------- | --------- | --------- | ---------- | --------- | --------- | ---------- |
>       | **R** | 167/1 | 162/0 | 160/走    | **160/1** | **159/0** | **157/走** | 159/1     | **163/0** | **157/停** |
>    | **G** | 168/0 | 162/0 | **157/1** | 160/0     | **159/0** | **157/0**  | **159/0** | **163/0** | 159/1      |
>       | **B** | 168/0 | 163/1 | **159/0** | 160/0     | 159/1     | 157/1      | **159/0** | 163/1     | 159/1      |
>    
>    这说明`encode_write`也有问题。

**③ water_1.txt测试结果（4个字符/1234）：**

<img src="D:\need\all_picture\water_1测试结果.png" style="zoom:45%;" />

<img src="D:\need\all_picture\water_1测试结果_RGB值.png" style="zoom:67%;" />

> 不算特别明显，但有变化，仔细看也能看出来。
>
> 可以发现像素点2的BGR值差距较大，反映在图像中（也就是第3个方块）就是很明显的淡蓝色。
>
> 而比较有代表性的像素点4的BGR值仅存在1的差值，反映在图中完全看不出来，符合图像变化的性质。

**④ water_2.txt测试结果（18个字符/123456789123456789）：**

<img src="D:\need\all_picture\water_2测试结果.png" style="zoom:35%;" />

![](D:\need\all_picture\water_2测试结果_RGB值_1.png)

![](D:\need\all_picture\water_2测试结果_RGB值_2.png)

> 开始明显了。
>
> 而且除了数值错误还出现了一个新的问题：同样是编码数据1234，像素点1的R值由162变为159，其他像素点倒没有什么问题，很奇怪。在⑤⑥测试中该问题更加严重，但**依然集中在像素点1和2上，合理推测该问题只存在于这俩像素点，至于为什么，我不理解。**

**⑤ water_3.txt测试结果（90个字符）：**

<img src="D:\need\all_picture\water_3测试结果.png" style="zoom:35%;" />

<img src="D:\need\all_picture\water_3测试结果_RGB值.png" style="zoom:50%;" />

> 很明显的变化。

**⑥ water_4.txt测试结果（909个字符，含9个换行符）：**

<img src="D:\need\all_picture\water_4测试结果.png" style="zoom:35%;" />

<img src="D:\need\all_picture\water_4测试结果_RGB值.png" style="zoom: 50%;" />

再来看一下原图的BGR值：

<img src="D:\need\all_picture\原图RGB值_2.png" style="zoom: 50%;" />

> 1. 存满了前3行，以及第4行的前24个像素点，可以看到非常明显的变化，个别点尤为严重，因为变化和差值巨大，典型的即1、2两个像素点以及第2、3行全体像素点。
>
> 2. 第3行的BGR值说明了两个问题：①`encode`有问题②`encode_write`有问题。
> 3. 第4行的BGR值说明都没动，亦能说明上述问题。



##### 2.关于输出图片大小问题的分析

- 首先是仅仅存入18个数字，图片大小由**75.4 ->345kb**，变化过大

  <img src="D:\need\all_picture\test_water_2_result.png" style="zoom: 25%;" />

- 然后存入题目要求的文本（180000个字符），图片大小变为**354kb**

  <img src="D:\need\all_picture\test_water_long_result.png" style="zoom:25%;" />

- 将上图缩小一点得到的图片大小变小，这是合理的。但是**分辨率没变，依然是800*600**，取景框大小没变的原因？（其实可以把这俩像素读出来看看...）

  <img src="D:\need\all_picture\test_water_long_result_s.png" style="zoom:25%;" />

- 根据上面数据来看一个极端例子，我直接输出原图。果然，**图片大小依然为345kb!**

  <img src="D:\need\all_picture\test_water_r_result.png" style="zoom:25%;" />

> **【结论】：**猜测是库自身使用的输出图像的编码问题，**当数据量不多时，图片大小必为345kb**；只有当数据量足够多时输出图片大小才会有少量增长，如上面的**十八万个字符，才仅仅增长了9kb**。后续可以研究下是否可以自定义输出图片或者其他输出方式，不采用opencv自带的输出方式。

- 【1004更新】opencv自身输出的图片格式为png，要修改为jpg需要**以画图方式打开**，然后另存为jpg。这样得到的jpg才是有损压缩后的，大小由**354->91.9kb**。直接修改后缀的方式是不可取的，大小不会发生变化。

  

##### 3.综上所述，问题一定出在编码上，分析如下

1. **get_pix**理论上没问题，只是正常将原图像素读取到列表。实际测试也没问题。不过他有个和算法不符的问题，即我需要的返回值为原图中所有我要存的像素值，这不仅包含我要存数据的像素值，也包含第9位的一个作前进flag的像素值。而实际代码只计算了前者，没有将flag算进去，所以这也可能是出问题的原因所在。**故第一步的任务是先把get_pix完善，让123先测试通过。**两个改进思路：①把flag也都进去就行②加点判断/标记？

   > 很对很对，改了getpix后encode输出和写入后的对上了！！！但有错位！第一个像素值没读进去，看看其他文本有没有这个问题以及是否能对上。123好像没对上来着？错位？下午看看water4是不是全队上了且错1位，同时看看flag位对不对！yeah，优化后好多了。依然存在错位+编码问题

2. **encode**有很大的问题，可能是循环的range有问题。而且如果代码没问题那么存储的*比特串长度*与*像素值个数*应该是一致的。④中提到的像素点1和2有大问题应该也是与该函数有关。甚至用123测试都不通过。明天先把123能调试通过再说。

3. **encode_write**理论上没问题，只是将encode得到的新像素值写回图片罢了，从前往后一个个写就行。不过他有个自己的问题，存在无限循环，虽然不影响显示图片，但总归不太好，想想如何解决。

4. 还需要检查一下**get_pix**和**encode_write**的range参数，确保每个for循环里的上下限是正确的。

> **【10.03更新】**`get_pix`已修复。直接把flag算进去即可
>
> **【10.04更新_encode】**发现问题：像素值列表的下标有问题。已修复。问题出在像素值下标问题、flag值置错、if条件里包含的运算符优先级未考虑到等。不得不说，debug真的好用！！！
>
> **【10.04更新_encode_write】**错位的原因在于第一轮循环没有进入itemset，后续都是正常进入。没进入的原因是最内层for的range的参数为(0, 0)。
>
> <img src="D:\need\all_picture\water_4修复结果_RGB值_1.png" style="zoom:50%;" />
>
> 错位应该是修复了，明天再测试一下。
>
> 还有俩问题：该数据只需要存4行，且第4行存不满。①第4行的像素值为什么没变？依然是原图的像素值。猜测原因1：前面`encode`返回的list还是有问题。
>
> ②第5行的像素值为什么变了？较原图数值整体降了，且一致统一全TM为131。。。
>
> **【10.05更新_encode_write】**昨天的错位原因分析的没错，问题①猜测原因错误，`encode`没有问题，是后续代码问题，最后赋值的时候搞了个循环，没有必要且错误，这会导致像素值的覆盖，同时这也是上述问题②的原因所在。此外上述问题①也已解决，是因为在写入最后一行像素时行号弄错了，赋到了下一行。debug我的超人！至此，编码部分已经全部测试通过。下面展示测试结果：
>
> *water_4.txt测试结果：*（**png, 348kb**）
>
> <img src="D:\need\all_picture\test_water_4_result_right.png" style="zoom: 33%;" />
>
> <img src="D:\need\all_picture\water_4完全修复结果_RGB值_2.png" style="zoom: 50%;" />
>
> *water_long.txt测试结果：*(**png, 354kb**)
>
> <img src="D:\need\all_picture\test_water_long_result_right.png" style="zoom:33%;" />
>
> *再对比下原图：*(**jpg, 75.4kb**)
>
> <img src="D:\need\all_picture\test.jpg" style="zoom:33%;" />
>
> **可以看到，肉眼完全看不出差别，符合我们的算法逻辑，perfect。**
>
> 再附一下water_4和water_long的**jpg**格式：**（均为92.0kb）**
>
> <div>			<!--块级封装-->
>     <center>	<!--将图片和文字居中-->
>     <img src="D:\need\all_picture\test_water_4_result_right.jpg"
>          alt="无法显示图片时显示的文字"
>          style="zoom:33%"/>
>     <br>		<!--换行-->
>     water_4测试结果_jpb	<!--标题-->
>     </center>
> </div>
>
> <div>			<!--块级封装-->
>     <center>	<!--将图片和文字居中-->
>     <img src="D:\need\all_picture\test_water_long_result_right.jpg"
>          alt="无法显示图片时显示的文字"
>          style="zoom:33%"/>
>     <br>		<!--换行-->
>     water_long测试结果_jpg	<!--标题-->
>     </center>
> </div>
>
> **【10.05更新】**关于程序停不下来的问题，是因为显示图片的两句代码：
>
> ```python
> cv.waitKey(0)
> cv.destroyAllWindows()
> ```
>
> **【10.05更新】**修改像素值列表后原图像素值列表也被修改
>
> 注意复制列表不能直接采用赋值法，否则对列表的任何修改都是永久的，无法保留原列表。
>
> ```python
> # 正确方法
> pix_new = pixel.copy()  # 等价于切片法复制：pix_new = pixel[:]
> ```
>
> **【10.05更新_decode】**只能恢复一部分。问题应该出在`decode_pre`函数的flag判断里。但是不应该啊，感觉对的很。。。
>
> water_long：
>
> <img src="D:\need\all_picture\water_long_rec_error_1.png" style="zoom: 50%;" />
>
> 测试一下water_4：
>
> <img src="D:\need\all_picture\water_4_rec_error_1.png" style="zoom: 50%;" />
>
> 来测试个极端的water_0：
>
> <img src="D:\need\all_picture\water_0_rec_error_1.png" style="zoom:50%;" />
>
> 还有个问题，jpg出大问题，无论嵌入多少都只能恢复一个字符。。。：
>
> <img src="D:\need\all_picture\rec_jpg.png" style="zoom: 50%;" />
>
> **分析：**都不能恢复，但前俩恢复的列表长度还挺接近，这肯定有问题。123都不能恢复，有大问题啊。如果jpg不是这个原因，那图片大小还真不好弄，只能压缩了。明天再来研究，争取解决。先把jpg的像素值读出来看看对不对。
>
> **【10.06更新_encode_write】**发现encode_write依然有错位问题，仅出现在存储仅需要一行的情况，给t0下标加1解决。
>
> **【10.06更新_decode】**water_0已测试通过，多次测试发现当存储仅需要一行时可以恢复png里的数据，从water_4开始就恢复不了了，可能是有上限，猜测在271左右（ASSCI值列表的长度）。而jpg恢复不了了，甚至连一个数据都恢复不了，因为他读出来的像素值都变了。
>
> ①现在先解决恢复多行Png的问题
>
> ②再解决jpg问题。（压缩）（读一下jpg，jpg的像素肯定是有问题的）
>
> **【10.06更新_decode】**这就是为什么只能读出267个字符的原因，`decode_pre`只读出了这么多个字符。然后我用`get_pix`又读了下嵌入数据后的Png，像素值是有问题，他丫的i忘改了，存第row+1行i取的row+1，应该取row，昨天只改了`encode_write`，`get_pix`没改，现在`get_pix`没问题了，但是。。。。所以问题必然出在`decode_pre`函数
>
> <img src="D:\need\all_picture\water_4_rec_error_2.png" style="zoom:50%;" />
>
> 3*90-6=264个正确的字符，也就是说前264\*3=792个像素点都没问题，第793个像素点出了问题
>
> <img src="D:\need\all_picture\water_4_rec_error_3.png" style="zoom:50%;" />
>
> 看着没有任何问题。。。
>
> <img src="D:\need\all_picture\water_4_rec_error_4.png" style="zoom:50%;" />
>
> 终于找到原因了，屮！因为在判断flag的j值时只考虑到了第一行也就是i=0的情况，详见上图。而第二行错位了，因为一行只有800个像素点，第一行的第798个像素点（j=797）的r值是最后一个flag，还剩下俩像素点，所以第二行的flag的j值与第一行的判断方法不同，且整体向左错2位，第二行第一个flag为 j=0，加的规律与第一行相同。故在（1，2，2）像素值处跳出循环返回了。
>
> 第二行倒数第二个flag为798-2=796个像素点，其 j=795，故最后一个flag的 j=798，故第三行的第一个flag的 j=1，较第一行整体向左错一位，较第二行整体向右错一位，倒数第二个flag的 j=796，最后一个flag的 j=799。
>
> 第四行的第一个flag的 j=2。好，规律出来了，三行一个周期，故加上i的判断即可。
>
> ```python
> # 第一行判flag的方法。j=3*n+2,n=0,1,2...。j0=2
> (i % 3 == 0) & (j % 3 == 2) & (k == 2)
> # 第二行判flag的方法。j=3*n,n=0,1,2...。j0=0
> (i % 3 == 1) & (j % 3 == 0) & (k == 2)
> # 第三行判flag的方法。j=3*n+1,n=0,1,2...。j0=1
> (i % 3 == 2) & (j % 3 == 1) & (k == 2)
> # 第四行判flag的方法。j=3*n,n=0,1,2...。j0=1
> (i % 3 == 0) & (j % 3 == 2) & (k == 2)
> ```
>
> ```python
> # 改后代码如下。测试通过！
> f1 = (i % 3 == 0) & (j % 3 == 2) & (k == 2)
> f2 = (i % 3 == 1) & (j % 3 == 0) & (k == 2)
> f3 = (i % 3 == 2) & (j % 3 == 1) & (k == 2)
> if f1 | f2 | f3:
> ```
>
> 至此，该代码已经彻底完成。



#### **六、下一步工作**

题目要求如下：

<img src="D:\need\all_picture\题目要求.png"  />

1. 首要任务：完成上图①，先搞清楚该要求再。。。

2. 其次：尽可能完成②，越多越好

3. 至于③暂不做考虑。



![](D:\need\all_picture\要求答复1.png)

![](D:\need\all_picture\要求答复2.png)



#### **七、图像压缩（png）**

基于jpg等有损压缩该算法无法恢复，我们只考虑png的压缩。

该章节仅为单图压缩，多图见下一章节——阈值加密。

1. 首先考虑的是opencv自带的压缩算法

   ```python
   # 保存为png时可以设置压缩比，0-9，最大为9，越大代表压缩力度越大。water_0可达到290kb；
   # water_long可达到301kb，不能再小了。。。
   saveFile_path_png = r'd:/need/all_picture/new1.png'
   cv.imwrite(saveFile_path_png, img_new, [cv.IMWRITE_PNG_COMPRESSION, 6])
   ```

   > 但最小只能到301kb，不能更小了。

2. 然后考虑使用tinify在线API压缩png

   ```python
   # 申请的密钥。一个月免费调用500次
   tinify.key = "WcXCF4ZYlPv47h3jWG6HmTBmLZSgm7qM"
   saveFile_path = r'd:/need/all_picture/new.png'
   # 从本地读取
   source = tinify.from_file(saveFile_path)
   # 默认存在当前python项目文件目录下
   source.to_file("compress_img.png")
   ```

   > 只能压缩至200kb，而且像素值改变，并非真正意义上的无损压缩。这使得数据无法恢复。其他有损压缩的API就更不用说了。

3. 更换更小的jpg作为输入

   偶然发现，如果我换一个物理内存更小的jpg作为输入，是否可以得到更小的png输出呢？试了一下还真他丫的可以，而且也能恢复。不过问题是大概在128kb就可以看到较为明显的差异，75kb就更不用谈了

   <img src="D:\need\all_picture\rec_2.png"  />

   > 从该图可以大致看到jpg的有损压缩原理。相近的色块直接统一，压缩比例越大统一程度越高。

​		反复尝试获得如下相对凑合的图：<img src="D:\need\all_picture\rec_5.png" style="zoom: 50%;" />



##### 记录一下得到某些大小的png的参数设置【单图存】

```python
# 统一参数配置
path_png_save1 = r'd:/need/all_picture/new1.png'
path_jpg_save1 = r'd:/need/all_picture/new1.jpg'
# 首先是一步opencv压缩，得到完美的301kb
# 注：i为opencv的压缩参数；j、q、s为pil的压缩参数，j为压缩目标，q为初始压缩比率，s为每次调整的压缩比率
# 然后是209kb，与301差别不大，也很不错

# (1). 119kb,rec_13.png【效果已经非常不错了】

# (2). 104kb,rec_18.png。第一轮结果.再多就炸了【效果还不错】
i=90, mb=16, q=50, s=5 
# (3). 97.0kb,rec_11.png【一般吧】

# (4). 92.4kb,rec_12.png。第一轮结果
i=50, mb=16, q=30, s=5
# (5). 91.8kb,rec_14.png。同4，第二轮结果.再多就炸了(和4一模一样)【4、5效果略逊于3】
# (6). 91.3kb,rec_17.png。第一轮结果.再多就炸了(和5一模一样)【但色块对比度没有5那么明显，效果还凑合】
i=90, mb=16, q=30, s=5 (mb到95效果都一样)
i=90, mb=15, q=50, s=5
# (7). 78.7kb,rec_21.png。【对比度比8低一点。】
i=90, mb=13, q=21, s=5
# (8). 78.1kb,rec_15.png。第一轮结果.再多就炸了
i=50, mb=16, q=20, s=5 (mb到95效果都一样)
# (9). 76.8kb,rec_16.png。第一轮结果.再多就炸了(和8一模一样)【8、9效果远逊于5，不过都是垃圾】
i=90, mb=16, q=20, s=5 (mb到95效果都一样)
i=90, mb=13, q=50, s=5
# (10). 75.6kb,rec_20.png。【与9一模一样。这多半就是最后提交的结果了】
i=90, mb=13, q=19, s=5
# (11). 74.7kb,rec_19.png。【色块分布与9一样，但对比度较9更明显一点】
i=90, mb=13, q=18, s=5
```

> 从这些结果基本可以看出压缩得到的图片大小和图片像素之间的关系了。压缩比率越大，即压缩后的文件越小，像素值的过渡越明显，即色块的断层越明显，不像压缩比率较小时过渡的那么自然。典型的可以对比观察rec_13->rec_11->rec_16。

4. 基于上述想法，尝试更换更小的png作为输入，但使用tinify得到最小的png预计可在40k左右，但出来的png达到两百多k。故得出结论：png不能作为输入，否则只会得到更大的png。只有足够小的jpg才能得到更小的png输出。

   <img src="D:\need\all_picture\rec_tini_1.png" style="zoom:50%;" />

5. 。。。【1009任务】。写个代码能稳定跑出上面71kb那种图。结果应在**75.4-79.17kb**之间。其实再小一点更好但是不太现实。

6. 一些压缩jpg的工具

   ①直接用cmd进入jpegtran.exe安装目录运行下面命令

   ```
   # 前一个jpg需要与jpegtran.exe在同一目录下。压缩结果为后一个jpg，存储在同一目录下
   jpegtran -copy none -optimize -perfect test.jpg 3.jpg
   ```

   效果不好，压缩结果：93->72kb，75->55kb

   ②再就是一些乱七八糟的软件了

   ③就python来看，PIL和opencv或许已经是最好的选择

7. 基于4有个想法，opencv能否输出存有我需要的像素的jpg，这样既能满足大小，而且还能恢复，说不定转png也能恢复？查了一下，默认输出png再输出jpg必然是经过一个png->jpg的过程，所以必然有损，寄。

   

#### **八、阈值加密**

采用的是一个(3，5)门限的阈值加密。（仅在恢复的第一阶段满足）

**数据分解过程：**原文件->1个secret.cc文件->6个secret_i.cc文件->每个secret_i.cc文件分解为5个share_i_j.txt文件。

**数据恢复过程：**对于某个i，任意3个share_i_j.txt文件恢复出一个secret_i.cc文件->集满3个i即可召唤1个recoverfile_i.cc文件->集满6个recoverfilet_i.cc文件即可恢复出1个secret.cc文件->原文件

**思路：**所有j相等的share_i_j.txt文件合并成一个txt文件，并写入一张图片，总计需要5张图片，任选3张图片可以恢复出原文件。





**一些问题：**

1. recover里的参数sub为什么是7？下标从1开始，分6份。
2. 恢复的数据存在一行space。已解决，share_all_1.txt文件末尾有空行<img src="C:\Users\Yeryo\AppData\Roaming\Typora\typora-user-images\image-20221015215110431.png" alt="image-20221015215110431" style="zoom: 67%;" />



##### 1.基于阈值加密的图像压缩参数设置【五图】

```python
# 保存后的大小部分向上取整。
# (1). 78.16kb(79),rec_1.png。垃圾
i=60, mb=12, q=21, s=5
# (2). 76.65kb(77),rec_2.png。垃圾【提交的结果】
i=90, mb=12, q=21, s=5
# (3). 84.28kb(85),rec_3.png。和之前单图78kb效果差不多，但对比度高一点
i=90, mb=13, q=21, s=5
# (4). 81.47kb(82),rec_4.png。和3差距不大，对比度再高一点
i=50, mb=13, q=21, s=5
# (5). 83.49kb(84),rec_5.png。不如3
i=50, mb=13, q=30, s=5
# (6). 75.39kb(76),rec_6.png。和2基本一样，垃圾
i=95, mb=12, q=30, s=5
# (7). 82.32kb(83),rec_7.png。和3差距不大，垃圾
i=95, mb=13, q=80, s=5
# (7_1). 89.67kb,rec_7_1.png。比7过渡自然一点，算凑合了
i=75, mb=14, q=75, s=5
# (8). 94，65kb,rec_8.png。明显优于7_1，效果拔群！【可追求的结果-在十五图中已经以87kb实现】
i=75, mb=15, q=75, s=5 
# (9). 110.76kb,rec_9.png。比8效果要好，和9相比过渡不够自然，不过已经很可以了
i=75, mb=16, q=75, s=5 (mb取17图片大小不降反增而且效果很差)
# (10). 120.10kb,rec_10.png。趋近于完美了【最好的结果】
i=75, mb=18, q=75, s=5 
# (11). 126.61kb,rec_11.png。和9基本一样，趋近于完美了
i=75, mb=19, q=75, s=5 
```

> **【1016更新】【结论】**诸多尝试已经没有更好的结果了，显然无法满足安全性需求，猜测可能是每张图嵌入数据太多（29行），之前单图是19行。现在尝试把图片数量翻一倍，每张图存29/2=14行，理论上应该可以达到之前单图压缩的效果，即安全性保证。（虽然之前的也很垃圾，不过这已经趋近极限了，再少就需要更多的图，那样图片数量过多也不行）
>
> **【1016更新】**尝试把图片数量翻一倍中...

##### 2.基于阈值加密的图像压缩参数设置【十图】

代码下标分析：

111	211	311	411	511(ijk)		1

11  	12		13	  14	  15(mn)

112	212	312	412	512(ijk)		2

21  	22		23	  24	  25(mn)

113	213	313	413	513(ijk)		3

31  	32		33	  34	  35(mn)

121	221	321	421	521(ijk)		4

41  	42		43	 44	  45(mn)

122	222	322	422	522(ijk)		5

51  	52		53	  54	  55(mn)

123	223	323	423	523(ijk)		6

61  	62		63	  64	  65(mn)

i标识n，(j,k)标识m。具体法则为：n==i，j==1时m=k，j==2是m==k+3

注意：实际下标均减一（ijk）

```python
# 【每组相近】：12一组/345一组/6一组/789一组/10一组

# (1). 76.74kb,rec_1.png。和单图78kb效果差不多，甚至好一点点（maybe错觉，对比度低一点
i=90, mb=13, q=21, s=5
# (2). 75.23kb,rec_2.png。和1一模一样【提交的结果】
i=90, mb=13, q=50, s=5
# (3). 83.04kb,rec_3.png。效果比1和2好，过度更自然，色系更细致
i=90, mb=14, q=50, s=5
# (4). 82.67kb,rec_4.png。和3一模一样
i=75, mb=14, q=50, s=5
# (5). 84.53kb,rec_5.png。对比度明显低于3和4，不过效果差的不算大
i=60, mb=14, q=50, s=5
# (6). 87.28kb,rec_6.png。明显优于5，效果拔群！【可追求的结果-在十五图中或可以79kb实现】
i=75, mb=15, q=90, s=5 (q降到50也是一样的结果)
# (7). 112.93kb,rec_7.png。趋近于完美了。【最好的结果】
i=75, mb=18, q=90, s=5 (q降到50也是一样的结果。mb取17图片大小不降反增而且效果很差)
# (8). 119.24kb,rec_8.png。趋近于完美了。效果与7相比大差不差
i=75, mb=19, q=90, s=5 (q降到50也是一样的结果，若q==50则mb可取19-30，后面没测了)
# (9). 135.22kb,rec_9.png。趋近于完美了。效果与7相比大差不差
i=75, mb=20, q=90, s=5 (mb可取到25。q降到75也是一样的结果，降至50就得到7了)
# (10). 213.57kb,rec_10.png。有一些碎点，有一种脸上长麻子的感觉。有点过于完美，在某些角度感觉上可能不如7
i=75, mb=26, q=90, s=5 (mb可取到30，后面没测了。q降到75也是一样的结果。降至50就得到7了)

# 有一点需要注意，看的角度不同可能会导致图像的亮度不同，由于我电脑右侧为窗户为进光侧，这会使得放在右边的图片显得亮一点。而且从右往左看和从左往右看的亮度也是相反的，故亮度暂不作为参考标准。
# 整体测下来，i取75是最佳选择，再小的话得到的png大小可能不降反增而且效果还不如小的。q稍微取大一点>=50，mb不要低于12，s取小一点<=5
```

> **【1016更新】**十图代码已写完，测试通过。与猜测一样，确实是因为每张图存入数据过多导致无法在满足安全性的前提下压缩至理想大小，分十图存储后，每图只需要存15行数据，小于单图时的19行，这就使得达到同一安全性时十图能比单图压缩的更小。据此可大致推断一张图存储的行数与可压缩的大小之间的关系，进一步可推断十五图甚至三十图的提升有多大，是否值得去写。

###### · 一个可以体现大致结论的表格

> **【上述推断的具体分析】**在达到同一安全性下，图片数量与压缩大小之间的关系：
>
> |                             | 单图     | 五图 | 十图 | 十五图       | 三十图      | 六十图  |
> | --------------------------- | -------- | ---- | ---- | ------------ | ----------- | ------- |
> | **一张图存储行数**          | 19       | 29   | 15   | 10左右(10)   | 5左右(5)    | 2左右   |
> | **原始大小（kb)**           | 301      | 307  | 300  | 298          | 294         | 292左右 |
> | **效果凑合的压缩大小（kb)** | 78       | 82   | 76   | 74左右(72)   | 72左右(70)  | 68左右  |
> | **效果不错的压缩大小（kb)** | (97,104) | 94   | 87   | 80左右(84)   | 72左右(81)  | 78左右  |
> | **效果完美的压缩大小（kb)** | 115      | 120  | 112  | 105左右(110) | 97左右(107) | 104左右 |
>
> 大约4行提升为2kb。可以去看一下单图在78+5kb（对应十五图）以及78+9kb（对应三十图）的效果，大致即可得知是否值得做十五图和三十图：83kb效果还不错，87kb暂时无图，除非87远好于83否则不值得一试，因为图片数量过多，十五张已经够多了。不过如果代码修改都可以整整。
>
> **【1017更新】**经过测试，推断十五图可以得到不错的效果，可以一试，若结果符合推测那么三十图不必尝试，可以直接下结论，而且以增加15次迭代次数来换取一点点安全性是并不划算的，当然这得看场景，如果安全性为第一要义那么三十图甚至六十图都是有必要的，而且根据合理推断，六十图是可以在图片大小浮动不超过5%的前提下达到完美的压缩效果的。**有一个问题**，三十图的理论推断中效果不错与效果凑合的理论大小重合了，或许三十图就可以达到完美效果？写完十五图应该就有结论了。**【1018更新】**并没有，详细结论见上表or三十图结论
>
> 注：十五图和三十图均为推测（根据单图五图十图推出的结论），括号中为测试结果；六十图为测试完前面所有的推出的结论。

##### 3.基于阈值加密的图像压缩参数设置【十五图】

提升应该在几kb



代码下标分析：

111	211	311	411	511(ijk)		1

11  	12		13	  14	  15(mn)

112	212	312	412	512(ijk)		2

21  	22		23	  24	  25(mn)

121	221	321	421	521(ijk)		3

31  	32		33	  34	  35(mn)

122	222	322	422	522(ijk)		4

41  	42		43	 44	  45(mn)

131	231	331	431	531(ijk)		5

51  	52		53	  54	  55(mn)

132	232	332	432	532(ijk)		6

61  	62		63	  64	  65(mn)

i标识n，(j,k)标识m。具体法则为：n==i，j==1时m=k，j==2是m==k+2，j==3是m==k+4

注意：实际下标均减一（ijk）

```python
# 初步压缩结果：298kb
# (1). 72.64kb,rec_1.png。和十图75kb效果差不多
i=75, mb=13, q=75, s=5
# (2). 76.91kb,rec_2.png。效果比1好，颜色更丰富，过渡比1自然【提交的结果】
i=75, mb=13, q=75, s=1 (q可取50-90)
# (3). 80.29kb,rec_3.png。和十图82.6效果差不多。比1过渡自然很多【多了1kb，麻了。。。】
i=75, mb=14, q=75, s=5 (s取1时得到4)
# (4). 84.68kb,rec_4.png。和十图87.2效果差不多。效果比1和2好，过渡更自然，色系更细致
i=75, mb=15, q=75, s=5 (q可取50-90。s取1时得到6)
# (5). 86.89kb,rec_5.png。和3一模一样
i=90, mb=15, q=50, s=5
# (6). 90.32kb,rec_6.png。效果比5好，颜色更丰富，过渡比5自然
i=75, mb=15, q=50, s=1
# (7). 100.91kb,rec_7.png。对比度比十图的112高一点，已经很不错了
i=75, mb=16, q=75, s=1 (q可取50-90，s取至5结果仍一样)
# (8). 110.41kb,rec_8.png。趋近于完美了。和十图的112一模一样【最好的结果】
i=75, mb=18, q=75, s=5 (q降到50也是一样的结果。mb取17图片大小不降反增而且效果很差)
# (9). 112.66kb,rec_9.png。趋近于完美了。细节上比8好一点，不过几乎看不出来
i=75, mb=18, q=75, s=1 
# (10). 123.22kb,rec_10.png。趋近于完美了。对比度比9低一点，更自然
i=75, mb=19, q=75, s=1 
# (11). 132.80kb,rec_11.png。和10看不出差别
i=75, mb=20, q=75, s=1 (mb取21结果一样)
# (12). 150.06kb,rec_12.png。和11看不出差别
i=75, mb=22, q=75, s=1 
# (13). 170.99kb,rec_13.png。磨砂的感觉开始明显了
i=75, mb=23, q=75, s=1 
# (14). 180.92kb,rec_14.png。细节更多，磨砂感更明显了
i=75, mb=24, q=75, s=1 (s取5得到11)
# (15). 191.79kb,rec_15.png。已经接近原图了，只是没那么细致
i=75, mb=25, q=75, s=1 (s取5得到11)
```

> **【1017更新】**十五图测试完毕，有一个问题，之前的参数s一直取的5，可能会影响结果的准确性，之后再测试一下。根据十图中的表格可以看到，对于效果不错和完美的压缩，五行数据只能提升2~3kb，效果凑合的可能提升多1~2kb。因此三十图值得一试，代码修改也不算太麻烦，只有单图转五图、五图转十图代码改起来有点麻烦。

##### 4.基于阈值加密的图像压缩参数设置【三十图】

代码下标分析：

11	21	31	41	51(ij)		1

11	12	13	14	15(mn)

12	22	32	42	52(ij)		2

21	22	23	24	25(mn)

13	23	33	43	53(ij)		3

31	32	33	34	35(mn)

14	24	34	44	54(ij)		4

41	42	43	44	45(mn)

15	25	35	45	55(ij)		5

51	52	53	54	55(mn)

16	26	36	46	56(ij)		6

61	62	63	64	65(mn)

i标识n，j标识m。具体法则为：n==i，j==m（互换）

注意：实际下标均减一（ij）

```python
# 初步压缩结果：294kb
# 
# (1). 70.12kb,rec_1.png。同十五图72kb,rec_1。垃圾
i=75, mb=13, q=75, s=5
# (2). 74.27kb,rec_2.png。同十五图76kb,rec_2。垃圾
i=75, mb=13, q=75, s=1 (q可取50-90)
# (3). 77.59kb,rec_3.png。同十五图80kb,rec_3【提交的结果】。凑合
i=75, mb=14, q=75, s=5 
# (4). 81.76kb,rec_4.png。渐入佳境
i=75, mb=14, q=75, s=1 
# (5). 81.91kb,rec_5.png。效果比4略好，看不太出来。同十五图84kb,rec_4
i=75, mb=15, q=75, s=5 
# (6). 87.52kb,rec_6.png。同十五图90kb,rec_6
i=75, mb=15, q=75, s=1
# (7). 98.06kb,rec_7.png。同十五图100kb,rec_7
i=75, mb=16, q=75, s=1
# (8). 107.58kb,rec_8.png。同十五图110kb,rec_8【最好的结果】
i=75, mb=18, q=75, s=5
# (9). 109.90kb,rec_9.png。同十五图112kb,rec_9
i=75, mb=18, q=75, s=1 (mb取17图片大小几乎不变但mb取17图片大小不降反增而且效果很差效果很差)
# (10). 120.14kb,rec_10.png。同十五图123kb,rec_10
i=75, mb=19, q=75, s=1 
# (11). 188.50kb,rec_11.png。同十五图191kb,rec_15
i=75, mb=25, q=75, s=1 
```

> **【1017更新】**三十图已经测试通过，参数测试还剩一半，十五图到三十图目前看到的提升是可提交的结果上升了一个档次，其他的明日再做分析。
>
> **【1018更新】**三十图测试完毕，可以看到相较于十五图的提升在2~3kb左右，但直接增加了十五张图片，在安全性非第一要义时，这是不划算的交换。进一步也可推测六十图的提升如十图中表格所示。



***据以上可以得到结论，安全性与迭代次数不可兼得。。。**而且牺牲迭代次数换来的安全性并不高，反映在图片大小上大约在2~3kb*

**不过有一个点可以考虑，题目虽然要求单图大小最大值为79.17kb，而基于此我们的三十图的安全性才勉勉强强合格，或许可以换一个角度，在不满足该要求的前提下，我们可以选择安全性更高的图片（100kb左右），这使得我们可以选择更小的迭代次数，或许这也是一种平衡？**



#### **九、下一步工作2**

①写一个输入图片恢复数据并验证的函数（感觉不需要，因为压缩后自带验证，要写的话也简单，直接调之前的就行），算了，懒得写了。你们有空写写吧，基本上参照decode里的函数来写就行，改改输入参数啥的。

②五图和单图的参数s可以改为1再测一测，或许能得到略好一点的结果。懒得测了

③decode的几个rec函数可以合并一下，compress_all的几个主函数也可以合并一下。懒得合并了，对于这个项目而言也不算啥太有意义的工作，只是让代码更规整，可移植性更高罢了

③剩下一些**健壮性的检测**了：

> **关于判断图像是否可恢复的大致方法为：**直接读取经过某些操作后的图片然后debug或者print就可以看到像素值，若修改格式后像素值没变就说明可以，否则不行。

- **【格式修改】**可以考虑一些无损压缩以及opencv可读取的图片格式。有最好，没有就算了。常见图片格式：https://zhuanlan.zhihu.com/p/149429406
- **【旋转】**老师的回复是旋转仍保留图像的每个部分，但是这又分两种，如果只是纯旋转那就可以恢复，如果是嵌入一张白纸里那就不行。这两点都可以写到报告里
- **【缩放】**这个简单，直接调opencv自带的缩放函数就行。理论上来讲这个是可以恢复的，不过我也不太清楚缩放原理，缩放修改的是不是图片的像素？如果是可能恢复就不太现实了。。
- **【其他方面】**建议去看看对图像的一些操作，可直接看opencv的库函数，有没有可以用的，即对图像进行某些操作后仍可恢复（体现健壮性），比如仿射变换里的平移、翻转等。尽量找点，否则咱做的这垃圾玩意要啥啥都不满足。可参考网站：opecv基础操作及例程：https://blog.csdn.net/youcans/article/details/125112487、python的仿射变换：https://www.jianshu.com/p/0231949598df



#### **十、项目总结**

##### 0.代码量

去掉未调用的python文件，代码总计约1600行，不过有约500行为相似代码（三十图、十五图、十图的代码基本相近）。

阈值加密模块未统计。

##### 1.题目原则

均已满足。

##### 2.评估点

- 迭代次数

  > 1、5、10、15、30（见下面健壮性分析）

- 安全性

  > 在满足题目原则的前提下要达到较强的安全性需要较高的迭代次数，这点如何平衡取决于实际的需求。（详细分析见前面阈值加密章节的结论与分析）

- 健壮性

  > 传输的图片数量我们可以控制在仅需要一张图片，但这会牺牲部分健壮性，比如图片受损等不可恢复，为此我们开发了五图、十图、十五图、三十图四个追加版本，并合理推测出六十图的相关结论。通过增加迭代次数（图片数量）使得即使有部分图片受损依然可恢复。采用的均为(3,5)门限，反映在十图、十五图、三十图上可损坏的图片数量分别为6、9、18，与五图版本可损坏任意两张图不同，后面三个版本对于损坏的图片是有限制的，这与数据的存储位置有关，根本原因在于多图版本采用的均为(3,5)门限的阈值加密。

  【其他方面的健壮性有待补充。。。】

##### 5.我们的优势

没有优势。编点。

##### 6.我们的劣势

哦我的天，全是劣势。在满足题目要求大小的前提下，安全性难以得到保障，健壮性也是一堆问题，迭代次数也就那样。。。。。下面主要说一下图片格式的修改问题（健壮性）

对于更改为jpg等有损压缩格式我们无能为力，因为我们的算法是通过修改原图像素值来存储的，有损压缩会合并修改像素值，关键是我们并未研究jpg有损压缩的原理，并不清楚是哪一块像素值修改了，不过从压缩结果来看可以得知opencv的jpg压缩原理主要是合并近似像素值并将其转为灰度图，这必然会导致数据无法恢复。

##### 5.可以改进的地方

- 算法主思想不变，可以考虑更改细节。比如采用分布式存储而非从头开始连续存储，具体为根据需要存储的行数结合图像的像素，将数据均匀分布在整个图像上，可能对于压缩效果有一定的提高。
- 直接更改算法，采用频域滤波处理等。。。
- 对于多图的阈值加密可以采用不同的门限，提高健壮性。
- 算法的时间复杂度较高，看着头疼，能用*的地方都没用推导式，能用推导式的地方都没用for循环，但还是不太行，有待优化。
- 暂时想不到了...

##### 6.附一下程序运行方法

a.选择迭代次数：在compress_all.py的main里选择需要跑的迭代次数，同时选择CV类里的out_png方法的迭代次数并更改参数，具体参数选择见本文档阈值加密章节。

b.然后直接跑compress_all.py就行了，得到压缩后的图片以及恢复的txt文件，对应目录可自己更改，在compress_all.py的各个迭代次数的函数里查看/更改（注意，txt的目录不要动，必须保证恢复的txt与disposefile.py在同一目录下才能正常执行disposefile.py）

c.然后跑disposefile.py，根据函数说明选择参数即可。
