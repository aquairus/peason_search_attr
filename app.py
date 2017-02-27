#!flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
import PIL
from PIL import Image
import simplejson
import traceback
from flask import Flask, request, render_template, session, redirect, url_for, flash, send_from_directory
import json
from werkzeug import secure_filename


model_path ="/data/Weakly-supervised-Pedestrian-Attribute-Localization-Network/lib"
caffe_path ="/data/Weakly-supervised-Pedestrian-Attribute-Localization-Network"
import sys
sys.path.append(model_path)
sys.path.append(caffe_path)

import caffe
from wpal_net.recog import recognize_attr
from utils.rap_db import RAP
import cv2
import numpy as np

par_set_id=0
db_path="/data/RAP"
db = RAP(db_path, par_set_id)
img_path=db.get_img_path(1)

threshold = np.ones(db.num_attr) * 0.5

net_dir="/data/Weakly-supervised-Pedestrian-Attribute-Localization-Network"
caffemodel=net_dir+"/data/snapshots/VGG_S_MLL_RAP/0/RAP/vgg_s_mll_rap_iter_100000.caffemodel"
prototxt=net_dir+"/models/VGG_S_MLL_RAP/test_net.prototxt"
net = caffe.Net(prototxt, caffemodel, caffe.TEST)
net.name = "rap_test"

from lib.upload_file import uploadfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['DATASET_FOLDER'] = 'data/dataset'
app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])




def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


def create_thumbnai(image):
    try:
        basewidth = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        print traceback.format_exc()
        return False


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files.values()[0]

        except Exception,e:
            print traceback.format_exc()

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type


            if not allowed_file(file.filename):
                result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_file_path)

                # create thumbnail after saving
                if mimetype.startswith('image'):
                    create_thumbnai(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)


            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [ f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


# @app.route("/delete/<string:filename>", methods=['DELETE'])
# def delete(filename):
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
#
#     if os.path.exists(file_path):
#         try:
#             os.remove(file_path)
#
#             if os.path.exists(file_thumb_path):
#                 os.remove(file_thumb_path)
#
#             return simplejson.dumps({filename: 'True'})
#         except:
#             return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)

@app.route("/data/dataset/<string:filename>", methods=['GET'])
def get_dataset(filename):
    return send_from_directory(os.path.join(app.config['DATASET_FOLDER']), filename=filename)



@app.route('/search_image', methods=['GET', 'POST'])
def search_image():
    # index_file='data/index.csv'
    image_key=request.args.get('image_key', '')
    img = cv2.imread(image_key)
    attr, _, score, _ = recognize_attr(net, img, db.attr_group, threshold)
    # if not os.path.exists(index_file):
    #     lib.index.build_index(index_file,'data/dataset')
    # result_file=lib.search.image_search(image_key,index_file,cnt=30)
    return json.dumps([{"attr":attr},{"attr_eng":db.attr_eng},{"attr_chinese":db.attr_ch}])



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index_plus.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
