import numpy as np


def dict2tuple(data):
    data_list = []
    for key, value in data.items():
        key_vectors = [vec.reshape(-1) for vec in np.split(value, value.shape[0])]
        for vec in key_vectors:
            data_list.append((key, vec))
    return data_list


def tuple2dict(data):
    data_dict = {}
    for key, vec in data:
        if key not in data_dict:
            data_dict[key] = []
        data_dict[key].append(vec)
    data_dict = {key: np.stack(value) for key, value in data_dict.items()}
    return data_dict


def cosine_similarity(input_array, array_to_compare):
    input_norm = np.linalg.norm(input_array, axis=1)[:, np.newaxis]
    array_norm = np.linalg.norm(array_to_compare, axis=1)
    dot_product = np.dot(input_array, array_to_compare.T)
    similarities = dot_product / (input_norm * array_norm)
    return similarities


def cosine_distance(input_array, array_to_compare):
    input_norm = np.linalg.norm(input_array, axis=1)[:, np.newaxis]
    array_norm = np.linalg.norm(array_to_compare, axis=1)
    dot_product = np.dot(input_array, array_to_compare.T)
    similarities = dot_product / (input_norm * array_norm)
    distances = 1 - similarities
    return distances


def dot_product(input_array, array_to_compare):
    dot_products = np.dot(array_to_compare, input_array.T)
    return dot_products.flatten()


def euclidean_distance(input_array, array_to_compare):
    distances = np.linalg.norm(array_to_compare - input_array, axis=1)
    return distances
