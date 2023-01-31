from ast import operator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User, Group

# M O D E L    O F   M Y   S M A R T   C O N T R A C T
cpState =    (
    (1, "CREATED"),
    (2, "ISSUED"),
    (3, "CHECKED"),
    (4, "TREATED"),
    (5, "PAID"),
    (6, "RECEIVED"),
    (7, "DELIVERED")
)

TypeTransaction =    (
    (1, "Create"),
    (2, "Issue"),
    (3, "Check"),
    (4, "Treat"),
    (5, "Pay"),
    (6, "Receive"),
    (7, "Deliver"),
)


# Create your models here.


#BD Squelette, En vérité, ceci sera repliquée sur le chaincode
class VdxPaper(models.Model):
    '''VDX Paper SC'''
    paperNumber = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    issuer = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'issuer_request', null = True, blank = True) #OneTimeSaving
    fullname = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    nas = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    operator = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'auteur_request', null = True, blank = True) #ChangingSaving (Getting the value of the next One Each time!)
    nid = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving #Num Identification
    nvh = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving #Nbr véhicule
    lines = models.CharField(max_length = 3000, null = True, blank=True, default = '') #Serialisation de la liste des marques
    currentState = models.IntegerField(choices = cpState) #ChangingSaving
    createDateTime = models.DateTimeField(blank = True, null = True) #Creation Date
    issueDateTime = models.DateTimeField(blank = True, null = True) #Start Date
    deliveredDateTime = models.DateTimeField(blank = True, null = True) #End Date
    docImma = models.CharField(max_length = 600, null = True, blank=True, default = '')  #Just Last Document  
    fileNumber = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    created_at  = models.DateTimeField(auto_now_add = True) #issueDateTime
    updated_at  = models.DateTimeField(auto_now = True)
    
    
    def __str__(self):
        return str(self.paperNumber)
    
    def valueCurrentState(self):
        return dict(cpState)[int(self.currentState)]

    def transactions(self):
        try:
            return Transaction.objects.filter(paper = self).order_by("id")
        except Exception as e:
            return []

    @property
    def lastTransaction(self):
        return self.transactions().reverse()[0]
    
    @property
    def vat(self):
        for transaction in self.transactions():
            if transaction.vat: return transaction.vat
        return None

    
    @property
    def files(self):
        try:
            result = []
            for transaction in self.transactions():
                data = {}
                if transaction.docHash:
                    data["valueTxn"] = transaction.valueTxn
                    data["docHash"] = transaction.docHash
                    result.append(data)
            return result
        except Exception as e:
            print(f"Exception on files {e}")
            return []
    

    
    @classmethod
    def createInstance(cls, issuer, paperNumber, createDateTime, nid, nvh, fullname, nas, lines):
        try:
            paper = cls()
            paper.issuer = issuer
            paper.operator = issuer
            paper.paperNumber = paperNumber
            paper.createDateTime = createDateTime
            paper.currentState = 1
            paper.nid = nid
            paper.nvh = nvh
            paper.fullname = fullname
            paper.nas = nas
            paper.lines = lines
            paper.save()
            return paper
        except Exception as e:
            print("dao_paper createInstance: ", e)
            return None
    
    def setCreated(self):
        self.currentState = 1
        self.save()

    def setIssued(self):
        self.currentState = 2
        self.save()
    
    def setChecked(self):
        self.currentState = 3
        self.save()
    
    def setTreated(self):
        self.currentState = 4
        self.save()
    
    def setPaid(self):
        self.currentState = 5
        self.save()
    
    def setReceived(self):
        self.currentState = 6
        self.save()
    
    def setDelivered(self):
        self.currentState = 7
        self.save()
    
    def isCreated(self):
        return self.currentState == 1

    def isIssued(self):
        return self.currentState == 2
    
    def isChecked(self):
        return self.currentState == 3
    
    def isTreated(self):
        return self.currentState == 4
    
    def isPaid(self):
        return self.currentState == 5
    
    def isReceived(self):
        return self.currentState == 6
    
    def isDelivered(self):
        return self.currentState == 7
    
    

class Transaction(models.Model):
    '''Ledger Transactions, Idéalement c'est un NoSQL
    Ce que je fais pour make it looks like a NoStructured Table, I give all property necessary to 
    Execute all Txn possible, in views, it will be like show just all that is visible! 
    Ton Contrat sera ton dao. Ce seul dao, va créer et faire progresser tout le reste.
    Dans cette table, on conserver donc tout ce qui nous est necessaire pour l'audit.'''
    hashTx = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    txn = models.IntegerField(choices = TypeTransaction, default = 1)
    paper = models.ForeignKey(VdxPaper, on_delete= models.CASCADE, related_name = "request_transaction", blank = True, null= True) #MOSTIMPORTANT LINK
    paperNumber = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    issuer = models.CharField(max_length = 600, null = True, blank=True, default = '')
    fullname = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    nas = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    currentOperator = models.CharField(max_length = 600, null = True, blank=True, default = '')#so we can test if the right operator is making the transaction, before giving the hand to the new one
    newOperator = models.CharField(max_length = 600, null = True, blank=True, default = '')
    nid = models.CharField(max_length = 600, null = True, blank=True, default = '')
    nvh = models.CharField(max_length = 600, null = True, blank=True, default = '') 
    lines = models.CharField(max_length = 3000, null = True, blank=True, default = '')
    createdAt = models.DateTimeField(blank = True, null = True) #issueTime, checkedTime://
    docHash = models.ForeignKey("IPFS", on_delete= models.CASCADE, related_name = "dochash_ipfs", blank = True, null= True) #Changement de rôle à chaque étape docIssue, docPay, docCertificate, docImma #Should be treat VarChar
    vat = models.CharField(max_length = 600, null = True, blank=True, default = '')
    payRef = models.CharField(max_length = 600, null = True, blank=True, default = '') #reference de paiement
    fileNumber = models.CharField(max_length = 600, null = True, blank=True, default = '') #OneTimeSaving
    comment = models.CharField(max_length = 600, null = True, blank=True, default = '')

    def __str__(self):
        return str(self.hashTx)


    
    def valueTxn(self):
        return dict(TypeTransaction)[int(self.txn)]




class IPFS(models.Model):
    '''Simulation IPFS'''
    privateUrlDocument = models.CharField(max_length = 1000, null = True, blank=True, default = '')
    publicUrlDocument = models.CharField(max_length = 1000, null = True, blank=True, default = '') #HashLink
    description = models.CharField(max_length = 600, null = True, blank=True, default = '')
    created_at  = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.privateUrlDocument}"

 



############ Looks like I don't really need this!!! I will make it, String Just!
# class LineRequest(models.Model):
#     brand = models.CharField(max_length = 600, null = True, blank=True, default = '')
#     model = models.CharField(max_length = 600, null = True, blank=True, default = '')
#     year = models.IntegerField(null = True, blank=True, default = '')
#     carId = models.CharField(max_length = 600, null = True, blank=True, default = '')
#     plateId = models.CharField(max_length = 600, null = True, blank=True, default = '')
#     request = models.ForeignKey(Request, on_delete=  models.CASCADE, related_name = 'line_of_request')
#     description = models.CharField(max_length = 1000, null = True, blank=True, default = '')
#     created_at  = models.DateTimeField(auto_now_add = True)
#     updated_at  = models.DateTimeField(auto_now = True)
#     auteur      = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'auteur_bon', null = True, blank = True)

    

#     def __str__(self):
#         return str(self.brand)



