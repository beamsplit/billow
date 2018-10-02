from django.test import TestCase

from bill.models import Bill, Category, AssociatedAct, Sponsor, Origin, Stage

# Create your tests here.

class BillModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        
        Category.objects.create(category = 'Health')
        AssociatedAct.objects.create(associated_act = 'Personal Injuries Assessment Board Act 2003')
        Sponsor.objects.create(sponsor = 'Minister for Business')
        Origin.objects.create(origin = 'Dáil Éireann')
        Stage.objects.create(stage = 'Dáil First Stage', stage_info = 'The Bill is initiated or presented to the House')
        Bill.objects.create(title = 'PERSONAL INJURIES ASSESSMENT BOARD (AMENDMENT) (NO. 2) BILL 2018', description = 'Bill entitled an Act to amend and extend the Personal Injuries Assessment Board Act 2003.')

    def test_title_label(self):
        bill = Bill.objects.get(id=1)
        field_label = bill._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_title_max_length(self):
        bill = Bill.objects.get(id=1)
        max_length = bill._meta.get_field('title').max_length
        self.assertEquals(max_length, 300)

    def test_updated_boolean_flag(self):
        bill = Bill.objects.get(id=1)
        updated = bill._meta.get_field('updated').default
        self.assertEquals(updated, False)








