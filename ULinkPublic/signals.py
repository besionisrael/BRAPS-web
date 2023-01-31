from django.utils import timezone
from ULinkPublic.models import VdxPaper 
from ULinkAdmin.models import RqPaper, WkfHistoric
from django.db.models.signals import post_save



def signal_vdxpaper_submitted(sender, instance, created, **kwars):
    '''Signal Créant une instance De RQPaper quand VDXPaper is Submitted
    means VdxPaper cpState = 2'''
    try:
        if instance.currentState == 2:
            vdxPaperRef = str(instance.paperNumber + str(instance.issuer)).replace(" ", "")
            rqpaper = RqPaper.createInstance(instance.paperNumber, 
                                   vdxPaperRef,
                                   instance.lines,
                                   instance.fullname,
                                   instance.nid,
                                   instance.nvh,
                                   instance.nas,
                                   instance.operator,
                                   instance.issuer
                                     )
            if rqpaper:
                WkfHistoric.createInstance(rqpaper = rqpaper, cpState = instance.currentState )
    except Exception as e:
        print(f"Signal VdX Paper Submitted to Create RQ Paper failed",e)

post_save.connect(signal_vdxpaper_submitted,sender=VdxPaper)