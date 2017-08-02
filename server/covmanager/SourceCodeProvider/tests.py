'''
Tests

@author:     Christian Holler (:decoder)

@license:

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

@contact:    choller@mozilla.com
'''

import json
import os
import unittest

from GITSourceCodeProvider import GITSourceCodeProvider
from HGSourceCodeProvider import HGSourceCodeProvider

class TestGITSourceCodeProvider(unittest.TestCase):
    def setUp(self):
        self.location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-git")
        os.rename(os.path.join(self.location, "git"), os.path.join(self.location, ".git"))

    def tearDown(self):
        os.rename(os.path.join(self.location, ".git"), os.path.join(self.location, "git"))

    def runTest(self):
        provider = GITSourceCodeProvider(self.location)

        tests = {
            "a.txt" : {
                "dcbe8ca3dafb34bc90984fb1d74305baf2c58f17" : "Hello world\n",
                "474f46342c82059a819ce7cd3d5e3e0695b9b737" : "I'm sorry Dave,\nI'm afraid I can't do that.\n"
            },
            "abc/def.txt" : {
                "deede1283a224184f6654027e23b654a018e81b0" : "Hi there!\n\nI'm a multi-line file,\n\nnice to meet you.\n",
                "474f46342c82059a819ce7cd3d5e3e0695b9b737" : "Hi there!\n\nI'm a multi-line file,\n\nnice to meet you.\n"
            }
        }

        for filename in tests:
            for revision in tests[filename]:
                self.assertTrue(provider.testRevision(revision), "Revision %s is unknown" % revision)
                self.assertEqual(provider.getSource(filename, revision), tests[filename][revision])

class TestHGSourceCodeProvider(unittest.TestCase):
    def setUp(self):
        self.location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-hg")
        os.rename(os.path.join(self.location, "hg"), os.path.join(self.location, ".hg"))

    def tearDown(self):
        os.rename(os.path.join(self.location, ".hg"), os.path.join(self.location, "hg"))

    def runTest(self):
        provider = HGSourceCodeProvider(self.location)

        # c179ace9e260adbabd17426750b5a62403691624
        # 7a6e60cac4556610ac95734284d4a3ac08bed15c
        # 05ceb4ce5ed96a107fb40e3b39df7da18f0780c3
        # c3abaa766d52f438219920d37461b341321d4fef

        tests = {
            "a.txt" : {
                "c3abaa766d52f438219920d37461b341321d4fef" : "Hello world\n",
                "c179ace9e260adbabd17426750b5a62403691624" : "I'm sorry Dave,\nI'm afraid I can't do that.\n"
            },
            "abc/def.txt" : {
                "05ceb4ce5ed96a107fb40e3b39df7da18f0780c3" : "Hi there!\n\nI'm a multi-line file,\n\nnice to meet you.\n",
                "c179ace9e260adbabd17426750b5a62403691624" : "Hi there!\n\nI'm a multi-line file,\n\nnice to meet you.\n"
            }
        }

        for filename in tests:
            for revision in tests[filename]:
                self.assertTrue(provider.testRevision(revision), "Revision %s is unknown" % revision)
                self.assertEqual(provider.getSource(filename, revision), tests[filename][revision])

if __name__ == "__main__":
    unittest.main()
