import math

# TODO: remove after testing
import os
import pickle
import os
import subprocess

tab = "  "
dtab = tab * 2

def generate_manim_file(fname, anim_data): 
    fcontents = "from manim import *\n"     
    fcontents += f"class {fname}(Scene):\n"
    fcontents += f"{tab}def construct(self):\n"

    # TODO: test should be replaced with tmp
    fpath = f"test/{fname}/{fname}.py"

    # groups_dict = {}

    # create objects
    for shape_i, shape in enumerate(anim_data): 
        shape_type = shape["typeStr"]
        states = shape["states"]

        for state_i, state in enumerate(states): 
            # make the obj 
            if shape_type == "Circle": 
                fcontents += f"{dtab}obj_{shape_i}_{state_i} = {construct_circle_str(state)} \n"
            elif shape_type == "Square": 
                fcontents += f"{dtab}obj_{shape_i}_{state_i} = {construct_square_str(state)} \n"

            # set state
            fcontents += f"{dtab}obj_{shape_i}_{state_i}.set_x({state['x']}) \n"
            fcontents += f"{dtab}obj_{shape_i}_{state_i}.set_y({state['y']}) \n"
            fcontents += f"{dtab}obj_{shape_i}_{state_i}.scale({state['size']}) \n"
            fcontents += f"{dtab}obj_{shape_i}_{state_i}.rotate({state['rot']*math.pi/180}, about_point=[{state['x']}, {state['y']}, 0] ) \n"

    # create animations
    for shape_i, shape in enumerate(anim_data): 
        states = shape["states"]
        for state_i, state in enumerate(states): 
            # init the mobject
            if state_i == 0: 
                fcontents += f"{dtab}self.add(obj_{shape_i}_{state_i})\n"
            # transform from prev obj to curr obj
            else: 
                run_time = state["time"] - states[state_i-1]["time"]
                run_time = 0 if run_time < 0 else run_time
                fcontents += f"{dtab}self.play(Transform( obj_{shape_i}_{state_i-1}, obj_{shape_i}_{state_i}, run_time={run_time} )) \n"

    # end vid with 1 sec wait
    fcontents += f"{dtab}self.wait(1)\n"

    with open(fpath, "w") as f: 
        f.write(fcontents)



def construct_circle_str(state): 
    return f"Circle(radius=1, color=\"{state['color']}\")"
    
def construct_square_str(state): 
    return f"Square(color=\"{state['color']}\")"



# TODO: remove after testing
def run_manim(fname): 
    # run docker with manim to render vid
    cwd = os.getcwd()
    subprocess.run( 
        f'docker run --rm -it -v {cwd}/test/{fname}:/manim manimcommunity/manim manim {fname}.py {fname} -ql'.split(' ')
    )


def test_gen():
    fname = "hello"

    with open("test/hello/anim_data.p", 'rb') as f: 
        anim_data = pickle.load(f)
    
    anim_data[0]["states"][0]["x"] = 0
    anim_data[0]["states"][0]["y"] = 0
    anim_data[0]["states"][0]["time"] = 0
    anim_data[0]["states"][1]["x"] = 2
    anim_data[0]["states"][1]["y"] = 1
    anim_data[0]["states"][1]["size"] = 2
    anim_data[0]["states"][1]["time"] = 1
    anim_data[0]["states"].append(anim_data[0]["states"][1])
    anim_data[0]["states"][2]["x"] = 0
    anim_data[0]["states"][2]["y"] = 1
    anim_data[0]["states"][2]["size"] = 1
    anim_data[0]["states"][2]["time"] = 2

    anim_data[1]["states"][0]["x"] = 4
    anim_data[1]["states"][0]["y"] = 0
    anim_data[1]["states"][0]["time"] = 0
    anim_data[1]["states"][1]["x"] = 1
    anim_data[1]["states"][1]["y"] = 0
    anim_data[1]["states"][1]["rot"] = 45 
    anim_data[1]["states"][1]["time"] = 2

    generate_manim_file(fname, anim_data)

    run_manim(fname)


if __name__ == "__main__": 
    # test_gen()
    run_manim("group_test")