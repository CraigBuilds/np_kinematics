from src.kinematics import *
from plot.joint_plot import *
from plot.event_listeners import *
from matrix_math import *
import tkinter as tk

# robot = Robot2D(
#     origin=np.array([0.0, 0.0]),
#     configuration=[
#         Joint(radians=0.0),
#         Link(length=1.0),
#         Joint(radians=0.0),
#         Link(length=1.0),
#     ]
# poses = [forward_kinematics(robot, i) for i in range(len(robot))]

def main():
    app = tk.Tk()
    plot = JointPlot(master=app)
    app.mainloop()

if __name__ == "__main__":
    main()