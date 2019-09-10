import numpy as np


class Yolo(object):

    @staticmethod
    def read_yolo(yolo_path):
        with open(yolo_path, 'r') as fp:
            yolo = fp.read()
        yolo = [np.fromstring(i, sep=' ') for i in filter(None, yolo.split('\n'))]
        return np.stack(yolo)[:, 1:]

    @staticmethod
    def write_yolo(yolo_path, yolo):
        yolo = '\n'.join([f'0 {xcen} {ycen} {width} {higth}' for xcen, ycen, width, higth in
                          yolo])
        with open(yolo_path, 'w') as fp:
            fp.write(yolo)

    @staticmethod
    def ccwh2tlwh(bbox):
        ccwh2tlwh_arr = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-.5, 0, 1, 0],
            [0, -.5, 0, 1],
        ])
        return np.matmul(bbox, ccwh2tlwh_arr)

    @staticmethod
    def twice(bbox):
        return np.matmul(bbox, np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 2],
        ]))

    @staticmethod
    def expand(bbox, size):
        return np.matmul(bbox, np.array([
            [size[0], 0, 0, 0],
            [0, size[1], 0, 0],
            [0, 0, size[0], 0],
            [0, 0, 0, size[1]],
        ]))
