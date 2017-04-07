#!flask/bin/python


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import PIL
from PIL import Image
import simplejson
import traceback
from flask import Flask, request, render_template, session, redirect, url_for, flash, send_from_directory
import json
from werkzeug import secure_filename


import cv2
from lib.image_parser import parse_image
from lib.upload_file import uploadfile
from lib.es_query import get_esquery
from flask_gzip import Gzip

from elasticsearch import Elasticsearch
es = Elasticsearch("222.29.193.166:9200")
app = Flask(__name__)
#gzip = Gzip(app)


app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['DATASET_FOLDER'] = 'data/dataset'
app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg',
                          'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
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
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
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

        except Exception, e:
            print traceback.format_exc()

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            if not allowed_file(file.filename):
                result = uploadfile(
                    name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
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

        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(
            os.path.join(app.config['UPLOAD_FOLDER'], f)) and f not in IGNORED_FILES]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(
                app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


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

    image_key = request.args.get('image_key', '')

    draw_im,pedestrian_attr = parse_image(image_key)
    cv2.imwrite('./data/result.jpg', draw_im)
    # org_img=get_pedestrian_image(image_key)
    # pick=get_peason_bbox(org_img)
    # pedestrian_attr=[]
    # image_list=crop_pedestrian_image(org_img,pick)
    #
    # for img in image_list:
    #     img_info={}
    #     img_info['attr']=[]
    #     attr, _, score, _ = recognize_attr(attr_net, img, db.attr_group, threshold)
    #     for i in range(len(attr)):
    #         if attr[i]>0 or "Female"in db.attr_eng[i][0][0]:
    #             img_info['attr'].append("{0}  ------ {1}:            \
    #              {2}\n".format(db.attr_eng[i][0][0],db.attr_ch[i][0][0].encode('utf-8'),attr[i]))
    #
    #     pedestrian_attr.append(img_info)
    print pedestrian_attr
    print "fuck"
    return json.dumps(pedestrian_attr, ensure_ascii=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index_plus.html')


@app.route('/video_demo', methods=['GET', 'POST'])
def video_demo():
    return render_template('video_demo.html')

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return "pong"


@app.route('/another_demo', methods=['GET', 'POST'])
def another_demo():
    return render_template('another_demo.html')

from flask import send_from_directory


@app.route('/video/<filename>')
def get_video(filename):
    return send_from_directory("/data/peason_search_attr/static/video", filename)


@app.route('/search_frame', methods=['GET', 'POST'])
def search_frame():
    keys_str = request.args.get('tags', "")
    if keys_str:
        keys=keys_str.split(",")
    else:
        keys=[]
    gender=request.args.get('gender', "1")
    query_body=get_esquery(keys,gender)
    res = es.search(index="peason_video",
                    body=query_body)
    #image_key=request.args.get('image_key', '')
    show_time_list=[]
    peason_list = res['hits']['hits']
    for peason in peason_list:
        show_time = peason['_source']['time']
        print show_time
        show_time_list.append(show_time)
    return json.dumps(show_time_list, ensure_ascii=False)
    #show_time_list
    #render_template('another_demo.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
