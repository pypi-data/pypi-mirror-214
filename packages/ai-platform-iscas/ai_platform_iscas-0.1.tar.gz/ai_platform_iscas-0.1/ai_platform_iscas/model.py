import os
import urllib.parse
import urllib.request


def __init__(self):
    self.svc_ip = os.getenv("svc_ip")
    self.model_id = os.getenv("model_id")
    self.modelApi = os.getenv("modelApi")


def get_model_api(self):
    return self.modelApi


def commit_train_acc(self, acc):
    data = {'modelId': str(self.model_id), "acc": acc}
    data = urllib.parse.urlencode(data).encode('utf-8')
    address = "http://" + str(self.svc_ip) + ":8080/train/addAcc"
    req = urllib.request.Request(url=address, data=data, method='POST')
    response = urllib.request.urlopen(req)
    return response


def commit_validation_acc(self, acc):
    data = {'modelId': str(self.model_id), "validationAccuracy": acc}
    data = urllib.parse.urlencode(data).encode('utf-8')
    address = "http://" + str(self.svc_ip) + ":8080/model/addValidationAcc"
    req = urllib.request.Request(url=address, data=data, method='POST')
    response = urllib.request.urlopen(req)
    return response
