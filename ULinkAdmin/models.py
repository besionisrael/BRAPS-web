from ast import operator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User, Group
from django.db import IntegrityError


wkfState =    (
    (1, "RECEIVE"),
    (2, "SEND"),
    (3, "COMPLETE")
)



# Create your models here.


#Table Réel Simulant une intégration du VdxPaper Contrat intelligent to RQ Organization
class RqPaper(models.Model):
    '''RQ Paper Private Object of RQ'''
    paperNumber = models.CharField(max_length = 600, null = True, blank=True, default = '', unique=True) #Getting from SC
    issuer = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'issuer_from_sc', null = True, blank = True) #Getting from SC ISSUER
    operator = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'operator_from_sc', null = True, blank = True) #Getting from SC (OPERATOR)
    vdxPaperRef = models.CharField(max_length = 600, null = True, blank=True, default = '', unique=True) #Getting from SC (PaperNumber + Issuer I guess)
    lines = models.CharField(max_length = 3000, null = True, blank=True, default = '') #Getting from SC
    fullname = models.CharField(max_length = 600, null = True, blank=True, default = '', verbose_name="requester fullname") #Getting from SC
    nas = models.CharField(max_length = 600, null = True, blank=True, default = '', verbose_name="request nas") #Getting from SC
    nid = models.CharField(max_length = 600, null = True, blank=True, default = '', verbose_name="requester nid") #Getting from SC
    nvh = models.CharField(max_length = 600, null = True, blank=True, default = '') #Getting from SC
    lines = models.CharField(max_length = 3000, null = True, blank=True, default = '') #Getting from SC
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at  = models.DateTimeField(auto_now = True)
    
    
    def __str__(self):
        return str(self.paperNumber)
    
    @classmethod
    def createInstance(cls, paperNumber, vdxPaperRef,  lines, fullname, nas, nid, nvh, operator = None, issuer = None ):
        try:
            paper = cls()
            paper.paperNumber = paperNumber
            paper.vdxPaperRef = vdxPaperRef
            paper.lines = lines
            paper.fullname = fullname
            paper.nid = nid
            paper.nvh = nvh
            paper.nas = nas
            paper.operator = operator
            paper.issuer = issuer
            paper.save()
            return paper
        except IntegrityError as e:
            print(f"Related RQ Paper is already Created! ")
        except Exception as e:
            print("dao_rqpaper createInstance: ", e)
            print("Exception ClassName", e.__class__.__name__)
            return None
    
    def historics(self):
        return WkfHistoric.objects.filter(rqpaper = self).order_by("id")

    @property
    def currentState(self):
        return self.historics().reverse()[0].workflowState
    @property
    def valueCurrentState(self):
        return dict(wkfState)[int(self.currentState)]
    
    
class WkfHistoric(models.Model):
    '''Historique de progression de Workflow privé propre à RQ'''
    rqpaper = models.ForeignKey(RqPaper, on_delete= models.CASCADE, related_name = "rq_paper", blank = True, null= True) #Link to Our RQPaper
    workflowState = models.IntegerField(choices = wkfState) #Internal Workflow Champ of RQ 
    description = models.CharField(max_length = 600, null = True, blank=True, default = '')
    created_at  = models.DateTimeField(auto_now_add = True) 
    updated_at  = models.DateTimeField(auto_now = True)
    
    
    def __str__(self):
        return f'{self.rqpaper.paperNumber} {self.valueWorkflowState()}'
        
    def valueWorkflowState(self):
        return dict(wkfState)[int(self.workflowState)]
    
    @classmethod
    def createInstance(cls, rqpaper, wkfState = None, cpState = None, description = None):
        try:
            historic = cls()
            historic.rqpaper = rqpaper
            historic.description = description
            #cpState is the state of Smart Contract workflow
            #by default = 2, because it's the state related to public state "issued to RQ"
            if cpState == 2:
                historic.workflowState = 1                
            elif wkfState:
                historic.workflowState = wkfState
            else:
                raise Exception(f"Value of CpState {cpState} and wkfState {wkfState} cannot be set")
            historic.save()
            return historic
        except Exception as e:
            print("dao_wkf_historique createInstance: ", e)
            return None
