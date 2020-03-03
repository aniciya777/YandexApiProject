import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = 37.530887, 55.703118
        self.scale = 0.002
        self.map_style = 'map'
        self.initUI()
        self.getImage()

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
        ## Изображение
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(response.content)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
