# PressureSense

开发芯片：nRF52832

基于官方SDK：nRF5 SDK 15.2.0



## 开发环境

Keil uvision5

需要安装pack：NordicSemiconductor.nRF_DeviceFamilyPack.8.17.0，见`prerequisites`文件夹



## 项目与文件路径

共有三个工程项目：

- 主机项目：连接从机蓝牙，与PC串口通信传送数据
- 从机DFU项目：采集传感器数据，通过蓝牙发送至主机，可OTA DFU空中升级
- 从机无DFU项目：采集传感器数据，通过蓝牙发送至主机，不支持DFU



各个工程项目共享总SDK文件夹，不同项目的区别入口在`nRF5_SDK_15.2.0_9412b96\examples`

- 主机项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_central\serial_uart\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_central\serial_uart\pca10040\s132\arm5_no_packs`
- 从机DFU项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725_DFU\pca10040\s132\arm5_no_packs`
  - DFU相关文件：`DFU_key`
- 从机无DFU项目：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725\`
  - 工程文件：`nRF5_SDK_15.2.0_9412b96\examples\ble_peripheral\ADG725\pca10040\s132\arm5_no_packs`

