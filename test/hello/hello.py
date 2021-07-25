from manim import *
class hello(Scene):
  def construct(self):
    obj_0_0 = Circle(radius=1, color="blue") 
    obj_0_0.set_x(0) 
    obj_0_0.set_y(0) 
    obj_0_0.scale(1) 
    obj_0_0.rotate(0.0, about_point=[0, 0, 0] ) 
    obj_0_1 = Circle(radius=1, color="red") 
    obj_0_1.set_x(0) 
    obj_0_1.set_y(1) 
    obj_0_1.scale(1) 
    obj_0_1.rotate(0.0, about_point=[0, 1, 0] ) 
    obj_0_2 = Circle(radius=1, color="red") 
    obj_0_2.set_x(0) 
    obj_0_2.set_y(1) 
    obj_0_2.scale(1) 
    obj_0_2.rotate(0.0, about_point=[0, 1, 0] ) 
    obj_1_0 = Square(color="blue") 
    obj_1_0.set_x(4) 
    obj_1_0.set_y(0) 
    obj_1_0.scale(1) 
    obj_1_0.rotate(0.0, about_point=[4, 0, 0] ) 
    obj_1_1 = Square(color="blue") 
    obj_1_1.set_x(1) 
    obj_1_1.set_y(0) 
    obj_1_1.scale(1) 
    obj_1_1.rotate(0.7853981633974483, about_point=[1, 0, 0] ) 
    self.add(obj_0_0)
    self.play(Transform( obj_0_0, obj_0_1, run_time=2 )) 
    self.play(Transform( obj_0_1, obj_0_2, run_time=0 )) 
    self.add(obj_1_0)
    self.play(Transform( obj_1_0, obj_1_1, run_time=2 )) 
    self.wait(1)
