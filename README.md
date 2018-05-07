# RPI-Hardware-Wallet
基于python的硬件钱包，运行在树莓派上

## 搭建步骤
1、下载源码

    git clone https://github.com/udidi/RPI-Hardware-Wallet.git \    
2、添加自启动

    sudo nano /etc/rc.local
  在"exit 0"之前加入以下语句：

    python2 /RPI-Hardware-Wallet/signrawtransaction_beta.py &
3、根据电路图搭建硬件

4、将串口连接电脑，重启树莓派

## 硬件电路图
![image](https://github.com/udidi/RPI-Hardware-Wallet/blob/master/img/circuitry.svg)

## 依赖项
pyaltcointools：https://github.com/udidi/pyaltcointools
