# project/test.py


import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ##########################
    #### helper functions ####
    ##########################
        
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)        

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)
    
    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    ###############
    #### tests ####
    ###############
    
    # each test should start with 'test'
    def test_user_setup(self):
        new_user = User('testrichard', 'richard.wartenburger@gmail.com', 'testrichard')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "testrichard"

    def test_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list', response.data)

    def test_users_can_login(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)
        self.register('richardtest', 'richard.wartenburger@gmail.com', 'richardtestpw', 'richardtestpw')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)        
        response = self.login('richardtest', 'richardtestpw')
        self.assertIn(b'Welcome richardtest!', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register('richardtest', 'richard.wartenburger@gmail.com', 'richardtestpw', 'richardtestpw')
        self.assertIn(b'Thanks for registering. Please', response.data)
        self.app.get('register/', follow_redirects=True)
        response = self.register('richardtest', 'richard.wartenburger@gmail.com', 'richardtestpw', 'richardtestpw')
        self.assertIn(b'That username and/or email already exists.', response.data)     

    def test_logged_in_users_can_logout(self):
        self.register('richardtest', 'richard.wartenburger@gmail.com', 'richardtestpw', 'richardtestpw')
        self.login('richardtest', 'richardtestpw')
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)
        response = self.logout()
        self.assertNotIn(b'Goodbye', response.data)

    def test_default_user_role(self):
        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )
        db.session.commit()
        users = db.session.query(User).all()
        print(users)
        for user in users:
            self.assertEqual(user.role, 'user')
        
if __name__ == "__main__":
    unittest.main()
