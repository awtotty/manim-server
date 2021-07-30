from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS

from manim_parser import generate_manim_file

import os
import subprocess
import shutil
import pickle
import time

# configuration
DEBUG = False

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/manim/<vid_id>', methods=['GET', 'POST'])
def manim(vid_id=None):
    if vid_id is None: 
        return jsonify("You didn't send a valid id to the server") 

    # store new vid data
    if request.method == 'POST': 
        anim_data = request.get_json()
        save_anim_data(vid_id, anim_data)
        return jsonify("Server received your scene info!")

    # send a vid
    else: 
        create_py_file(vid_id)
        create_vid(vid_id)

        # send file
        f = None
        try: 
            f = open(f"tmp/{vid_id}/media/videos/{vid_id}/480p15/{vid_id}.mp4", 'rb') 
        except: 
            print(f"Failed to open tmp/{vid_id}/media/videos/{vid_id}/480p15/{vid_id}.mp4") 
            pass

        # clean up vid files
        try: 
            shutil.rmtree(f"tmp/{vid_id}")
        except: 
            print(f"Failed to remove temp dir tmp/{vid_id}")
            pass

        return f.read() if f is not None else Response(status=500) 
    
def save_anim_data(fname, anim_data): 
    # create fname folder if needed
    try: 
        os.mkdir(f"tmp/{fname}", mode=0o777)
    except: 
        pass

    # wait for necessary files
    tmp_dir = f"tmp/{fname}"
    if not file_exists_delayed(tmp_dir, 5): 
        return

    with open(f"tmp/{fname}/anim_data.p", 'wb') as f: 
        pickle.dump(anim_data, f)
    with open(f"tmp/{fname}/anim_data.txt", 'w') as f: 
        f.write(str(anim_data))

def create_py_file(fname): 
    # wait for necessary files
    anim_data_path = f"tmp/{fname}/anim_data.p"
    if not file_exists_delayed(anim_data_path, 5): 
        return

    # parse anim_data and create python file
    with open(anim_data_path, 'rb') as f: 
        anim_data = pickle.load(f)

    try: 
        generate_manim_file(f"{fname}", anim_data)
    except: 
        print(f"Failed to generate manim file {fname}")

def create_vid(fname): 
    # wait for necessary files
    py_file_path = f"tmp/{fname}/{fname}.py"
    if not file_exists_delayed(py_file_path, 5): 
        return

    # run docker with manim to render vid
    try: 
        cwd = os.getcwd()
        subprocess.run( 
            f'docker run --rm -it -v {cwd}/tmp/{fname}:/manim manimcommunity/manim manim {fname}.py {fname} -ql'.split(' ')
        )
    except: 
        print(f"Docker failed to handle {fname}")

def file_exists_delayed(fpath, max_time_s): 
    time_counter = 0
    while not os.path.exists(fpath):
        time.sleep(1)
        time_counter += 1
        if time_counter > max_time_s:
            return False; 
    return True


if __name__ == '__main__':
    app.run()