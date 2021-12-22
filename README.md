# PressureSense

开发芯片：nRF52832

基于官方SDK：nRF5 SDK 15.2.0



## 开发环境

Keil uvision5

需要安装pack：NordicSemiconductor.nRF_DeviceFamilyPack.8.17.0，见`prerequisites`文件夹



## 项目与文件路径

共有四个工程项目：

- 主机项目：连接从机蓝牙，与PC串口通信传送数据
- 从机含IMU数据的DFU项目：采集阵列传感器数据和IMU数据，通过蓝牙发送至主机，可OTA DFU空中升级
- 从机DFU项目：采集阵列传感器数据，通过蓝牙发送至主机，可OTA DFU空中升级
- 从机无DFU项目：采集阵列传感器数据，通过蓝牙发送至主机，不支持DFU



各个工程项目共享总SDK文件夹，不同项目的区别入口在`nRF5_SDK_15.2.0_9412b96\examples`

- 主机项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_central\serial_uart\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_central\serial_uart\pca10040\s132\arm5_no_packs`
- 从机含IMU数据的DFU项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU_IMU\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU_IMU\pca10040\s132\arm5_no_packs`
  - DFU相关文件：`DFU_key`
- 从机DFU项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU\pca10040\s132\arm5_no_packs`
  - DFU相关文件：`DFU_key`
- 从机无DFU项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725\pca10040\s132\arm5_no_packs`



## DFU文件生成

从机DFU生成key的文件夹：

- 含IMU数据从机项目：`DFU_key_IMU`
- 不含IMU数据从机项目：`DFU_key`

在对应项目生成DFU key的文件夹下，执行`make`命令可生成：

- `ADG725_output.zip`：手机DFU传送包
- `app_setting.hex`：自动运行application而非停在bootloader模式的设置文件
- `merged.hex`：将协议栈、bootloader、application和设置文件合并的HEX文件，可一步烧写到位，不必多次烧写



## 主机上位机控制器

主机默认按照UUID搜索从机，也可以在主机上位机的控制下附加名称过滤。主机上位机通过串口向主机发送控制命令。

主机上位机控制器通信API：

| 编码                      | 命令                      | 含义                                                         | 返回   |
| ------------------------- | ------------------------- | ------------------------------------------------------------ | ------ |
| 0(byte)                   | reconnect                 | 按当前配置重新连接                                           | 无     |
| 1(byte)                   | name                      | 获取在名称过滤开启时所搜索的从机名                           | 字符串 |
| 2(byte)+str               | connect name              | 发送搜索从机名并重新搜索连接到该从机（自动打开名称过滤）     | 无     |
| 3(byte)+cmd(byte)         | namefilter enable/disable | 开启/关闭名称过滤并重新连接，0表示关闭，1表示开启，如果已开启/关闭则无变化 | 无     |
| 4(byte)+protocol_id(byte) | protocol protocol_id      | 切换通信协议，0表示simple，1表示secure                       | 无     |

双方通信通过以下协议打包分帧：

- 头字节：0xEB
- 帧内容，需要转义的情况如下：
  - 原字节为0xEC，转义为0xEC + 0x00
  - 原字节为0xEB，转义为0xEC + 0x01
  - 原字节为0xED，转义为0xEC + 0x02
- 尾字节：0xED



