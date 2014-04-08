import os

def bag_describe(url, bag_path):
    '''Describes a bag using an instance of the DAITSS Format Description 
    Service running at url.
    
    url - e.g. "http://localhost:3000"
    bag_path - Path to the top level of a BagIt bag
    '''
    bag_path = os.path.abspath(bag_path)
    data_dir = os.path.join(bag_path, 'data')

    if not os.path.isdir(bag_path):
        raise Exception("Not a valid path to a directory: %s" % bag_path)
    if not os.path.isdir(os.path.join(bag_path, 'data')):
        raise Exception("Bag contains no data directory: %s" % bag_path)
    if not os.path.isfile(os.path.join(bag_path, 'bagit.txt')):
        raise Exception("Bag path contains no bagit.txt file: %s" % bag_path)

    # TODO: Verify description service is responsive

    os.chdir(data_dir)
    for dirpath, dirnames, filenames in os.walk('.'):
        os.makedirs(os.path.join(bag_path, 'premis', dirpath))
        for filename in filenames:
            # TODO: Call description service
            pass
