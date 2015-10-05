from .tests_imports import * 

class PermissionsTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(PermissionsTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
        self.c = Client()
        self.password = '123456'

    def setUp(self):
        self.myGenerator.generateInitialControlledState()


    def test_will_not_allow_access_to_a_secure_page_to_a_user_not_logged_in(self):
        #arrange
        
        #act
        response = self.c.get('/reports/')
        #assert
        self.assertTrue(response.status_code != 200)
        # self.assertTrue(False)

    def test_will_allow_access_to_a_user_not_logged_in_to_login_page(self):
        #arrange
        
        #act
        response = self.c.get('/')
        #assert
        self.assertTrue(response.status_code == 200)
        # self.assertTrue(False)

    def test_will_allow_access_to_a_secure_page_to_a_user_that_is_logged_in(self):
        #arrange
        password = 12345678
        username = 'coco'
        user = factories.UserFactory(password=password , username=username)
        employer = factories.EmployerFactory(user=user)
        self.c.login(password=password , username=username)
        #act
        response = self.c.get('/reports/')
        #assert
        self.assertTrue(response.status_code == 200)
        # self.assertTrue(False)

    def test_will_allow_access_to_edit_a_specific_entry_for_the_said_employee_while_logged_in_as_employer_GET(self):
        #arrange
        employer = Employer.objects.first()
        views_list = ['/reports/','/',]
        self.c.login(password=self.password , username=employer.user.username)

        #act + #assert
        for current_view in views_list:
            response = self.c.get(current_view)
            self.assertTrue( response.status_code == 200 , msg='current_view: {0}'.format(current_view))

    @unittest.skip("not implemented")
    def test_validate_is_relevant_employer_to_employee(self):
        #arrange
        current_view = '/my_test/'
        employer = Employer.objects.first()
        self.c.login(password=self.password , username=employer.user.username)

        #act
        response = self.c.get(current_view)

        #assert
        self.assertTrue( response.status_code == 200)
        self.assertIn('i am in the view' , response.content.decode('utf-8'))
