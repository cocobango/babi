from .tests_imports import * 
from django.core.urlresolvers import reverse
from ..decorators import *
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

    def test_block_irrelevant_employer_to_employee_get(self):
        #arrange
        employer = Employer.objects.first()
        employee = factories.EmployeeFactory()
        current_view = reverse('reports:edit_specific_entry_by_employer', kwargs={'employee_user_id': employee.user.id})
        self.c.login(password=self.password , username=employer.user.username)

        #act
        response = self.c.get(current_view)

        #assert
        self.assertTrue( response.status_code != 200)

    def test_block_irrelevant_employer_to_employee_post(self):
        #arrange
        current_view = reverse('reports:set_as_valid')
        employer = Employer.objects.first()
        employee = factories.EmployeeFactory()
        self.c.login(password=self.password , username=employer.user.username)

        #act
        response = self.c.post(current_view, {'employee_user_id': employee.user.id, 'entry_id': 1, 'for_year': 2015, 'for_month':1})

        #assert
        self.assertTrue( response.status_code != 200)
        self.assertNotIn('is_okay' , response.content.decode('utf-8'))

    def test_allow_relevant_employer_to_employee_get(self):
        #arrange
        employer = Employer.objects.first()
        employee = factories.EmployeeFactory(employer=employer)
        current_view = reverse('reports:edit_specific_entry_by_employer', kwargs={'employee_user_id': employee.user.id})
        self.c.login(password=self.password , username=employer.user.username)

        #act
        response = self.c.get(current_view)
        #assert
        self.assertTrue( response.status_code == 200)

    def test_allow_relevant_employer_to_employee_post(self):
        #arrange
        current_view = reverse('reports:set_as_valid')
        employer = Employer.objects.first()
        employee = factories.EmployeeFactory(employer=employer)
        self.c.login(password=self.password , username=employer.user.username)

        #act
        response = self.c.post(current_view, {'employee_user_id': employee.user.id, 'entry_id': 1, 'for_year': 2015, 'for_month':1})

        #assert
        self.assertTrue( response.status_code == 200)
        self.assertIn('is_okay' , response.content.decode('utf-8'))

    def test_decorator_class(self):

        @tester(1,2)
        def like_a_view_function(request, *args, **kwargs):
            pass
            # print('inside the view like function')
            # print(args)
            # print(kwargs)

        like_a_view_function(1, 2, 3)


    def test_validate_non_admin_users_cannot_generate_historic_reports(self):
        #arrange
        current_view = reverse('reports:store_data_gui')
        employer = Employer.objects.first()
        self.c.login(password=self.password , username=employer.user.username)

        #act
        response = self.c.get(current_view)

        #assert
        self.assertTrue( response.status_code != 200)
        self.assertNotIn('יצר מידע לאחר הזנה היסטורית' , response.content.decode('utf-8'))
