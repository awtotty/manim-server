from manim import *
class hello(Scene):
  def construct(self):
    obj0 = Circle(radius=1, color="blue") 
    self.add(obj0)
    self.wait(1)
    obj1 = Square(color="blue") 
    self.add(obj1)
    self.wait(1)
