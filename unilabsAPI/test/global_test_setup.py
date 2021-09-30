from lecturer_user.models import Lecturer
from display_item.models import DisplayItem
from item_category.models import ItemCategory
from lab_manager_user.models import LabManager
from lab_assistant_user.models import LabAssistant
from department.models import Department
from student_user.models import Student
from rest_framework.test import APITestCase
from faker import Faker
from admin_user.models import Admin
from lab.models import Lab
from item.models import BorrowLog, Item, LogState
from request.models import Request,RequestItem
from datetime import date


class GlobalTestSetUp(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()

        # Admins for tests
        cls.global_test_admin = Admin.objects.create_admin(
            email='test_admin1@gmail.com'
        )

        cls.global_test_admin_two = Admin.objects.create_admin(
            email='test_admin2@gmail.com'
        )


        # Department for test
        cls.global_test_department = Department.objects.create(
            name='Test Department 1',
            code='TestDepCode1',
        )

        cls.global_test_department_two = Department.objects.create(
            name='Test Department 2',
            code='TestDepCode2',
        )

        # Labs for tests
        cls.global_test_lab = Lab.objects.create(
            name='Test Lab 1',
            department=cls.global_test_department
        )

        cls.global_test_lab_two = Lab.objects.create(
            name='Test Lab 2',
            department=cls.global_test_department_two
        )

        cls.global_test_lab_three = Lab.objects.create(
            name='Test Lab 3',
            department=cls.global_test_department
        )

        # Lab Managers for tests
        cls.global_test_lab_manager = LabManager.objects.create_lab_manager(
            email = cls.fake.email(),
            lab = cls.global_test_lab,
            department = cls.global_test_department
        )

        cls.global_test_lab_manager_two = LabManager.objects.create_lab_manager(
            email = cls.fake.email(),
            lab = cls.global_test_lab_two,
            department = cls.global_test_department_two
        )

        # Lab Assistant for tests
        cls.global_test_lab_assistant = LabAssistant.objects.create_lab_assistant(
            email = cls.fake.email(),
            lab = cls.global_test_lab,
            department = cls.global_test_department
        )

        cls.global_test_lab_assistant_two = LabAssistant.objects.create_lab_assistant(
            email = cls.fake.email(),
            lab = cls.global_test_lab_two,
            department = cls.global_test_department_two
        )


        # Item Categories for tests
        #---------------------------- Item Categories of lab one --------------------------------------
        cls.global_test_item_category=ItemCategory.objects.create(
            name='Test Item Category 1',
            lab=cls.global_test_lab
        )

        cls.global_test_item_category_two=ItemCategory.objects.create(
            name='Test Item Category 2',
            lab=cls.global_test_lab
        )

        cls.global_test_item_category_three=ItemCategory.objects.create(
            name='Test Item Category 3',
            lab=cls.global_test_lab
        )

        #---------------------------- Item Categories of lab two --------------------------------------
        cls.global_test_item_category_four=ItemCategory.objects.create(
            name='Test Item Category 4',
            lab=cls.global_test_lab_two
        )

        # Display Items for tests
        # --------------------- display items of lab one --------------------------------------
        cls.global_test_display_item_one=DisplayItem.objects.create(
            name='Test Display Item 1',
            item_category=cls.global_test_item_category,
            lab=cls.global_test_lab,
            item_count=1, # When request created default value of item count should be >0 so manually setup
        )

        cls.global_test_display_item_two=DisplayItem.objects.create(
            name='Test Display Item 2',
            item_category=cls.global_test_item_category,
            lab=cls.global_test_lab,
            item_count=1,
        )

        cls.global_test_display_item_three=DisplayItem.objects.create(
            name='Test Display Item 3',
            item_category=cls.global_test_item_category_three,
            lab=cls.global_test_lab,
            item_count=1,
        )
        #--------------------display items of lab 2 ---------------------------
        cls.global_test_display_item_four=DisplayItem.objects.create(
            name='Test Display Item 4',
            item_category=cls.global_test_item_category_four,
            lab=cls.global_test_lab_two,
            item_count=1, 
        )

        cls.global_test_display_item_five=DisplayItem.objects.create(
            name='Test Display Item 5',
            item_category=cls.global_test_item_category_four,
            lab=cls.global_test_lab_two,
            item_count=1,
        )

        cls.global_test_display_item_six=DisplayItem.objects.create(
            name='Test Display Item 6',
            item_category=cls.global_test_item_category_four,
            lab=cls.global_test_lab_two,
            item_count=1,
        )

        #Items for test
        # ----------------------------items in lab 1 ----------------------------------------
        cls.global_test_item_one=Item.objects.create(
            display_item=cls.global_test_display_item_one,
            item_category=cls.global_test_item_category,
            lab=cls.global_test_lab
        )

        cls.global_test_item_two=Item.objects.create(
            display_item=cls.global_test_display_item_two,
            item_category=cls.global_test_item_category_two,
            lab=cls.global_test_lab_two
        )

        cls.global_test_item_three=Item.objects.create(
            display_item=cls.global_test_display_item_three,
            item_category=cls.global_test_item_category_three,
            lab=cls.global_test_lab
        )

        #------------------------------------------- items in lab 2 -------------------------------------------------
        cls.global_test_item_four=Item.objects.create(
            display_item=cls.global_test_display_item_four,
            item_category=cls.global_test_item_category_four,
            lab=cls.global_test_lab_two
        )

        cls.global_test_item_five=Item.objects.create(
            display_item=cls.global_test_display_item_five,
            item_category=cls.global_test_item_category_four,
            lab=cls.global_test_lab_two
        )

        cls.global_test_item_six=Item.objects.create(
            display_item=cls.global_test_display_item_six,
            item_category=cls.global_test_item_category_four,
            lab=cls.global_test_lab_two
        )

         # Student for tests
        cls.global_test_student = Student.objects.create_student(
            email = cls.fake.email(),
            student_id = "123321X",
            department = cls.global_test_department
        )

        cls.global_test_student_two = Student.objects.create_student(
            email = cls.fake.email(),
            student_id = "1278Fd21X",
            department = cls.global_test_department
        )

        cls.global_blocked_student_data = {
            'email':cls.fake.email(),
            'student_id': "65745X",
            'department': cls.global_test_department,
            "blocked": True
        }
        cls.global_blocked_student = Student.objects.create_student(
            email = cls.global_blocked_student_data["email"],
            student_id = cls.global_blocked_student_data["student_id"],
            department = cls.global_blocked_student_data["department"]
        )
        cls.global_blocked_student.blocked = cls.global_blocked_student_data["blocked"]
        cls.global_blocked_student.save()
        
        # Lecturer for tests
        cls.global_test_lecturer = Lecturer.objects.create_lecturer(
            email = cls.fake.email(),
            lecturer_id = "1433T1X",
            department = cls.global_test_department,
            permitted_labs = [cls.global_test_lab.id,cls.global_test_lab_two.id]
        )

        cls.global_test_lecturer_two = Lecturer.objects.create_lecturer(
            email = cls.fake.email(),
            lecturer_id = "14TST1X",
            department = cls.global_test_department,
            permitted_labs = [cls.global_test_lab.id]
        )

        cls.global_test_lecturer_three = Lecturer.objects.create_lecturer(
            email = cls.fake.email(),
            lecturer_id = "14TSTFGF",
            department = cls.global_test_department,
            permitted_labs = []
        )

        # requests for test
        cls.global_test_request_one=Request.objects.create(
            lab=cls.global_test_lab,
            student=cls.global_test_student,
            lecturer=cls.global_test_lecturer,
            reason="Sample reason"
        )

        # request items for tests
        cls.global_test_request_item_one=RequestItem.objects.create(
            request=cls.global_test_request_one,
            display_item=cls.global_test_display_item_one,
            student=cls.global_test_student,
            lab=cls.global_test_lab,
            quantity=1
        )

        cls.global_test_request_item_two=RequestItem.objects.create(
            request=cls.global_test_request_one,
            display_item=cls.global_test_display_item_three,
            student=cls.global_test_student,
            lab=cls.global_test_lab,
            quantity=1
        )

        #borrow log for tests
        cls.global_test_borrow_log_one=BorrowLog.objects.create(
            item=cls.global_test_item_one,
            student=cls.global_test_student,
            lab=cls.global_test_lab,
            state=LogState.TEMP_BORROWED,
            due_date=date.today()

        )

        cls.global_test_borrow_log_two=BorrowLog.objects.create(
            item=cls.global_test_item_two,
            student=cls.global_test_student,
            lab=cls.global_test_lab,
            state=LogState.BORROWED,
            due_date=date.today()
        )

        cls.global_test_borrow_log_three=BorrowLog.objects.create(
            item=cls.global_test_item_two,
            student=cls.global_test_student,
            lab=cls.global_test_lab,
            state=LogState.RETURNED,
            due_date=date.today(),
            returned_date=date.today()
        )

        cls.global_test_borrow_log_four=BorrowLog.objects.create(
            item=cls.global_test_item_four,
            student=cls.global_test_student_two,
            lab=cls.global_test_lab_two,
            state=LogState.BORROWED,
            due_date=date.today()
        )

        
        return

    def tearDown(self):
        return super().tearDown()