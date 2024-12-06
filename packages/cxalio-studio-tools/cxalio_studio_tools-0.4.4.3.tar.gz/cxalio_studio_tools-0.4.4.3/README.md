# cxalio-studio-tools

## 介绍

这是一套用于简化影视后期工作的脚本合集。

涉及各种繁复的资料处理工作，解放双手，减少出错。

## 安装

```shell
pip --install cxalio-media-tools

#推荐使用 pipx 安装
pipx --install cxalio-media-tools
```

## 包含的工具

### MediaKiller

MediaKiller 可以通过配置文件操纵 ffmpeg 批量地对大量媒体文件转码，
仅支持单文件输入，可以保留源文件的目录层级。
请查看[具体说明](src/media_killer/help.md)

### SubConv

subconv 是一个批量从字幕文件提取台词本的工具。
请查看[具体说明](src/sub_conv/help.md)

### Jpegger

Jpegger 是一个批量转换图片格式的工具。请查看[具体说明](src/jpegger/help.md)

### BatchCommander

BatchCommander 是一个使用命令批量处理文件的工具。请查看[详细说明](src/batch_commander/help.md)

### update_githubhosts

一个自动更新hosts的小工具

## To-do

- media-inspector 解析媒体信息

## Change-log

### 0.4.4.3

- 修复了可有可无的bug

### 0.4.4.2

- 修正 MediaKiller 探测媒体出错可能导致失败的问题
- MediaKiller 可以识别未指定扩展名的输入是否为配置文件

### 0.4.4

- 为 MediaKiller 增加文件长度缓存特性

### 0.4.3
- 修正了MediaKiller中的重大Bug
- MediaKiller 中，当前任务执行出错会跳过而非中断
- 为 MediaKiller 增加了继续模式，将会提前检测已完成的任务并跳过
- 重新整理了 MediaKiller 主要流程的代码结构
- 增加了媒体时长计算器，总体进度现在按照时长计算，更精准
- batchcommander 重命名为 **batman**
- jpegger 现在可以使用小写方式指定文件格式了

### 0.4.0
- 重新编写了MediaKiller，原来的版本保存为`media_killer_legacy`

### 0.3.7
- 修复了 subconv 解析源文件目录时的一大bug

### 0.3.6
- 修复了 mediakiller 目标文件夹无法使用标签的bug

### 0.3.4

- 增加了 batchcommander 工具
- 增加了为包含空格的路径信息增加引号的功能

### 0.3.2

- 移除了 PathExpander 中解析glob的功能
- 为 jpegger 和 subconv 添加了解析glob的功能

### 0.3.1

- 为 jpegger 提供保留上级目录的功能
- 修复了 jpegger 中一个文件转换失败时直接结束的bug
- ~~尝试为 PathExpander 提供解析 glob 的功能~~

### 0.3.0

- 新工具 jpegger
- 修改了 subconv 帮助文件中的错误内容
- 增加了 cx_image 模块

### 0.2.8

- 强制扩展名按小写判断，不再区分大小写

### 0.2.7

- 为 mediakiller 增加忽略默认白名单的功能
- 为 mediakiller 增加自定义表引用的功能

### 0.2.6

- 统一设计可迭代的 PathExpander 代替 FolderExpander
- 重新构造更健壮的 subconv
- 更新 mediakiller 的逻辑与结构
- 修改了cx_core库的结构，优化了全部代码
- 优化了 mediakiller 和 subconv 的状态显示布局
- 修复了 mediakiller 无数值选项传递失败的 bug
- 为 subconv 增加了备选翻译方案

### 0.2.5

mediakiller:

- 修复了 duration 无法解析时崩溃的 bug。
- 修复了目标目录解析为当前目录的错误。
- 增加了扩展名检查，强制生成的配置文件扩展名为`toml`。
- 修改了当前任务进度条的样式，减少闪烁。
- 修复了不可覆盖输出文件时，转码卡住的问题。

subconv:

- 增加了强制设置读取文件编码的选项。

### 0.2.0

重新构建现有工具。

#### MediaKiller

- 增加了标签替换系统
- 增加了任务模块，统一转码和脚本生成功能
- 修改配置文件，分开输入和输出两部分，并且`input`和`output`现在是表数组了。这样就支持了多个文件的输入和输出。
- 大幅优化内存占用和性能
- 大幅调整调试信息

