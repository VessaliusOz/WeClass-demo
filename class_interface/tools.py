# coding: utf-8


class StatusHandler(object):

    def __init__(self):
        self.status = False

    def reverse_status(self):
        self.status = not self.status


status_handler = StatusHandler()
