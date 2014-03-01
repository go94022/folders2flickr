"""
Test case for tags2set.py
"""
import logging
import sys
import os
try:
    inifile = open('uploadr.ini', 'w')
    sample = open('../uploadr.ini.sample', 'r')
    inifile.write(sample.read())
    inifile.close()
except IOError:
    sys.exit(1)
sys.path.append('..')
import unittest
import tempfile
import fakeflickr
import shelve
import f2flickr.tags2set

def addinvert(dictthing):
    """
    Add the keys and values, but inverted to the dictionary
    """
    keys = dictthing.keys()
    for key in keys:
        newkey = dictthing[key]
        dictthing[newkey] = key

class Tags2SetTest(unittest.TestCase):
    """
    Test suite for tags2set.py
    """

    def testSetIsUpdated(self):
        """
        Check that when updating in batches, the set is updated.
        First upload 20 photos, then upload some more, up to 44
        The 44 should be in the set.
        """
        historyFile = tempfile.mktemp()
        fakeuploaded = shelve.open(historyFile)
        for i in range(1, 21):
            fakeuploaded[str(i)] = 'random/img%d.jpg' % i

        addinvert(fakeuploaded)
        fakeuploaded.close()

        uploaded = [str(r) for r in range(1, 21)]
        f2flickr.tags2set.createSets(uploaded, historyFile)
        user = fakeflickr.fakelogin()
        self.assertEquals(1, len(user.getPhotosets()))

        fakeuploaded = shelve.open(historyFile)
        for i in range(1, 45):
            fakeuploaded[str(i)] = 'random/img%d.jpg' % i
        addinvert(fakeuploaded)
        fakeuploaded.close()

        uploaded = [str(r) for r in range(22, 45)]
        f2flickr.tags2set.createSets(uploaded, historyFile)
        user = fakeflickr.fakelogin()
        self.assertEquals(1, len(user.getPhotosets()))

        ps = user.getPhotosets()[0]
        photos = ps.getPhotos()
        self.assertEquals(44, len(photos))

        os.remove(historyFile)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                filename='debug.log',
                filemode='w')
    logging.debug('Started')
    unittest.main()