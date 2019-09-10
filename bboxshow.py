import itertools
from pathlib import Path
from yolo import Yolo
from copy import deepcopy
import numpy as np
import json

from PyQt5.QtGui import QImage, QPainter, QPixmap, QPen, QKeySequence
from PyQt5.QtWidgets import (
    QWidget, QLabel, QMessageBox, QPushButton, QGridLayout, QDesktopWidget, QShortcut,
)
from PyQt5.QtCore import Qt


class BBoxShow(QWidget):

    def __init__(self, parent):
        super(BBoxShow, self).__init__()
        self.parent = parent
        self.statedict = deepcopy(parent.statedict)
        self.current_img = None

        self.imagebox = QLabel()
        self.buttons = (
            QPushButton(), QPushButton(), QPushButton(), QPushButton(),
        )

        self.init_ui()

    def init_ui(self) -> None:
        self.center()
        layout: QGridLayout = QGridLayout()
        self.setLayout(layout)

        # pix_map: QPixmap = QPixmap("./img/cam7_00002960.png").copy(*test_bbox_XmYmWH)
        pix_map = QPixmap()
        self.imagebox.setPixmap(pix_map)
        layout.addWidget(self.imagebox, 0, 0, 1, 4, Qt.AlignVCenter | Qt.AlignHCenter)

        for idx, (name, button) in enumerate(itertools.zip_longest(['<<', 'Human', 'Not Human', '>>'], self.buttons)):
            button.setText(name)
            layout.addWidget(button, 1, idx)

        self.buttons[0].clicked.connect(self.before)
        self.buttons[1].clicked.connect(self.human)
        self.buttons[2].clicked.connect(self.nohuman)
        self.buttons[3].clicked.connect(self.next)

        # shortcut
        beforeshorcut = QShortcut(QKeySequence(Qt.Key_A), self)
        beforeshorcut.activated.connect(self.before)
        humanshorcut = QShortcut(QKeySequence(Qt.Key_S), self)
        humanshorcut.activated.connect(self.human)
        nohumanshorcut = QShortcut(QKeySequence(Qt.Key_D), self)
        nohumanshorcut.activated.connect(self.nohuman)
        nextshorcut = QShortcut(QKeySequence(Qt.Key_F), self)
        nextshorcut.activated.connect(self.next)

        if Path.is_file(Path(self.statedict['changedir']) / 'state.json'):
            self.deserialize()
        self.refresh(True)

    # from https://gist.github.com/saleph/163d73e0933044d0e2c4
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def refresh(self, reload=False):
        if 'imglist' not in self.statedict:
            reload = True
            self.statedict['imglist'] = sorted([str(name.relative_to(self.statedict['imgdir']).with_suffix(''))
                                                for name in Path(self.statedict['imgdir']).glob('**/*.png')])
        self.statedict['current_img_idx'] = self.statedict.get('current_img_idx', 0)

        if 'bboxes' not in self.statedict:
            self.statedict['bboxes'] = Yolo.read_yolo(
                Path(self.statedict['origdir']) /
                (self.statedict['imglist'][self.statedict['current_img_idx']] + '.txt')
            )

        if 'bbox_nocheck' not in self.statedict:
            if Path.is_file(Path(self.statedict['changedir']) /
                            (self.statedict['imglist'][self.statedict['current_img_idx']] + '.txt')):
                yolo = Yolo.read_yolo(
                    Path(self.statedict['changedir']) /
                    (self.statedict['imglist'][self.statedict['current_img_idx']] + '.txt')
                )
                self.statedict['bbox_nocheck'] = list()
                self.statedict['bbox_human'] = [
                    int(self.statedict['bboxes'].tolist().index(idx)) for idx in yolo.tolist()
                ]
                self.statedict['bbox_nohuman'] = [
                    idx for idx in range(len(self.statedict['bboxes'])) if idx not in self.statedict['bbox_human']
                ]
            else:
                self.statedict['bbox_nocheck'] = list(range(len(self.statedict['bboxes'])))
                self.statedict['bbox_human'] = list()
                self.statedict['bbox_nohuman'] = list()
        self.statedict['current_bbox_idx'] = self.statedict.get('current_bbox_idx', 0)

        if reload:
            self.current_img: QPixmap = QPixmap(
                str(Path(self.statedict['imgdir']) /
                    (self.statedict['imglist'][self.statedict['current_img_idx']] + '.png'))
            )
            painter = QPainter(self.current_img)
            rectpen = QPen(Qt.green)
            rectpen.setWidth(1)
            painter.setPen(rectpen)
            image_size = (self.current_img.width(), self.current_img.height())
            bbox_int = [
                [int(i) for i in j] for j in Yolo.expand(Yolo.ccwh2tlwh(self.statedict['bboxes']), image_size)
            ]
            for bbox in bbox_int:
                painter.drawRect(int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]))
            painter.end()

        image_size = (self.current_img.width(), self.current_img.height())
        bbox = self.statedict['bboxes'][self.statedict['current_bbox_idx']]
        bbox_int = [int(i) for i in Yolo.expand(Yolo.ccwh2tlwh(bbox), image_size)]
        twice_bbox_int = [int(i) for i in Yolo.expand(Yolo.ccwh2tlwh(Yolo.twice(bbox)), image_size)]

        pix_map = self.current_img.copy(*twice_bbox_int)
        painter = QPainter(pix_map)
        rectpen = QPen(Qt.red)
        rectpen.setWidth(2)
        painter.setPen(rectpen)
        painter.drawRect(
            bbox_int[0] - max(twice_bbox_int[0], 0),
            bbox_int[1] - max(twice_bbox_int[1], 0),
            bbox_int[2], bbox_int[3],
        )
        painter.end()

        self.setWindowTitle(f'{self.statedict["imglist"][self.statedict["current_img_idx"]]}'
                            f'( {self.statedict["current_bbox_idx"]} / {len(self.statedict["bboxes"])} )')
        self.imagebox.setPixmap(pix_map)

    def next(self):
        if ('current_bbox_idx' in self.statedict and
                (len(self.statedict['bboxes']) == self.statedict['current_bbox_idx'] + 1)):
            if ('current_img_idx' in self.statedict and
                    (len(self.statedict['imglist']) == self.statedict['current_img_idx'] + 1)):
                QMessageBox.warning(None, "End of Images",
                                    "Complete!")
                self.maywrite()
                return
            else:
                self.statedict['current_img_idx'] += 1
                self.statedict['current_bbox_idx'] = 0
                self.maywrite()
                self.refresh(True)
        else:
            self.statedict['current_bbox_idx'] += 1
            self.refresh()

    def before(self):
        if ('current_bbox_idx' in self.statedict and
                (self.statedict['current_bbox_idx'] == 0)):
            if ('current_img_idx' in self.statedict and
                    (self.statedict['current_img_idx'] == 0)):
                QMessageBox.warning(None, "Start of Images",
                                    "ToDo")
                return
            else:
                self.statedict['current_img_idx'] -= 1
                self.statedict['current_bbox_idx'] = 0
                self.refresh(True)
        else:
            self.statedict['current_bbox_idx'] -= 1
            self.refresh()

    def human(self):
        cur_bbox_idx = self.statedict['current_bbox_idx']
        if cur_bbox_idx not in self.statedict['bbox_human']:
            if cur_bbox_idx in self.statedict['bbox_nocheck']:
                self.statedict['bbox_nocheck'].remove(cur_bbox_idx)
            elif cur_bbox_idx in self.statedict['bbox_nohuman']:
                self.statedict['bbox_nohuman'].remove(cur_bbox_idx)
            else:
                raise Exception()
            self.statedict['bbox_human'].append(cur_bbox_idx)
        self.next()

    def nohuman(self):
        cur_bbox_idx = self.statedict['current_bbox_idx']
        if cur_bbox_idx not in self.statedict['bbox_nohuman']:
            if cur_bbox_idx in self.statedict['bbox_nocheck']:
                self.statedict['bbox_nocheck'].remove(cur_bbox_idx)
            elif cur_bbox_idx in self.statedict['bbox_human']:
                self.statedict['bbox_human'].remove(cur_bbox_idx)
            else:
                raise Exception()
            self.statedict['bbox_nohuman'].append(cur_bbox_idx)
        self.next()

    def maywrite(self):
        if len(self.statedict['bbox_nocheck']) == 0:  # all checked, write checked yolo
            checked_bbox = np.stack([self.statedict['bboxes'][idx] for idx in self.statedict['bbox_human']])
            Yolo.write_yolo(Path(self.statedict['changedir']) /
                            (self.statedict['imglist'][self.statedict['current_img_idx']] + '.txt'), checked_bbox)

    def serialize(self):
        self.statedict['bboxes'] = self.statedict['bboxes'].tolist()
        with open(Path(self.statedict['changedir']) / 'state.json', 'w') as fp:
            json.dump(self.statedict, fp, indent=4)

    def deserialize(self):
        with open(Path(self.statedict['changedir']) / 'state.json', 'r') as fp:
            self.statedict = json.load(fp)
        self.statedict['bboxes'] = np.array(self.statedict['bboxes'])

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.parent.show()
            self.serialize()
            self.maywrite()
            event.accept()
        else:
            event.ignore()
