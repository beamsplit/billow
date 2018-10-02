from django.contrib import admin

# Register your models here.

from .models import Bill, Category, AssociatedAct, Sponsor, Origin, Stage, Deputy, Senator, Constituency, Party, Panel, Movement

admin.site.register(Bill)
admin.site.register(Movement)
admin.site.register(Category)
admin.site.register(AssociatedAct)
admin.site.register(Sponsor)
admin.site.register(Origin)
admin.site.register(Stage)
admin.site.register(Deputy)
admin.site.register(Senator)
admin.site.register(Constituency)
admin.site.register(Party)
admin.site.register(Panel)

