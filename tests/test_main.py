# project/test_api.py

import os
import unittest
from datetime import date

from project import app, db
from project._config import basedir


TEST_DB = 'test.db'


class APITests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ###############
    #### tests ####
    ###############

    def test_index(self):
        """ Ensure flask was set up correctly. """
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
