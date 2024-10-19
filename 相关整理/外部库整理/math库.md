math模块简介
math模块是python中用来处理常见的数学计算。
内容参考自：
https://blog.csdn.net/weixin_53372816/article/details/133434668
一、概览

暂时无法在飞书文档外展示此内容
二、详情
数学常量
math.pi 
圆周率，具体数值为3.1415926536
math.e 
自然常数e，值为2.7182818285
math.inf      
正无穷大，负无穷大为-math.inf(-∞)
math.nan    
非浮点数标记，值为NaN
数值计算函数
math.fmod(x,y)                
返回x与y的模 x mod y
math.fabs(x)       
返回x的绝对值
math.fsum([x,y,…] )           
 浮点数精确求和
 math.ceil(x)                
向上取整，返回不小于x的最小整数
 math.mod f(x)                
返回x的小数和整数部分
math.factorial(x)   
返回x的阶乘x!，如果x是小数或负数，则返回“ValueError”
math.gcd(a,b)             
返回a与b的最大公约数
math.floor(x)       
向下取整，返回不大于x的最大整数
math.frexp(x)        
x=mx2^e ,返回(m,e);当x=0时，返回(0,0,0)
math.ldexp(x,i)       
 返回x*2^i运算值，是math.frexp(x)函数的反运算
math.trunc(x)                
返回x的整数部分
math.copysign(x,y)             
x的绝对值乘以y的绝对值除y，用数值y的正负号替换数值x的正负号
math.isclose(a,b)                
比较a和b的相似性，返回True或False
math.isfinite(x)        -        
当x不是无穷大或NaN时，返回True，否则返回False
math.isinf(x)                
当x为正负无穷大时，返回True，否则返回False
math.isnan(x)                
当x是NaN时，返回Tnue，否则返回False
幂函数与对数函数相关操作
math.sqrt(x)            
返回x的平方根
math.exp(x)             
返回e的x次幂，e是自然对数
math.expml(x)         
返回e 的x次幂减1
math.pow(x,y)         
返回x的y次幂
math.log(x[,base] )   
返回x的对数值。只输入x时，返回自然对数，即Inx
math.loglp(x)     
返回1+x的自然对数值
math.log2(x)            
log2x，返回x的以2为底的对数值
math.log 10(x)  
log1ox，返回x的以10为底的对数值
三角函数相关操作
- math.sin(x)        sinx        返回x的正弦函数值
- math.cos(x)        cosx        返回x的余弦函数值
- math.tan(x)        tanx        返回x的正切函数值
- math.asin(x)        arcsinx        返回x的反正弦函数值
- math.acos(x)        arccosx        返回x的反余弦函数值
- math.atan(x)        arctanx        返回x的反正切函数值
- math.degrees(x)        -        将角度x的弧度值转换为角度值
- math.radians(x)                将角度x的角度值转换为弧度值
- math.atan2(y,x)        arctan y/x        返回y/x 的反正切函数值
其他数学操作
math.crf(x)       
 高斯误差函数，应用于概率论、统计学等领域
math.erfc(x)       
 余补高斯误差函数
math.gamma(x)  
 伽玛函数，又称欧拉第二积分函数
math.lgamma(x)  
伽玛函数的自然对数
