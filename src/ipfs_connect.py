import ipfsapi
api = ipfsapi.connect('127.0.0.1', 5001)


def add_to_ipfs(my_data_file):
    try:
        data_hash = api.add(my_data_file)['Hash']
        return data_hash
    except IOError:
        print 'no such file with data'
        return None
    return data_hash


def get_from_ipfs(hash):
    try:
        data = api.cat(hash)
        return data
    except ipfsapi.exceptions.StatusError:
        print 'incorrect hash'
        return None

