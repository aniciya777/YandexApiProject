import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = 37.530887, 55.703118
        self.scale = 0.002
        self.scale_coeff = 2
        self.map_style = 'map'
        self.initUI()
        self.getImage()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.pixmap = QPixmap()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params={
            'll': ','.join(map(str, self.coords)),
            'spn': ','.join(map(str, [self.scale] * 2)),
            'l': self.map_style
        })
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.pixmap.loadFromData(response.content)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.scale *= self.scale_coeff
            self.getImage()
        elif event.key() == Qt.Key_PageUp:
            self.scale /= self.scale_coeff
            self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
