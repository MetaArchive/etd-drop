import os
import urllib2

import requests  # pip install requests


def bag_describe(url, bag_path):
    '''Describes a bag using an instance of the DAITSS Format Description
    Service running at url. Creates a 'premis' tag directory in bag's root
    containing description service outputs per file in bag payload.

    Note: If you have a tagmanifest, you should use a BagIt utility to update
    it after this operation. Otherwise, these tags will not be accounted for.

    url - e.g. "http://localhost:3000"
    bag_path - Path to the top level of a BagIt bag
    '''
    bag_path = os.path.abspath(bag_path)
    data_dir = os.path.join(bag_path, 'data')
    describe_url = "%s/describe" % url

    if not os.path.isdir(bag_path):
        raise Exception("Not a valid path to a directory: %s" % bag_path)
    if not os.path.isdir(os.path.join(bag_path, 'data')):
        raise Exception("Bag contains no data directory: %s" % bag_path)
    if not os.path.isfile(os.path.join(bag_path, 'bagit.txt')):
        raise Exception("Bag path contains no bagit.txt file: %s" % bag_path)

    # Verify description service is reachable
    if urllib2.urlopen(url).getcode() is not 200:
        raise Exception(
            "Description service not reachable at given URL: %s" % url
        )

    # Walk through all files/directories
    os.chdir(data_dir)
    for dirpath, dirnames, filenames in os.walk('.'):
        current_dir = os.path.join(bag_path, 'premis', dirpath)
        os.makedirs(current_dir)
        for filename in filenames:
            extension = os.path.splitext(filename)[1]
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r') as document:
                r = requests.post(
                    describe_url,
                    files={'document': document},
                    data={'extension': extension}
                )
                with open(os.path.join(current_dir, filename+'.xml'), 'w') as premis:
                    premis.write(r.text)
