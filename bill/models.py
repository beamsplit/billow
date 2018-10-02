from django.db import models
import datetime



# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=255)
    def __str__(self):
        return self.category

class AssociatedAct(models.Model):
    associated_act = models.TextField(max_length=300)
    def __str__(self):
        return self.associated_act

class Sponsor(models.Model):
    sponsor = models.CharField(max_length=255, default='Sponsor')
    def __str__(self):
        return self.sponsor

class Origin(models.Model):
    origin = models.CharField(max_length=255, default='Origin')
    def __str__(self):
        return self.origin

class Stage(models.Model):
    stage = models.TextField(max_length=255)
    stage_info = models.TextField(max_length=500, default='Stage Info')
    def __str__(self):
        return self.stage

class Constituency(models.Model):
    name = models.CharField(max_length=200)
    con_id = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.name

class Party(models.Model):
    name = models.CharField(max_length=100)
    party_id = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.name

class Panel(models.Model):
    name = models.CharField(max_length=100)
    panel_id = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.name

class Deputy(models.Model):
    name = models.CharField(max_length=100)
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=70,blank=True)
    phone = models.CharField(max_length=20)
    photo = models.URLField(max_length=200,default='')
    url = models.URLField(max_length=200,default='')
    def get_absolute_url(self):
        return reverse('bill:deputy-detail', args=[str(self.id)])
    def __str__(self):
        return self.name

class Senator(models.Model):
    name = models.CharField(max_length=100)
    panel = models.ForeignKey(Panel, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=70,blank=True)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Bill(models.Model):
    title = models.TextField(max_length=300)
    description = models.TextField(max_length=1000)
    category = models.ManyToManyField(Category,help_text='Select a category for this bill')
    sponsor = models.ManyToManyField(Sponsor,help_text='Select a sponsor for this bill')
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True)
    stage = models.ForeignKey(Stage,on_delete=models.SET_NULL, null=True)
    bill_history = models.TextField(max_length=1000,default = '')
    date = models.DateField(max_length=100, default = datetime.datetime.today().strftime('%Y-%m-%d'))
    td = models.ManyToManyField(Deputy,help_text='Select a td for this bill')
    senator = models.ManyToManyField(Senator,help_text='Select a td for this bill')
    associated_act = models.ManyToManyField(AssociatedAct,help_text='Select associated act')
    url = models.URLField(max_length=200,default='')
    updated = models.BooleanField(default = False)
    updated_at = models.DateField(max_length=100, default = datetime.datetime.today().strftime('%Y-%m-%d'))
    def __str__(self):
        return self.title

class Movement(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='movement')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='movement', default=1)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1000)
    url = models.URLField(max_length=200,default='')
    created_date = models.DateField(max_length=100, default=datetime.datetime.today().strftime('%Y-%m-%d'))
    approved_movement = models.BooleanField(default=False)
    
    def approve(self):
        self.approved_movement = True
        self.save()
    
    def __str__(self):
        return self.text




