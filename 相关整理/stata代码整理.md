# stata代码整理
视频链接：
https://www.bilibili.com/video/BV19i4y1t7WZ/?spm_id_from=333.999.0.0

陈强老师主页：
http://econometrics-stata.com/

> 本文档主要是基于陈强老师计量经济学的课程对课程内提及的代码进行的整理

注意：文档中的举例不具备实际意义，只是实验代码的使用随意调用的参数，并没有过多关注运行效果
此外，特别注意代码块中代码中夹杂的中文是为了方便理解，比如其中的被解释变量就是对应模型的被解释变量，而表示代码就写被解释变量

---
# 1. 基础指令
## 1.1 打开文件
```stata
ues 对应路径,clear
```
使用use命令打开dta文件，其中clear用于清理内存（可以不加）
打开stata自带数据集
```stata
sysues 对应路径 //列出自带数据的目录
```
当然还可以直接制定打开的系统数据集名称
```stata
//这里以auto数据集为例，auto.dta是1978年在美国销售的74个车牌号的汽车的技术参数和价格等数据。
sysuse auto
```
## 1.2 变量管理

![image](https://github.com/user-attachments/assets/7482e2ba-4e79-49b5-9151-c7ff0bfcfd6c)

![image](https://github.com/user-attachments/assets/c2aa8f1c-f80e-40e6-8f61-6206766726f2)

> 截图自陈强老师的教学视频

**注意严格区分大小写！！！**

### 1.2.1 生成新变量
使用gen(也可以简写为g)生成新变量，感觉与python中的赋值差不多意思
```stata
gen x=log(price)
```
生成新变量常用于各种对变量的计算，特别是取对数。取对数可以帮助我们更好地解释自变量对因变量的影响，从而提高回归分析的解释效果，对数转换在回归分析中被用于以下几种情况：
```
1. 应对非线性关系：当变量之间存在非线性关系时，通过取对数可以将这种关系线性化，便于使用线性回归模型进行分析。
2. 减少斜率变化速率：对于具有非常宽范围的数据，取对数可以缩小数值范围，使得模型的斜率变化更加平滑，减小误差。
3. 提高模型稳定性：在一些情况下，数据可能存在异常值或极端值，通过取对数可以减少这些异常值对回归模型的影响，提高模型的稳定性。
```

### 1.2.2 变量重命名
使用rename可以重命名
```stata
rename 原名称 新名称
```

## 1.3 审视数据
```stata
//查看数据集中的变量名称、标签等
describe
```
还可以用将命令简写为d
运行结果：

![image](https://github.com/user-attachments/assets/5e00e6c6-804c-461e-a099-31c75d6f0105)

使用list查看具体数值                          
list 变量名1 变量名2 ...查看部分变量也可以直接list查看全部数据

![image](https://github.com/user-attachments/assets/62433df8-adc2-44ad-b8f5-6373daf01f6e)


- 滚屏显示命令运行结果：
```stata
set more off
```
- 回复分页显示：
```stata
set more on
```
|只查看前5个数据：|只查看第6-10个：|设置条件看满足条件的：|
|----|----|----|
|![image](https://github.com/user-attachments/assets/1a24094c-92b1-4b58-8e0c-6ad5f9c07ebf)|![image](https://github.com/user-attachments/assets/6be6ad4a-d86b-4243-9bc6-64b0e8a9bc62)|![image](https://github.com/user-attachments/assets/578ab018-3b6b-45ad-aa4b-4a64a9a452c6)|


## 1.4 删除
```stata
//删除满足条件的部分数据
drop if 条件
//只保留满足条件的那个部分数据
keep if 条件
```
**注意：在stata中删除数据要慎重，数据一旦删除则不能恢复**
## 1.5 排序
升序（按照提供的变量名排序）
```stata
sort 变量名
```
降序
```stata
gsort -变量名
```
## 1.6 画图
||||
|----|----|----|
|直方图：histogram|分位数图：quantile|标准化正态概率图：pnorm|
|一般绘图命令：graph或twoway|正态分布分位数图：qmorm|卡方概率图：pchi|
|对称图：symplot|QQ分位数图：qqplot|散点图：scatter|
例如：
```stata
//绘制箱线图
graph box price
```

![image](https://github.com/user-attachments/assets/7fbee195-0a9b-44bc-bb28-84b650937ac6)

而一般绘图命令：graph还可以用来绘制诸多图表
矩阵图(matrix)、折线图(line)、柱状图(bar)、饼图(pie)等
如：graph bar 变量名...
twoway命令用于在同一个图上绘制多种类型的图形，绘制时，不同的图用“||”隔开
```stata
//这里是在同一张图中绘制散点图与线性拟合（lfit），其中lp(dash)表示画虚线
twoway scatter price mpg || lfit price mpg,lp(dash)
```

![image](https://github.com/user-attachments/assets/7ef52cb2-c4dc-4bed-8e23-d1ff5d94eb78)

画图中可以在逗号后面的添加项：

||作用|使用|
|----|----|----|
|lp|定义绘制线段|如lp(dash)绘制虚线，lp(shortdash)绘制短横虚线，默认实线
|xaxis|定义x轴|如twoway scatter price mpg,xaxis(1) yaxis(1) || lfit price mpg,xaxis(2) yaxis(2) lp(dash)中xaxis(1) yaxis(1)与xaxis(2) yaxis(2)表示分别使用不同坐标|
|yaxis|定义y轴||
|xvarlab|定义标签|xvarlab(标签名称)，如graph box price,xvarlab(price)|
|ytitle|定义y轴名称|ytitle(名称)|
|xtitle|定义x轴名称|xtitle(名称)|
|title|定义图表名称|title(名称)|
|connect|（简写c）连接散点的方式|.   不连接   l   直线连接   s  平滑曲线连接       ||  直线连接在同一纵向上的两点   J  阶梯式线条连接    例：c(.)|
| symbol|(简写s)各个散点的图形|O  大圆圈       S    大方块   T   大三角型    o   小圆圈   d   小菱形        p   小加号   .     小点        例：s(O)|
```stata
twoway scatter price mpg,xtitle(X) ytitle(Y)
title(散点图) s(d)
```

![image](https://github.com/user-attachments/assets/40afebcd-4b1c-4c74-a21e-1ddc303054aa)

更多参考

https://blog.csdn.net/Ptrose/article/details/126998179

## 1.7 帮助
> 通过帮助可以了解想要使用的命令的更多情况
```stata
//如想要对了解关于graph的使用方法
help graph
```
通过help command_name还可以直接查看帮助文档

## 1.8 统计分析
### 1.8.1 特征统计
使用sum查看变量的特征统计，可以简写为su。分别表示样本容量，平均值，标准差，最小值，最大值

![image](https://github.com/user-attachments/assets/76568f25-6f91-4474-9dcd-d24c3349404f)

### 1.8.2 经验积累分布函数
通过tabulate（可以简写为ta）查看经验累积分布函数，分布表示频数，百分比，累积百分比

![image](https://github.com/user-attachments/assets/55e16adf-fe05-4173-bfef-f9d5077158db)

### 1.8.3 相关关系
- pwcorr”表示“pairwise correlation”(两两相关)
- “sig表示显示相关系数的显著性水平(即p值，列在相关系数的下方)。
- star(.05)”表示给所有显著性水平小于或等于 5%的相关系数打上星号。


## 1.9 输出结果
一、安装外部包
在Stata内安装外部包：estout和logout
```stata
ssc install estout
ssc install logout
```
二、相关命令
tabstat varlist [if] [in] [weight] [, options]
```stata
tabstat y x1 x2, stat(count mean sd max min) col(stat) format(%10.2f)
```
说明：stat表示要显示的统计量，col(stat)表示行列转置，format表示数据格式及小数点位数
logout, [options : command]
```stata
logout, save(test) excel replace: stat(count meansd max min)
```
说明：save括号内为文件名，excel可以替换为word，replace:后跟描述性统计的其他命令即可
estout [ what ] [ using filename ] [ , options ]
```stata
esttab using reg.rtf, title(reg) cells(b(star fmt(3)) t(par fmt(3)))
```
说明：输出回归结果，rtf为word可以打开的格式，title为标题，b为截距，t为t值
esttab [ namelist ] [ using filename ] [ , options ]
```stata
esttab using reg.rtf, r2 ar2 se replace nogap
```
说明：esttab为estout包内的命令，r2表示R方，ar2表示调整的R方，se表示标准误，replace表示每次替代原文件，nogap可去空格行

原文链接：

https://blog.csdn.net/Hyouka_x/article/details/123456755

## 1.10 其他
|名称|作用|用法|
|display|stata内部计算器|display 计算公式，可以通过return list查看r类命令（e类命令估计类命令以外的其他命令）的计算结果（e类命令则可以通过ereturn list显示）|
|log|stata日志|- log using 日志名称生成一个对应的.smcl日志文件 - log off暂时关闭日志(不再记录输出结果) - log on恢复使用日志 - log close彻底退出日志|
|update|更新命令库|update all|
|search|搜索|search 关键词|
|set|增加记录|set obs 30确定随机抽样的样本容量为30（增加30条空白记录） set seed 10101指定随机抽样的“种子”为10101|

---
# 2. 回归
## 2.1 一元回归
使用regress命令进行OLS最小二乘估计也就是回归（可简写为reg），使用时就是reg 变量名1 变量名2...
```stata
reg price mpg
```

![image](https://github.com/user-attachments/assets/d21f4013-9cf1-4bbe-bec0-7e093a42c933)

上图结果中，Coefficient为回归系数，_cons为常数项。一般重点关注Number of obs（样本量）、R-squared（拟合优度R方）、Coefficient（回归系数）、Std. err（标准误差）、P>|t|（P值）
分别用来观察
- Number of obs：模型样本量
- R-squared：拟合效果（**越接近1越好**），如R-squared=0.219表示模型可以解释21.9%的情况
- Coefficient：对应解释变量对被解释变量的影响（**看符号、看大小**，正则正相关；负则负相关；大小（绝对值来看）则决定对被解释变量的影响程度）
- Std. err：衡量样本均值的变动程度（**越小越好**）
- P>|t|：显著性水平（起码要小于0.1，小于0.1显著性水平10%，小于0.05显著性水平5%，**最好小于0.01**显著性水平1%）
当然，F(1, 72)（F统计量，**越大越好**），Adj R-squared（调整拟合优度R方，对模型解释变量数量的惩罚，**越接近1越好**），t（T统计量，大则拒绝原假设，小（为负）则倾向于接受原假设）也可以关注参考
> 另外，右上角MSS+RSS=TSS稍微留意，还有T统计量=Coefficient/Std. err，知道即可

- 后面加一个,noc可以去掉常数项，一般常数项是默认存在的

![image](https://github.com/user-attachments/assets/14b07fb4-fa15-455d-8605-430dd4bffb40)

- 加robust(可以简写为r)则可以得到OLS估计的稳健标准误（存在异方差的情况下使用）

## 2.2 多元回归
> 使用reg同理一元回归即可
```stata
reg price mpg rep78 headroom trunk weight length turn displacement
```

![image](https://github.com/user-attachments/assets/7a47e103-1195-46ba-a1de-a81ec35c2cf2)

使用vce显示协方差矩阵

![image](https://github.com/user-attachments/assets/51cee1bb-ce0e-4e9c-a118-8b45257c877a)

```stata
//以foreign为虚拟变量进行回归，一般用于像区分南方北方，0或1这种情况使用，如果写 ~foreign 则表示是另一部分。"~"表示否。
reg price mpg rep78 headroom trunk weight length turn displacement if foreign
```

![image](https://github.com/user-attachments/assets/80793e79-b689-49c5-87b6-753cede2d641)

这里还可以设置条件比如price>=4000，reg price mpg rep78 headroom trunk weight length turn displacement if foreign & price>=4000
- 如果想要不汇报结果进行回归则可以加quietly命令在前面（可简写为qui）
- 计算被解释变量拟合值并记为lnw1：可以输入命令predict lnw1
- 计算残差并记为e：可以输入命令predict e,residual，其中residual表示计算残差可以及简写为r（predict默认计算拟合值）
- 使用_b[变量名称]可以调用系数的估计值，比如_b[mpg]可以调用变量mpg的估计系数25.7947
- 可以使用test进行检验变量系数

## 2.3 虚拟变量
以下三张关于虚拟变量讲述的截图截取自陈强老师的课程视频
||||
|----|----|----|
|![image](https://github.com/user-attachments/assets/c4d76c91-f612-4a95-b9ae-3959788a56ef)|![image](https://github.com/user-attachments/assets/3bf24851-e4aa-4776-a0d3-58b740b66d50)|![image](https://github.com/user-attachments/assets/8ad4bdea-3907-467a-a6d4-98fa3adcb120)|


## 2.4 二值选择模型
> 二值选择模型主要是针对是或否、国内或国外、儿童或成人，类似这样的0或1数据类型的数据，由于调查问卷此种类型数据较多，可能多用于分析问卷调查数据

回归前可以先查看变量的统计特征，观察01数据的统计特征比较特殊就单独拿出来
```stata
//查看各个变量的统计特征
sum [fweight=freq]
```
这里[fweight=freq]可以实现加权计算或估计，fweight表示frequency weight（频数权重），主要是直接通过统计特征查看0或1这种类型的数据并没有太大意义，所以会考虑通过加权的方式去查看
- 还可以进一步通过条件来具体查看某一变量的具体情况
```stata
//比如有这样一组数据，考试成绩，里面的内容是合格与不合格，想要具体合格率可以这样写
sum 考试成绩 if 合格 [fweight=freq]
```

### 2.4.1 二值模型的stata命令
```stata
//probit模型
probit ,r
//logit模型
logit ,r or
```
or表示显示几率比，不显示回归系数

### 2.4.2 预测/计算准确的百分比
- 完成probit或logit估计后，可以进行预测，或计算准确的百分比
```stata
//计算发生概率的预测值并记为y1
predict y1
//计算准确预测的百分比，clas表示创建类别变量
estat clas
```

### 2.4.3 计算边际效应
- 完成估计后，可计算边际效应
```stata
//计算所有解释变量的平均边际效应；“*”表示所有解释变量
margins,dydx(*)
//计算所有解释变量在样本均值处的边际效应
margins,dydx(*) atmeans
//计算所有解释变量 在x1=0处 的平均边际效应
margins,dydx(*) at（x1=0）
//计算 解释变量x1 的平均边际效应
margins,dydx(x1)
//计算平均弹性
margins,eyex(*)
//计算平均半弹性，x变化一单位引起y变化百分之几
margins,eydx(*)
//计算平均半弹性，x变化1% 引起y变化几个单位
margins,dyex(*)
```

## 2.5 面板模型
> 面板模型顾名思义就是对面板数据进行回归的模型

面板数据特征如下：
|||
|--|--|
|![image](https://github.com/user-attachments/assets/31dc4e51-bca4-4d19-ba14-2ddd89ab17f1)|![image](https://github.com/user-attachments/assets/5a1b3b8e-631a-4ce7-8007-0c7e2175fed2)|
*——截取自陈强老师计量经济学课件*

### 2.5.1 面板数据设定
```stata
xtset panelvar timevar
```
xtset就是告诉stata数据集为面板数据
panelvar为面板（个体）变量，注意面板变量取值需要为整数且不重复，相当于将样本中每位个体进行偏好。
timevar为时间变量
举例：
```stata
//假设有这么一组面板数据：面板变量为country，其中区分有多个国家，取值为1，2，3...，代表不同国家；时间变量为year
xtset country year
//假如面板变量本来是字符串（比如国家名字）则可以使用以下命令
encode country,gen(cntry)
```
gen(cntry)表示将新生成的数字型变量记为cntey，通过变量cntey“1，2，3，...”来表示不同国家
- 显示面板数据的统计特性
```stata
//显示面板数据的结构，是否为平衡面板
xtdes
//显示组内、组间与整体的统计指标
xtsum
//对每个个体分别显示该变量的时间序列图
xtline 变量名   //如果想要将所有个体的时间序列图叠放，可以在后面加上overlay
```
### 2.5.2 混合回归
```stata
reg 被解释变量 解释变量,vce(cluster 面板变量)
//将结果储存并记为OLS
estimates store OLS
```
vce(cluster 面板变量)表示使用对应的面板变量来计算聚类的稳健标准误

### 2.5.3 固定效应
```stata
//固定效应模型（组内估计量）
xtreg 被解释变量 解释变量,fe
//记录结果并记为FE
estimates store FE

//由于未使用聚类稳健标准误，F检验并不有效，则进一步使用LSDV法考察
//LSDV法：
reg 被解释变量 解释变量 i.面板变量,vce(cluster 面板变量)
//记录结果并记为LSDV
estimates store LSDV

//一阶差分法
xtserial 被解释变量 解释变量,output
//记录结果并记为FD
estimates store FD
```
fe表示使用固定效应估计量，默认使用re表示随机效应估计量，另外，r与vce(cluster 面板变量)都是为了使用聚类稳健标准误，不加r就还多一个F检验，加了r一般结果记为FE_robust。如果F检验p值为0.0000，拒绝原假设，可以认为FE优于混合回归
i.面板变量表示根据面板变量生成虚拟变量
stata没有专门执行一阶差分法的命令，但使用xtserial ,output对组内自相关进行检验时，可附带一阶差分法的结果
> 一阶差分法（FD）的估计系数与组内估计量（FE）有一定区别，FE 比 FD 更有效率，故较少使用 FD

也可在固定效应模型中考虑时间效应，即双向固定效应(Two-way FE)，以捕捉技术进步等效应。
```stata
//为节省待估参数，首先加入时间趋势项(将估计结果记为“FE trend” ):
xtreg 被解释变量 解释变量 t,fe r
estimates store FE_trend
```
t为时间趋势项，若t不显著，主要变量的显著性不变，则加入年度虚拟变量。
```stata
//此命令将生成时间虚拟变量（这里是假设时间虚拟变量为年） year1，year2，...
tab year,gen(year)
```
进行含时间虚拟变量的双向固定效应估计(将结果记为“FE_TW” ):
```stata
xtreg 被解释变量 解释变量,fe rngca
estimates store FE_TW
```
检验所有年度虚拟变量的联合显著性:
```stata
test year2 year3 ...
```

### 2.5.4 随机效应
个体效应还可能以随机效应(RE)的形式存在
```stata
//随机效应估计的 Stata 命令为
xtreg 被解释变量 解释变量,re r theta
//将结果记为RE_robust
estimates store RE_robust
```
theta表示显示用于进行广义离差变换的θ值
对于随机效应模型，也可进行 MIE 估计
```stata
xtreg 被解释变量 解释变量,mle
//记录结果
estimates store MLE
```
究竟使用混合回归，还是个体随机效应模型，可以使用检验个体随机效应的LM检验
> 原假设为“H:σ,=0”，备择假设为“H:σ,≠0”如拒绝H，则模型中应有反映个体特性的随机扰动项u，而不应使用混合回归。也就是p值为0.0000时认为应选择“随机效应”

该LM检验的 Stata 命令为xttest0(在执行命令xtreg,re之后才能进行)。
还可以使用豪斯曼检验确认究竟使用混合回归，还是个体随机效应模型，豪斯曼检验命令：hausman FE RE,constant sigmamore（后文工具变量法处有进一步记述）
此外，随机效应模型与固定效应模型相比,前者多了“个体异质性,与解释变量不相关”的约束条件，可视为过度识别条件。
```stata
//下载安装命令 xtoverid
ssc install xtoverid   
//稳健的豪斯曼检验
xtoverid
```

### 2.5.5 组间估计量
```stata
xtreg 被解释变量 解释变量,be
```
豪斯曼检验选择了固定效应，而组间估计量仅在随机效应情况下才一致，故组间估计结果不可信。
> 根据组间估计量，如果解释变量在1%水平上显著为负，即解释变量反而对被解释变量有负作用。

将以上各主要方法的回归系数及标准误列表(为节省空间，不汇报包含年度虚拟变量的双向固定效应):
```stata
esttab OLS FE_robust FE_trend FE RE,b se mtitle
```
## 2.6 时间序列
### 2.6.1 定义时间变量
```stata
tsset 时间对应变量名  //一般是tsset year
```
tsset表示time series set，主要是告诉stata该数据集为时间序列且时间变量为year
常用时间序列算子包括滞后（lag）与差分（difference），分别以L.与D.表示，例如一阶滞后算子为L.x二阶滞后算子为L2.x，以此类推。L(1/4)则同时表示一阶至四阶滞后。差分算子同理
> 零阶滞后为当前值，一阶滞后为下一时间段，零阶差分同样为当前值，一阶差分为上一时间段

差分和滞后可以一起用LD.表示一阶差分的滞后值，DL.表示滞后值的一阶差分，两者实际上是等价的
另外，时间序列分析中可能会遇到季节效应问题，可以通过虚拟变量的形式去解决
导入时间数据时如果数据中含有格式为“1949-10-01”或“1949/10/01”的时间变量，在导入 Stata 后，可能被视为“字符串”(string)，而非“数字型”(numeric)，无法直接对其进行运算(比如，滞后一期)。
需要对这种类型的数据进行处理
```stata
//对于日度数据(daily data)，可使用如下命令转换为“整数日期变量”(integer date variable):
gen newvar=date(varname,"YMD")
//为让新的时间变量 newvar 仍以通常的日期格式(HumanReadable Format，简记 HRF)在 Stata 中显示，可输入命令:
format newvar %td
```
其中，函数date表示转换为日期变量;varname为原来的时间变量,newvar为新定义的时间变量。"YMD"告诉 Stata，原始数据的格式为“年-月-日”。如数据格式为“月-日-年”，则应为"MDY"，以此类推。如此定义后，新的时间变量 newvar 将以“整数日期”的形式显示。另外，%td中的d即表示“date’
同理有
```stata
//转换月度数据
gen newvar=monthly(varname,"YM")
format newvar %tm

//转换季度数据
gen newvar=quarterly(varname,"YQ")
format newvar %tq
```
其中，"YM"表示“年-月”格式，"YQ"表示“年-季”格式；%tm中的m即表示“month”；%tq中的q即表示“quarter’

### 2.6.2 观察时间趋势
```stata
tsline 变量,xlabel(1980(10)2010)
```
其中，tsline表示绘制时间趋势图，在此等价于命令1ine 变量 year(year 为时间变量)。xlabel(1980(10)2010)表示在横轴 1980-2010 期间，每隔 10年做个标注(1abel)，在需要时可以通过g计算生成新变量后再绘制

### 2.6.3 进一步考察
考察自相关系数使用命令corrgram 变量，corrgram就表示绘制自相关图
使用画自相关图的另一命令：
```stata
ac 变量,lags(20)
```
其中，ac表示 autocorrelation自相关;选择项1ags (20)表示画 1-20 阶的自相关图，默认的最高阶数为min{foor(n/2)-2.40},其中floor(n/2)为不超过n/2的最大整数。

![image](https://github.com/user-attachments/assets/ca6c51c3-4fdc-437f-b630-db872c6f4a52)

以截取自课程视频的上图为例，超出灰色范围的点表示对应该点的阶数自相关系数显著为零

### 2.6.4 自回归
自回归本质上就是被解释变量和解释变量都是同一个变量，可以用于预测、估计
```stata
//如仅使用2013年前数据预测2013的数据，假设要预测的变量为y取对数，时间变量为year
g lny=log(y)
reg lny l.lny if year<2013,r
//计算回归拟合值并记为dlny1
predict dlny1
//查看估计的拟合值
list dlny1 if year==2013
//计算真正的估计值
dis exp(lny[35]+dlny1[36])
//计算预测误差
dis y[36]-exp(lny[35]+dlny1[36])
```
由于假设扰动项8,无白相关，故使用异方差稳健的标准误即可，不必使用异方差自相关稳健的 HAC 标准误。
由于时使用的了取对数的方式取进行回归，所以需要通过exp()再次计算才能得出真正的估计值
lny[35]表示变量 lny 的第 35 个观测值(即 2012 年)
dlny1[36]表示变量 dlnyl 的第 36个观测值(即 2013年)

### 2.6.5 确认滞后阶数
实践中可以通过先确认一个较大的滞后阶数然后不断减小来不断进行T检验确认，或者使用信息准则，取AIC和BIC最小的对应阶数
使用信息准则确认：
```stata
//再自回归后使用,输出AIC与BIC
estat ic
```
得出AIC与BIC结果后再进行滞后操作进行回归然后再使用estat ic得出AIC与BIC结果，以此类推多重复几次操作然后进行对比确认滞后阶数
> 需要注意的是，有时候不止一个变量存在滞后问题，由此基于一定理论建立的模型往往可以节省较多时间

### 2.6.6 VAR向量自回归
> 在需要研究多个变量自回归时会需要使用VAR模型

在设定 VAR 模型时，应根据经济理论确定哪些变量在 VAR 模型中：
VAR系统包含的变量个数越多，需要估计的系数越多。
> 假设有5个变量，滞后4期，则每个方程中共有 21个待估系数(含截距项)，整个 VAR 系统共有 105 个待估系数!

待估系数过多使有效样本容量过小，增大估计误差，降低预测精度。故 VAR 模型通常仅包含少数几个变量。
- 进行VAR前先确认滞后阶数
```stata
varsoc 变量1 变量2...,maxlag(#)
//例如要考察变量y 和 d的滞后阶数则可以写为  
varsoc y d
```
varsoc命令用来计算不同滞后期的信息准则，是一个用于确定 VAR（向量自回归）模型最佳滞后阶数的统计方法，maxlag(#)表示最大滞后期（可以省略），默认值为 4。
- 确认滞后阶数后进行VAR估计
VAR 模型包含许多参数，其经济意义很难解释，故常将注意力集中于脉冲响应函数。
```stata
//假设要滞后三阶
//便捷估计
varbasic y d,lags(1/3) irf
//正式估计
var y d,lags(1/3) exog(w1 w2)
```
其中lags(1/3)表示滞后三阶，使用lags()默认滞后二阶，也就是lags(1/2)；irf（可简写为i）表示画(未正交化)脉冲响应图，默认为oirf(画正交化脉冲响应图);exog(w1 w2)（可简写为ex(w1 w2)）表示在 VAR 模型中引入外生变量wl,w2
- 检验
估计 VAR后进行检验
```stata
//LM检验（检验残差是否存在自相关）
varlmar
//通过特征值检验该 VAR系统是否为平稳过程
varstable,graph
//沃尔德检验（对每个方程以及所有方程的各阶系数的联合显著性）
varwle
//格兰杰因果检验
vargranger
```
如果所有特征值都在单位圆内部，则为平稳过程。选择项graph表示画出特征值的几何分布图。
- 储存脉冲响应结果
将有关脉冲响应的结果存为irfname(可自行命名)。
```stata
irf create irfname,set(filename) step(#) replace order(varlist)
```
set(filename)表示建立脉冲文件filename使之成为当前的脉冲文件(make filename active)，并将脉冲结果irfname存入此脉冲文件filename(若未使用选择项set(filename)指定脉冲文件，则将脉冲响应结果存入当前的脉冲文件)。step(#)表示考察截止#期的脉冲响应函数，默认为step(8)；replace表示替代已有的同名脉冲响应结果irfname(如果有)。选择项order(varlist)指定变量排序，默认使用估计VAR 时的变量排序计算正交化IRF。
> 一个脉冲文件可存储多个脉冲响应结果

- 绘制脉冲响应图
```stata
//画脉冲响应图(未正交化)
irf graph irf,impulse(varname) response(varname)
//画正交化的脉冲响应图
irf graph oirf,impulse(varname) response(varname)
```
选择项impulse(varname)用于指定脉冲变量，varname就是指定变量的名称（根据需要替换），response(varname)用来指定反应变量;默认画出所有变量的脉冲响应图。
如将以上命令中的irf graph改为irf table，则将相应信息列表而非画图。
- 预测与比较
```stata
//计算被解释变量未来#期的预测值并记为prefix
fcast compute prefix,step(#)
//将变量的预测值画图，
fcast graph varlist,observed
```
其中varlist就是要画图的各个变量选择项observed表示与实际观测值相比较。

---
# 3. 检验
## 3.1 异方差
### 3.1.1 异方差检验
#### 3.1.1.1 绘制残差图
使用rvfplot命令绘制残差图，直接使用命令是绘制残差与拟合值的散点图，rvfplot 变量名的方式则是绘制残差与对应变量的散点图
以多元回归回归结果为例，直接使用rvfplot命令绘制残差图如下：

![image](https://github.com/user-attachments/assets/a95e3d82-6510-4956-8481-9ceab23bb8d6)

分析残差图主要是：
- 关注方向：观察残差图上点的分布趋势。如果残差呈现出某种明显的模式或趋势，这表明模型可能没有很好地捕捉到数据的某些结构。
- 均匀分布：理想情况下，残差应该围绕零点均匀分布，这意味着模型很好地捕捉了数据的方差，没有系统性偏差。
- 散点分布：检查残差的散点分布。如果分布呈扇形或曲线，这 可能意味着模型过于简单，无法捕捉数据的复杂性。
- 倾斜或弯曲：观察残差的分布是否有倾斜或弯曲。这可能是由于模型选择不当（如高斯错误分布不适合数据的真实分布）。
截图自以下文章
https://www.sohu.com/a/406703172_120233365

![image](https://github.com/user-attachments/assets/74f8d9e3-5230-4eab-b456-8fbf45aeac27)

![image](https://github.com/user-attachments/assets/33a9598d-1707-4eae-99a8-be6996eba0d7)

#### 3.1.1.2 BP检验
在stata中完成回归后使用estat hettest,iid rhs进行BP检验
其中estat指post-estimation statistics估计后统计量（完成估计后所计算的后续统计量），hettest表示heteroskedasticity异方差性，iid表示仅假定数据为iid，而无需正态假定，rhs表示使用方程右边全部解释变量进行辅助回归（默认使用被解释变量的拟合值进行辅助回归）。
如果想要指定使用某些解释变量进行辅助回归，则可以使用命令estat hettest [varlist],iid。其中的[varlist]为指定的变量清单，也就是estat hettest 变量1 变量2...,iid
以多元回归那一部分的回归结果为例，进行BP检验 ->

如果Prob > chi2（即P值）都小于0.01，则强烈拒绝同方差的原假设，可以认为存在异方差

![image](https://github.com/user-attachments/assets/16f467dd-2575-4e46-8ab2-e6cc88fa7245)

BP检验最好做三步：
- 使用被解释变量拟合值进行BP检验：estat hettest,iid
- 使用所有解释变量进行BP检验：estat hettest,iid rhs
- 使用某一变量（最关键的那几个解释变量）进行BP检验：estat hettest 变量名,iid

#### 3.1.1.3 怀特检验
在stata中完成回归后使用estat imtest,white进行怀特检验
其中imtest指information matrix test（信息矩阵检验）
还是以多元回归回归结果为例

![image](https://github.com/user-attachments/assets/5bcb1b92-f636-4f55-be0b-cd026d6d499e)

与BP检验相同，主要就是关注Prob > chi2（即P值），与BP检验是一样的。如果P值为0.0000则强烈拒绝同方差的原假设，认为存在异方差

### 3.1.2 异方差处理
#### 3.1.2.1 WLS加权最小二乘法
得到扰动项方差估计值后，可以将其作为权重进行WLS估计
```stata
//首先计算残差并记为e1
qui reg price mpg rep78 headroom trunk weight length turn displacement
predict e1,r
//其次，生成残差的平方并记为e2
g e2=e1^2
//将残差平方取对数
g lne2=log(e2)
//假设turn就是扰动项方差估计值，并基于此进行辅助回归
reg lne2 turn
//如果常数项不显著则可以去掉常数项再次回归  
reg lne2 turn,noc
//计算辅助回归的拟合值并记为lne2f，计算之前先对比有无常数项的回归效果，如果有常数项效果好则再跑一次reg lne2 turn，如果没有常数项就继续
predict lne2f
//去掉对数后得出方差的估计值，记为e2f
g e2f=exp(lne2f)
//使用方差估计值的倒数作为权重进行WLS回归
reg price mpg rep78 headroom trunk weight length turn displacement [aw=1/e2f]
```
一元回归结果怎么看WLS回归结果就怎么看，需要注意的就是如果数据中存在明显异方差，使用WLS后可以提高估计效率，如果还担心条件方差函数设定不准确导致加权后的新扰动项仍有异方差的话，可以加,r使用稳健标准误再次进行WLS估计（无论是否使用稳健标准误，WLS的回归系数都相同，但标准误有所不同）

## 3.2 自相关
#### 3.2.1 自相关检验
#### 3.2.1.1 画图
完成回归后，将残差记为e1
```stata
//绘制残差与其滞后的散点图
scatter e1 L.e1
//如果想看残差自相关图（各阶自相关系数）
ac e1
```
其中，ac表示autocorrelation（自相关）

#### 3.2.1.2 BG检验
```stata
estat bgodfrey,lags(p) nomiss0
//以下为简写版:
estat bgo,l(p) nom0
```
lags(p)中的p用于指定滞后阶数，默认是lags(1)，至于如何确定滞后结束主要是要通过自相关图ac e1，看落在95%置信区间以外的区域的自相关系数，也可以直接设一个较大的值然后不停回归并减小直到最后一个系数**从显著到不显著为止**，也就是看结果主要关注P值

#### 3.2.1.3 Q检验
```stata
//将OLS残差记为e1并进行Q检验
wntestq e1,lags(p)
wntestq指white noise testQ，因为白噪声没有自相关；lags(p)指定滞后阶数，默认为min{floor(n/2)-2,40}
//另一种Q检验方式
corrgram e1,lags(p)
```

#### 3.2.1.4 DW检验
```stata
//使用命令estat dwatson可以进行DW检验，可以简写为
estat dwa
```
|||
|--|--|
|![image](https://github.com/user-attachments/assets/cb6c28fd-17bf-4282-ba50-f742ace1d723)|![image](https://github.com/user-attachments/assets/e4b50ff2-1bd6-4365-8f42-2bf8ed97f9db)|
*——两张图都截自陈强老师教学视频*

### 3.2.2 自相关处理
#### 3.2.2.1 使用“OLS+异方差自相关稳健的标准误”
> HAC稳健标准误，使用newey进行OLS估计并提供Newey-West标准误，同时通过lag(p)指定截断参数p，用于计算HAC标准误的最高滞后阶数
```stata
newey 被解释变量 解释变量1 解释变量2...,lag(p)
```

#### 3.2.2.2 准差分法
```stata
prais 被解释变量 解释变量1 解释变量2...,corc
```
corc表示使用CO估计法，默认PW估计法，在后面加一个nolog可以不显示迭代过程

#### 3.2.2.3 广义最小二乘法（GLS）
```stata
xtgls 被解释变量 解释变量1 解释变量2..., options
```
其中， options 可以包含多种选项，如指定模型的异方差性（heteroskedasticity）或自相关性（autocorrelation）。比如使用panel(het) 指定面板数据的异方差性，使用 corr(ar1) 指定一阶自相关性。或是fe 指定固定效应模型，re 指定随机效应模型。
例如xtgls 被解释变量 解释变量1 解释变量2...,corr(ar1) fe

## 3.3 对函数形式检验
在回归后进行RESET检验可以对线性模型进行检验确认是否遗漏高次项，也可以用来检验看是否应加入非线性项
```stata
estat ovtest,rhs
```
ovtest表示omitted variable test被忽略变量测试，因为遗漏高次项后果类似于遗漏解释变量；rhs表示使用解释变量的幂为非线性项，默认使用被解释变量的二次方、三次方和四次方为非线性项
> 看结果同样也是关注P值，比如为0.06则可以说明在5%的置信水平上接受“无遗漏变量”的原假设

## 3.4 多重共线性检验
为了避免挑选出来的解释变量之间高度相关而影响回归结果，需要检验多重共线性以决定是否要剔除个别高度相关的变量
```stata
estat vif
```
结果中vif值越大则多重共线性越明显，也就是VIF值越小越好，小于10则说明可以排除模型中存在多重共线性
当然，如果构建模型有取平方项的变量则很容易导致出现多重共线性，可以通过标准化平方项来缓解

## 3.5 极端值检验
在回归后通过predict lev,lev来检验数据集中是否存在极端值
```stata
//注意要回归之后才能用，记所有观测数据的影响力为lev
predict lev,lev
//统计所有观测数据影响力的特征并对比最大值与平均值的大小
sum lev
dis r(max)/r(mean)
```
如果最大值与平均值的比值较大的话说明差距大，则可能存在极端值，要考虑进行剔除，不过要注意详尽的说明，不能随意剔除

## 3.6 工具变量法
工具变量法主要通过2SLS估计呈现ivregress 2sls 被解释变量 解释变量1 解释变量2... (工具变量=工具变量1 工具变量2),r first
```stata
ivregress 2sls 被解释变量 外生解释变量1 外生解释变量2... (内生解释变量=工具变量1 工具变量2...),r first
```
- r表示使用异方差稳健的标准误
- first表示显示第一阶段的回归结果

### 3.6.1 弱工具变量检验
完成2SLS估计后，可以通过estat firststage（可简写为estat first）检验弱工具变量
在弱工具变量的情况下，LIML的小样本性质可能优于2SLS
```stata
ivregress liml 被解释变量 外生解释变量1 外生解释变量2... (内生解释变量=工具变量1 工具变量2...)
```

### 3.6.2 过度识别检验
完成2SLS估计后，可以通过
```stata
estat overid
```
进行过度识别检验
弱工具变量检验和过度识别检验主要也都是看P值
使用estat overid报错no overidentifying restrictions时表明是没有达到过度识别检验标准，可能是可用的工具变量正好识别或太少

### 3.6.3 豪斯曼检验
豪斯曼检验（Hausman Test）主要用于完成基本回归以后，检验解释变量是否内生
```stata
//储存OLS结果并记为ols
estimates store ols  //estimates可以简写为est，store可以简写为sto
ivregress 2sls 被解释变量 外生解释变量1 外生解释变量2... (内生解释变量=工具变量1 工具变量2...)
//储存上一步2SLS估计的结果并记为iv
estimates store iv
//豪斯曼检验
hausman iv ols,constant sigmamore
```
constant表示前面记录的两个估计中都包含常数项进去进行计算，sigmamore表示使用更有效率的估计量

### 3.6.4 DWH检验
由于传统豪斯曼检验不适用于异方差情形，由此产生了适用于异方差情形的“杜宾-吴-豪斯曼检验”（Durbin-Wu-Hausman Test，简称DWH），在完成2SLS估计后使用命令:
```stata
estat endogenous
```

## 3.7 ADF单位根检验
> ADF 检验也是左边单侧检验，其拒绝域只在分布的最左边。ADF 统计量的临界值也要通过蒙特卡罗模拟得到。ADF 统计量的临界值取决于真实模型(H)是否带漂移项，以及用于检验的回归方程是否含常数项或时间趋势。

ADF 检验的 Stata 命令为：
```stata
dfuller y,lags(p) regress noconstant drift trend
```
其中，选择项1ags(p)表示包含P阶滞后差分项，默认为“lags (0)”，对应于 DF 检验。选择项regress（可简写为reg）表示显示回归结果。选择项noconstant drift trend(三者最多选一项，不能并用)的含义参见右表。

![image](https://github.com/user-attachments/assets/9a78f432-c20e-4e5f-aded-25ddfa95d5a8)

> 上表截取自陈强老师计量经济学课程视频
