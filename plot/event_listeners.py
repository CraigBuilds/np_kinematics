from abc import ABC, abstractmethod

class MouseEventListeners(ABC):
    @abstractmethod
    def on_click(self, event):pass
    @abstractmethod
    def on_release(self, event):pass
    @abstractmethod
    def on_motion(self, event):pass