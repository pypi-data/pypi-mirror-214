import os
import numpy as np
import torch
from vectorium.utils import *


class VectorDatabase:
    def __init__(self, collection, dim=None, collection_path='db'):
        self.collection = collection
        self.collection_path = os.path.join(collection_path, f'{collection}.npz')

        os.makedirs(name=collection_path, exist_ok=True)
        
        if os.path.exists(self.collection_path):
            self.load(self.collection_path)
        else:
            self.data_dict = {}
            self.dim = dim
            self.keys = []

        self.compare_functions = {
            'cosine': cosine_similarity,
            'euclidean': euclidean_distance,
            'dot': dot_product,
        }

        self.aggregate_functions = {
            'mean': np.mean,
            'sum': np.sum,
            'max': np.max,
            'min': np.min,
            'none': lambda x: x,
        }
    
    def add(self, key, vec):
        if isinstance(vec, torch.Tensor):
            vec = vec.detach().cpu().numpy()

        if self.dim is None:
            self.dim = vec.shape[-1]

        assert vec.shape[-1] == self.dim, f'Vector dimension must be {self.dim} instead of {vec.shape[-1]}'
        
        if vec.ndim == 1:
            vec = vec.reshape(1, -1)
        
        if key not in self.data_dict:
            self.data_dict[key] = vec
        else:
            self.data_dict[key] = np.concatenate([self.data_dict[key], vec])
        self.update()

    def remove(self, key):
        del self.data_dict[key]
        self.update()

    def compare(self, input_vector, func='cosine', aggregate='mean'):
        if isinstance(input_vector, torch.Tensor):
            input_vector = input_vector.detach().cpu().numpy()

        if input_vector.ndim == 1:
            input_vector = input_vector.reshape(1, -1)

        if input_vector.shape[1] != self.dim:
            raise ValueError(f'input_vector must be of dimension {self.dim} instead of {input_vector.shape[1]}')

        if isinstance(func, str):
            if func not in self.compare_functions:
                raise ValueError(f"Invalid function: {func}. Valid options are {list(self.compare_functions.keys())}")
            func = self.compare_functions[func]

        results = {}
        for key, vectors in self.data_dict.items():
            results[key] = func(input_vector, vectors).squeeze()

        if aggregate not in self.aggregate_functions:
            raise ValueError(f"Invalid aggregate function: {aggregate}. Valid options are {list(self.aggregate_functions.keys())}")

        results = {key: self.aggregate_functions[aggregate](values) for key, values in results.items()}

        return results

    def topk(self, input_vector, k=10, func='cosine', aggregate='mean', reverse=False):
        results = self.compare(input_vector, func=func, aggregate=aggregate)
        results = sorted(results.items(), key=lambda x: x[1], reverse=reverse)[:k]
        results = {key: value for key, value in results}
        return results

    def reset(self):
        self.data_dict = {}
        self.update()

    def save(self):
        np.savez(self.collection_path, **self.data_dict)

    def load(self, collection_path):
        self.data_dict = dict(np.load(collection_path))
        self.dim = self.data_dict[list(self.data_dict.keys())[0]].shape[-1]
        self.keys = list(self.data_dict.keys())
        self.update()

    def update(self):
        self.data_list = dict2tuple(self.data_dict)
        self.keys = list(self.data_dict.keys())
