from django.test import TestCase
from django.contrib.auth.models import User

class AnonymousUserTestCase(TestCase):
    '''Test cases for anonymous (non-authenticated) users'''
    def test_anon_user_can_visit_home(self):
        '''Ensure the anonymous user is redirected to /login when visiting the root'''
        response = self.client.get('/')
        self.assertRedirects(response, '/login')

    def test_anon_user_can_visit_login(self):
        '''Ensure the anonymous user is redirected to /login when visiting the root'''
        response = self.client.get('/login')
        self.assertEquals(response.status_code, 200)

    def test_anon_user_cannot_visit_submit(self):
        '''Ensure the anonymous user can't view the submission page'''
        response = self.client.get('/submit')
        self.assertRedirects(response, '/login')

    def test_anon_user_cannot_post_submit(self):
        '''Ensure the anonymous user can't POST to the submission page'''
        response = self.client.post('/submit', {})
        self.assertRedirects(response, '/login')

    def test_anon_user_cannot_visit_submissions(self):
        '''Ensure the anonymous user can't access the submissions view (should 
        result in a 302 redirect'''
        response = self.client.get('/submissions')
        self.assertRedirects(response, '/login')

    def test_anon_user_cannot_access_pdf(self):
        '''Ensure the anonymous user can't access the submission_pdf view'''
        response = self.client.get('/submissions/fakeid.pdf')
        self.assertRedirects(response, '/login')

class RegularUserTestCase(TestCase):
    '''Test cases for a regular (non-staff, non-super) authenticated user'''
    def setUp(self):
        User.objects.create_user('regular', password='pass')
        self.client.login(username='regular', password='pass')

    def test_reg_user_can_visit_submit(self):
        response = self.client.get('/submit')
        self.assertEquals(response.status_code, 200)

    def test_reg_user_can_post_submit(self):
        '''Ensure the regular user can POST to the submission page'''
        response = self.client.post('/submit', {})
        self.assertEquals(response.status_code, 200)

    def test_reg_user_cannot_visit_submissions(self):
        '''Ensure the regular user can't access the submissions view (should 
        result in 403 (unauthorized)'''
        response = self.client.get('/submissions')
        self.assertEquals(response.status_code, 403)

    def test_reg_user_cannot_access_pdf(self):
        '''Ensure the regular user can't access the submission_pdf view'''
        response = self.client.get('/submissions/fakeid.pdf')
        self.assertEquals(response.status_code, 403)

class StaffUserTestCase(TestCase):
    '''Test cases for a staff (non-super) authenticated user'''
    def setUp(self):
        User.objects._create_user('staff', None, 'pass', True, False)
        self.client.login(username='staff', password='pass')

    def test_staff_user_can_visit_submissions(self):
        '''Ensure the staff user can access the submissions view'''
        response = self.client.get('/submissions')
        self.assertEquals(response.status_code, 200)