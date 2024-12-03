from PyQt5.QtWidgets import QApplication

from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2

app = QApplication([])

class VideoWidget:
    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration(
            main={"size": (1920, 1080)}
        )
        self.camera.configure(config)
        self.box = QGlPicamera2(self.camera)

    def start_stream(self):
        self.camera.start()

    def stop_stream(self):
        self.camera.stop()

video = VideoWidget()
video.box.show()
video.start_stream()
app.exec()
