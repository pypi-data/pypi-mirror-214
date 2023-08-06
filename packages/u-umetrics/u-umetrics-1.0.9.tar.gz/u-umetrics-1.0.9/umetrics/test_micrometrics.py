# -*- coding: utf8 -*-
#
import random
from typing import List

from sklearn.metrics import f1_score
from umetrics.micrometrics import MicroMetrics
from unittest import TestCase


class TestMicroMetrics(TestCase):
    def test_a(self):
        y_true = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4]
        y_pred = [1, 1, 1, 0, 0, 2, 2, 3, 3, 3, 4, 3, 4, 3]

        m = MicroMetrics(labels=[1, 2, 3, 4])
        m.step(y_trues=y_true, y_preds=y_pred)
        assert f1_score(y_true=y_true, y_pred=y_pred, labels=[1, 2, 3, 4], average='micro') == m.f1_score()

    def test_if_label_is_null(self):
        # 如果没有指定labels，默认则所有的标签就计算，例如：
        y_true = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4]
        y_pred = [1, 1, 1, 0, 0, 2, 2, 3, 3, 3, 4, 3, 4, 3]

        assert f1_score(y_true=y_true, y_pred=y_pred, average='micro') == f1_score(y_true=y_true, y_pred=y_pred,
                                                                                   labels=[0, 1, 2, 3, 4],
                                                                                   average='micro')

    def test_c(self):
        y_true = [random.randint(0, 10) for i in range(10000)]
        y_pred = [random.randint(0, 10) for i in range(10000)]

        labels = list(range(0, 11))
        m = MicroMetrics(labels=labels)

        batch_y_trues = split_l(y_true, size=32)
        batch_y_preds = split_l(y_pred, size=32)
        for batch_y_true, batch_y_pred in zip(batch_y_trues, batch_y_preds):
            m.step(y_trues=batch_y_true, y_preds=batch_y_pred)

        assert f1_score(y_true=y_true, y_pred=y_pred, labels=labels, average='micro') == m.f1_score()


def split_l(l: List, size=32):
    results = []
    buf = []
    buf_size = 0
    for i in l:
        buf.append(i)
        buf_size += 1
        if buf_size == size:
            results.append(buf)
            buf, buf_size = [], 0
    if buf:
        results.append(buf)
        buf, buf_size = [], 0
    return results
