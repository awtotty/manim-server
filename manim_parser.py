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

    fpath = f"tmp/{fname}/{fname}.py"
    # TODO: test should be replaced with tmp
    # fpath = f"test/{fname}/{fname}.py"

    print(anim_data)

    # groups_dict stores a dict for each time marker in object states
    groups_dict = {}
    mobject_times_dict = {}

    # create objects
    for shape_i, shape in enumerate(anim_data): 
        shape_type = shape["typeStr"]
        states = shape["states"]
        max_t = 0 
        min_t = 0 

        for state_i, state in enumerate(states): 
            state["x"] = float(state["x"])
            state["y"] = float(state["y"])
            state["rot"] = float(state["rot"])
            state["size"] = float(state["size"])
            state["time"] = float(state["time"])

            t = state["time"] 
            t_str = str(t).replace(".", "_")

            # track start/end times for this mobject
            if state_i == 0: 
                max_t = t
                min_t = t
            if t > max_t: 
                max_t = t
            if t < min_t: 
                min_t = t

            # make the obj 
            if shape_type == "Circle": 
                fcontents += f"{dtab}obj_{shape_i}_{t_str} = {construct_circle_str(state)} \n"
            elif shape_type == "Square": 
                fcontents += f"{dtab}obj_{shape_i}_{t_str} = {construct_square_str(state)} \n"
            elif shape_type == "Triangle": 
                fcontents += f"{dtab}obj_{shape_i}_{t_str} = {construct_triangle_str(state)} \n"
            elif shape_type == "Point": 
                fcontents += f"{dtab}obj_{shape_i}_{t_str} = {construct_point_str(state)} \n"

            # set mobject state
            fcontents += f"{dtab}obj_{shape_i}_{t_str}.set_x({state['x']}) \n"
            fcontents += f"{dtab}obj_{shape_i}_{t_str}.set_y({state['y']}) \n"
            fcontents += f"{dtab}obj_{shape_i}_{t_str}.scale({state['size']}) \n"
            fcontents += f"{dtab}obj_{shape_i}_{t_str}.rotate({state['rot']*math.pi/180}, about_point=[{state['x']}, {state['y']}, 0] ) \n"

            # add mobject state to group
            if t not in groups_dict: 
                groups_dict[t] = {}
            groups_dict[t][shape_i] = f"obj_{shape_i}_{t_str}"

        # track start/end times for this mobject
        mobject_times_dict[shape_i] = [min_t, max_t]

    # fill out the missing values in the time groups
    prev_state_dict = {}
    for t in sorted(groups_dict): 
        for shape_i, shape in enumerate(anim_data): 
            # shape not found in this time step
            if shape_i not in groups_dict[t]: 
                # shape should continue with prev state
                if mobject_times_dict[shape_i][0] < t and t < mobject_times_dict[shape_i][1]: 
                    groups_dict[t][shape_i] = prev_state_dict[shape_i]
                # shape should not currently exist 
                else: 
                    groups_dict[t][shape_i] = "VMobject()"
                    prev_state_dict[shape_i] = groups_dict[t][shape_i]
            # shape was found, so remember state 
            else: 
                prev_state_dict[shape_i] = groups_dict[t][shape_i]
        
    # create animation groups
    for t in sorted(groups_dict): 
        t_str = str(t).replace(".", "_")
        # build a group
        group_list = []
        for shape_i in sorted(groups_dict[t]): 
            group_list.append(groups_dict[t][shape_i])

        fcontents += f"{dtab}group_{t_str} = VGroup({','.join(group_list)}) \n"

    # create animations
    t_prev = 0
    t_str_prev = "0"
    for t_i, t in enumerate(sorted(groups_dict)): 
        t_str = str(t).replace(".", "_")

        if t_i == 0: 
            t_prev = t
            t_str_prev = t_str
            fcontents += f"{dtab}self.add(group_{t_str}) \n"
            continue

        run_time = t - t_prev
        fcontents += f"{dtab}self.play(Transform( group_{t_str_prev}, group_{t_str}, run_time={run_time} )) \n"
        fcontents += f"{dtab}self.remove(group_{t_str_prev}) \n"
        fcontents += f"{dtab}self.add(group_{t_str}) \n"

        t_prev = t
        t_str_prev = t_str

    # end vid with 1 sec wait
    fcontents += f"{dtab}self.wait(1)\n"

    with open(fpath, "w") as f: 
        f.write(fcontents)



def construct_circle_str(state): 
    return f"Circle(radius=1, color=\"{state['color']}\")"
    
def construct_square_str(state): 
    return f"Square(color=\"{state['color']}\")"

def construct_triangle_str(state): 
    return f"Triangle(color=\"{state['color']}\")"

def construct_point_str(state): 
    return f"Dot(color=\"{state['color']}\")"


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
    anim_data[0]["states"][0]["time"] = 0.5
    anim_data[0]["states"][1]["x"] = 2
    anim_data[0]["states"][1]["y"] = 1
    anim_data[0]["states"][1]["size"] = 2
    anim_data[0]["states"][1]["time"] = 1
    # anim_data[0]["states"].append(anim_data[0]["states"][1].copy())
    # anim_data[0]["states"][2]["x"] = 0
    # anim_data[0]["states"][2]["y"] = 1
    # anim_data[0]["states"][2]["size"] = 1
    # anim_data[0]["states"][2]["time"] = 2

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
    test_gen()
    # run_manim("group_test")