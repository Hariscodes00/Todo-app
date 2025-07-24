import unittest
from app import app

class FlaskTodoAppTest(unittest.TestCase):

    def setUp(self):
        # Setup runs before each test
        self.app = app.test_client()
        self.app.testing = True

    def test_signup_page_loads(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Form', response.data)

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_home_redirects_without_login(self):
        response = self.app.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/signup', response.location)

    def test_otp_page_loads(self):
        response = self.app.get('/otp')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OTP Verification', response.data)

    def test_logout_redirects(self):
        response = self.app.get('/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_delete_action(self):
        with self.app:
            self.app.post('/login', data={
                'username': 'haris_00',
                'password': '1010'
            }, follow_redirects=True)

            self.app.post('/', data = {
                'title':'Delete',
                'desc':'Testing Delete'
            }, follow_redirects = True)

            from app import Todo
            todo = Todo.query.filter_by(title = 'Delete').first()
            self.assertIsNotNone(todo)

            response = self.app.get(f'/delete/{todo.sno}' , follow_redirects = True)
            self.assertEqual(response.status_code , 200)

    def test_update_action(self):
        with self.app:
            self.app.post('/login', data={
                'username': 'haris_00',
                'password': '1010'
            }, follow_redirects=True)

            self.app.post('/', data = {
                'title':'Delete',
                'desc':'Testing Delete'
            }, follow_redirects = True)

            self.app.post('/', data= {
                'title':'Update' ,
                'desc' : 'Testing update'
            }, follow_redirects = True)

            from app import Todo
            todo = Todo.query.filter_by(title = 'Update').first()
            self.assertIsNotNone(todo)

            response = self.app.get(f'/update/{todo.sno}' , follow_redirects = True)
            self.assertEqual(response.status_code , 200)


if __name__ == '__main__':
    unittest.main()
