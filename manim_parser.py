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

    for shape_i, shape in enumerate(anim_data): 
        shape_type = shape["typeStr"]
        states = shape["states"]

        # handle animations
        for state_i, state in enumerate(states): 
            # init the mobject
            if state_i == 0: 
                if shape_type == "Circle": 
                    fcontents += f"{dtab}obj{shape_i} = {construct_circle_str(state)} \n"
                elif shape_type == "Square": 
                    fcontents += f"{dtab}obj{shape_i} = {construct_square_str(state)} \n"


        fcontents += f"{dtab}self.add(obj{shape_i})\n"
        fcontents += f"{dtab}self.wait(1)\n"
    

    with open(fpath, "w") as f: 
        f.write(fcontents)



def construct_circle_str(state): 
    return f"Circle(radius={state['size']}, color=\"{state['color']}\")"
    
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

    generate_manim_file(fname, anim_data)

    run_manim(fname)


if __name__ == "__main__": 
    test_gen()