from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')



@app.route('/manim', methods=['POST'])
def manim():
    anim_data = request.get_json()

    fname = "hello"
    with open(f"tmp/{fname}.txt", 'w') as f: 
        f.write(str(anim_data))

    f = open(f"vid/{fname}.txt", 'r') 
    return f.read()


if __name__ == '__main__':
    app.run()