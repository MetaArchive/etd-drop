import os
import urllib2
import argparse

import requests  # pip install requests


def bag_describe(url, bag_path):
    '''Describes a bag using an instance of the DAITSS Format Description
    Service running at url. Creates a 'premis' tag directory in bag's root
    containing description service outputs per file in bag payload.

    Note: If you have a tagmanifest, you should use a BagIt utility to update
    it after this operation. Otherwise, these tags will not be accounted for.

    Parameters:
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
    if urllib2.urlopen(url).getcode() != 200:
        raise Exception(
            "Description service not reachable at given URL: %s" % url
        )

    # Walk through all files/directories
    os.chdir(data_dir)
    for dirpath, dirnames, filenames in os.walk('.'):
        current_dir = os.path.join(bag_path, 'premis', dirpath)
        os.makedirs(current_dir)
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r') as document:
                r = requests.post(describe_url, files={'file': document})
                with open(os.path.join(current_dir, filename+'.xml'), 'w') as premis:
                    premis.write(r.text)


def _make_arg_parser():
    parser = argparse.ArgumentParser(
        description="Describe a BagIt bag using the DAITSS Format "
                    "Description Service."
    )
    parser.add_argument(
        'url',
        help="URL of running instance of DAITSS Format Description Service "
             "(e.g. 'http://localhost:3000')"
    )
    parser.add_argument('bag', help="path to the bag being surveyed")
    return parser

if __name__ == "__main__":
    '''Command-line usage:
    python bag-describe.py <URL> <BAG>
    '''
    parser = _make_arg_parser()
    args = parser.parse_args()
    bag_describe(args.url, args.bag)
