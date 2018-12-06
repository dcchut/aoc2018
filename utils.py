def load_input(filename):
    # load the input data
    with open(filename, 'r') as fh:
        data = fh.read()

    return data.split('\n')
