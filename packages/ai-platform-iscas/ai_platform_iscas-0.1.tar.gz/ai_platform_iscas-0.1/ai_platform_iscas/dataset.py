import os
import urllib.parse
import urllib.request


def __init__(self):
    self.dataset_id = os.getenv("dataset_id")
    self.dataset_path = None
    self.dataset_tagging = None


def get_dataset_path(self):
    self.dataset_path = '/dataset/' + str(self.dataset_id) + "/dataset"
    return self.dataset_path


def get_tagging_path(self):
    self.dataset_tagging = '/dataset/' + str(self.dataset_id) + '/tagging.txt'
    return self.dataset_tagging

