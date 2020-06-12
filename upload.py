import flask, os, sys,time
from flask import request,render_template,send_file,Flask
import subprocess
from shutil import copyfile
import textrank
import FSM

app = Flask(__name__, static_folder='pdf')

def html_and_txt(file_name):
    path = os.getcwd().replace('\\','/') + '/pdf'
    cmd_docker = 'docker run -idt --rm -v {}:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 {}.pdf'.format(path,file_name)
    subprocess.call(cmd_docker)
    subprocess.call(cmd_docker)
    subprocess.call('python pdf2txt.py -o ./pdf/{}.txt ./pdf/{}.pdf '.format(file_name,file_name))

interface_path = os.path.dirname(__file__)
sys.path.insert(0, interface_path)  #将当前文件的父目录加入临时系统变量


@app.route('/', methods=['get'])
def index():
    return '<form action="/upload" method="post" enctype="multipart/form-data"><input type="file" id="img" name="img"><button type="submit">上传</button></form>'

@app.route('/upload', methods=['post'])
def upload():
    fname = request.files['img']  #获取上传的文件

    if fname:
        # t = time.strftime('%Y%m%d%H%M%S')
        new_fname = r'pdf/' + fname.filename
        fname.save(new_fname)  #保存文件到指定路径
        # 生成html和txt
        html_and_txt(fname.filename[:-4])
        # 得到关键字
        words_list = textrank.words(fname.filename[:-4])
        # 生成高亮html
        FSM.light(words_list,fname.filename[:-4])
        return send_file('./pdf/{}.html'.format(fname.filename[:-4]))
    else:
        return '{"msg": "请上传文件！"}'
# print('----------路由和视图函数的对应关系----------')
# print(server.url_map) #打印路由和视图函数的对应关系
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=9500, debug=True)