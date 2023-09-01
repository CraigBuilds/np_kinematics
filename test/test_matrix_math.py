from src.kinematics import *
from plot.joint_plot import *
from plot.event_listeners import *
from src.matrix_math import *
import tkinter as tk
from functools import partial

def main():
    app = tk.Tk()
    plot = JointPlot(master=app)
    origin = Pose(position=np.array([0.0, 0.0]), orientation=0.0)
    x10y0 = Pose(position=np.array([10.0, 0.0]), orientation=0.0)
    x0y10 = Pose(position=np.array([0.0, 10.0]), orientation=0.0)
    plot.add_pose(origin)
    plot.add_pose(x10y0)
    plot.add_pose(x0y10)

    def apply_rotation(degrees: tk.StringVar):
        pose = plot.selected_pose()
        if not pose:
            print("No pose selected")
            return
        radians = np.deg2rad(float(degrees.get()))
        print(f"Applying rotation of {radians:.3f} radians")
        rot = rotation_matrix(radians)
        pretty_print_rotation_matrix(rot)
        new_pos = np.matmul(rot, pose.position)
        plot.remove_pose(pose)
        plot.add_pose(Pose(position=new_pos, orientation=pose.orientation + radians))

    def apply_translation(x: tk.StringVar, y: tk.StringVar):
        pose = plot.selected_pose()
        if not pose:
            print("No pose selected")
            return
        x = float(x.get())
        y = float(y.get())
        print(f"Applying translation of ({x:.3f}, {y:.3f})")
        t = translation_matrix(x, y)
        pretty_print_translation_matrix(t)
        temp_resized = np.append(pose.position, 1.0)
        new_pose_resized = np.matmul(t, temp_resized)
        new_pose = new_pose_resized[:2]
        plot.remove_pose(pose)
        plot.add_pose(Pose(position=new_pose, orientation=pose.orientation))

    def apply_transformation(degrees: tk.StringVar, x: tk.StringVar, y: tk.StringVar):
        pose = plot.selected_pose()
        if not pose:
            print("No pose selected")
            return
        radians = np.deg2rad(float(degrees.get()))
        x = float(x.get())
        y = float(y.get())
        print(f"Applying transformation of {radians:.3f} radians and ({x:.3f}, {y:.3f})")
        t = transformation_matrix(x, y, radians)
        pretty_print_transformation_matrix(t)
        resized = np.append(pose.position, 1.0)
        new_pose_resized = np.matmul(t, resized)
        new_pose = new_pose_resized[:2]
        plot.remove_pose(pose)
        plot.add_pose(Pose(position=new_pose, orientation=pose.orientation + radians))

    angle= tk.StringVar(master=app, value="0.0")
    translation_x = tk.StringVar(master=app, value="0.0")
    translation_y = tk.StringVar(master=app, value="0.0")
    layout = [
        tk.Spinbox(master=app, from_=-360, to=360, increment=10, textvariable=angle),
        tk.Button(master=app, text="Apply Rotation", command=partial(apply_rotation, angle)),
        tk.Spinbox(master=app, from_=-10, to=10, increment=1, textvariable=translation_x),
        tk.Spinbox(master=app, from_=-10, to=10, increment=1, textvariable=translation_y),
        tk.Button(master=app, text="Apply Translation", command=partial(apply_translation, translation_x, translation_y)),
        tk.Button(master=app, text="Apply Transformation", command=partial(apply_transformation, angle, translation_x, translation_y)),
    ]
    for widget in layout:
        widget.pack()
    app.mainloop()

if __name__ == "__main__":
    main()