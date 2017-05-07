监控视频行人属性分析系统
===================


## 介绍

本系统从视频中取帧，检测图片帧中的行人，对其进行属性分析，提取出结构化信息。然后对图片帧进行索引，达到通过属性搜索行人的效果



## 依赖
处于隔离环境，方便迁移的考虑。本系统运行在docker 容器中。
下面是初始化环境的一些依赖

### cudnn



sudo nvidia-docker run -v /home/chenxinyuan/data:/data -it nvidia/cuda:cudnn3-devel bash

-v 指定docker容器所挂载的本地文件夹，其中存放了了系统源代码。包括系统的http服务代码和用于属性分析、结构定位的两个子项目。

环境初始化脚本 script/init.sh  会安装一些系统运行所需的依赖库


### 子项目


1. 行人属性分析 [peason_attr](https://github.com/aquairus/peason_attr)

本项目用caffe训练行人属性分析网络，输入图片输出多项行人属性信息。在系统运行之前，请训练好相应的模型，详情请戳链接。

2. 行人结构分析 [frcnn](https://github.com/rbgirshick/py-faster-rcnn)

本项目在faster－rcnn上略做修改，用[rap dataset](http://rap.idealtest.org)数据集训练用模型，用于分别定位行人的头部，上身，下身。获取数据集请戳以上链接。数据集需要转换格式才能用于faster rcnn的模型训练，格式转换代码位于script/rap_2_voc.py。转换完之后faster rcnn也有个别参数需要调整。

### web:

本项目的http服务利用了flsk 作为web 框架，另外用了jquery-upload 作为前端文件上传控件，videojs用于视频播放控制

built on Python Flask , [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) and [videojs](https://github.com/videojs/video.js)

### 图像处理：
本项目的一些基础图像操作用到了opencv 、 pil 和 imutils 

### 图片索引

本项目使用 elasticsearch 储存索引，这里简单的用 elasticsearch 的官方docker镜像起了一个服务

docker run -it -p 9200:9200 elasticsearch


## 项目结构
本项目的基本项目是flask的默认结构，template中有网页模板，static中存放静态文件。

lib中包含了分析图片行人属性，在视频中查询行人的函数，这些功能主要通过调用两个子项目实现。

app.py 是启动http 服务的脚本,包含了各个路由函数,buiid_index.py 是分析视频建立视频索引的脚本

下面给出lib 中文件的一些介绍

目录 | 简介 | 
------------ | ------------- |
attr_net | 输入单个行人图片，调用属性分析网络，返回行人属性 | 
dehaze_lib| 实现了暗通道去雾算法，用于图片预处理|
image_parser|输入整张图片，返回所有行人属性|
es_query|用于建立索引，查询索引|
obj_detetor| 用hog svm 定位原始图片中的行人，将行人裁剪处理啊| 
peason_layout| 输入单个行人图片，调用rcnn网络，进行行人结构分析
upload_file| 用于图片，视频上传

# 流程
图片的分析流程如下，首先输入整张图片，然后切分图片中的行人，对行人进行属性和结构分析，返回整张图片的信息，建立索引。

0. picture
1. hog+svm
2. layout & attrbute
3. return picture with annoation+attr

## 部署

0. 安装依赖、训练模型
1. 建立视频索引 python build_index.py
2. 启动web服务 python app.py

## 演示

有两个页面可用于展示

1.index 上传有行人的图片，可以返回行人属性标注后的图片。

2.video_demo  填写表单，返回行人出现时间,通过行人出现时间定位视频的图片帧。
