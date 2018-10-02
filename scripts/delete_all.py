#scripts/delete_all.py

from bill.models import Bill, Category, AssociatedAct, Origin, Stage, Sponsor, Deputy, Senator, Constituency, Party, Panel

def run():
    b = Bill.objects.all()
    c = Category.objects.all()
    o = Origin.objects.all()
    s = Stage.objects.all()
    sp = Sponsor.objects.all()
    d = Deputy.objects.all()
    sen = Senator.objects.all()
    con = Constituency.objects.all()
    party = Party.objects.all()
    pan = Panel.objects.all()
    act = AssociatedAct.objects.all()
    b.delete()
    c.delete()
    o.delete()
    s.delete()
    sp.delete()
    d.delete()
    sen.delete()
    con.delete()
    party.delete()
    pan.delete()
    act.delete()
