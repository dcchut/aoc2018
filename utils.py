import multiprocessing

from joblib import Parallel, delayed


def load_input(filename):
    # load the input data
    with open(filename, 'r') as fh:
        data = fh.read()

    return data.split('\n')


def parallel_map(inputs, fn, unpack=False):
    num_cores = multiprocessing.cpu_count()

    # if the unpack parameter is true, then unpack each input into our function
    if unpack:
        return Parallel(n_jobs=num_cores)(delayed(fn)(*q) for q in inputs)
    else:
        return Parallel(n_jobs=num_cores)(delayed(fn)(q) for q in inputs)
