行人属性分析
===================

## 依赖

###cudnn

sudo nvidia-docker run -v /home/chenxinyuan/data:/data -it nvidia/cuda:cudnn3-devel bash

环境初始化脚本 init.sh
###子项目


1. 行人属性分析 [peason_attr](https://github.com/aquairus/peason_attr)
2. 行人结构分析 [frcnn](https://github.com/rbgirshick/py-faster-rcnn)

###web:

built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/)

###图像处理：
opencv and pil

###图片索引
elasticsearch on docker

#流程

0. picture
1. hog+svm
2. layout & attrbute
3. return picture with annoation+attr

##部署
0. 安装依赖、训练模型
1. python build_index.py
2. python app.py

##演示
1.index 上传有行人人的图片，返回行人属性

2.video_de填写表单，返回行人出现时间
