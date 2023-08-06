# -*- coding:utf-8 -*-
import gc
import torch
import torch.backends.cudnn as cudnn
from copy import deepcopy


# 通用PyTorch推理框架
class Model(object):
    def __init__(self, net, model_path, param_key=None, strict=True):
        cudnn.benchmark = True
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.cpu_device = torch.device('cpu')

        net_params = torch.load(model_path, map_location=self.cpu_device)
        if param_key is not None and param_key in net_params:
                net_params = net_params[param_key]

        # remove unnecessary 'module.' or 'model.'
        for k, v in deepcopy(net_params).items():
            if k.startswith('module.'):
                net_params[k[7:]] = v
                net_params.pop(k)
            elif k.startswith('model.'):
                net_params[k[6:]] = v
                net_params.pop(k)

        net.load_state_dict(net_params, strict=strict)

        self.model = net
        self.model.eval()
        self.model = self.model.to(self.device)

    def predict(self, inputs):
        if isinstance(inputs, tuple):
            inputs = list(inputs)

        with torch.no_grad():
            if isinstance(inputs, dict):
                for k, v in inputs.items():
                    inputs[k] = v.to(self.device)
                results = self.model(**inputs)
            elif isinstance(inputs, list):
                for i in range(len(inputs)):
                    inputs[i] = inputs[i].to(self.device)
                results = self.model(*inputs)
            else:
                inputs = inputs.to(self.device)
                results = self.model(inputs)

        if isinstance(results, tuple):
            results = list(results)
        if isinstance(results, torch.Tensor):
            results = results.to(self.cpu_device)
        elif isinstance(results, dict):
            for k, v in results.items():
                results[k] = v.to(self.cpu_device)
        elif isinstance(results, list):
            for i in range(len(results)):
                results[i] = results[i].to(self.cpu_device)

        gc.collect()
        torch.cuda.empty_cache()
        return results
