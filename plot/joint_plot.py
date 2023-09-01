from dataclasses import dataclass
import tkinter as tk
from typing import Dict, Optional, List, Tuple
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.kinematics import Pose
from plot.event_listeners import MouseEventListeners
import numpy as np

@dataclass
class MetaData:
    style: str = 'o'
    directional: bool = False
    selected: bool = False
    color = 'red'

class JointPlot(FigureCanvasTkAgg):

    def __init__(        
        self,
        master: tk.Tk,
        event_listeners: List[MouseEventListeners] = []
    ) -> None:
        super().__init__(Figure(figsize=(5, 5), dpi=100), master=master)
        # create a store for the data that will be plotted
        self.__pose_data: Dict[str, Tuple[Pose, MetaData]] = {}
        # pack inside the master frame
        self_as_tk = self.get_tk_widget()
        self_as_tk.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # add default event listener
        event_listeners.append(PointSelector(self))
        # subscribe to event listeners
        for event_listener in event_listeners:
            self.mpl_connect("button_press_event", event_listener.on_click)
            self.mpl_connect("button_release_event", event_listener.on_release)
            self.mpl_connect("motion_notify_event", event_listener.on_motion)
        # create the plot
        self.__plot = self.figure.add_subplot(111)

    def data(self) -> List[Tuple[Pose, MetaData]]:
        """Return a list of all the poses and metadata."""
        return list(self.__pose_data.values())

    def redraw(self) -> None:
        """Redraw the plot."""
        self.__plot.clear()
        for pose, metadata in self.__pose_data.values():
            self.__plot.plot(pose.position[0], pose.position[1], metadata.style, color=metadata.color)
            if metadata.directional:
                self.__plot.arrow(
                    pose.position[0],
                    pose.position[1],
                    np.cos(pose.orientation),
                    np.sin(pose.orientation),
                    head_width= 0.1,
                    head_length= 0.1,
                    fc='k',
                    ec='k',
                )
            if metadata.selected:
                self.__plot.plot(pose.position[0], pose.position[1], 'x')

        self.__plot.grid(True)
        self.draw()

    def add_pose(self, pose: Pose, directional: bool = True):
        """Add the given pose (position and orientation) as a point on the plot."""
        self.__pose_data[pose] = (pose, MetaData(style='o', directional=directional))
        self.redraw()

    def add_connected_poses(
        self,
        poses: List[Pose],
    ) -> None:
        """add each pose (position and orientation) as connected points on the plot."""
        for pose in poses:
            self.__pose_data[pose] = (pose, MetaData(style='-o'))
        self.redraw()

    def remove_pose(self, pose: Pose):
        """Remove the given pose from the plot."""
        if pose in self.__pose_data:
            del self.__pose_data[pose]
            self.redraw()

    def selected_poses(self) -> List[Pose]:
        """get all the poses that are selected"""
        return [pose for pose, metadata in self.__pose_data.values() if metadata.selected]

    def selected_pose(self) -> Optional[Pose]:
        """get the first pose that is selected"""
        for pose, metadata in self.__pose_data.values():
            if metadata.selected:
                return pose
        return None

class PointSelector(MouseEventListeners):
    def __init__(self, parent: JointPlot) -> None:
        self.__parent = parent

    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return
        for _, metadata in self.__parent.data():
            metadata.selected = False
        (x, y) = (event.xdata, event.ydata)
        #get the first pose that is within 0.2 units of the given point
        result = None
        for pose, metadata in self.__parent.data():
            if np.linalg.norm(pose.position - np.array([x, y])) < 0.2:
                result = (pose, metadata)

        if result is not None:
            _, metadata = result
            metadata.selected = not metadata.selected
        self.__parent.redraw()

    def on_release(self, event):
        pass
    def on_motion(self, event):
        pass