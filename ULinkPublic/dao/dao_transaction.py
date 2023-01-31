from __future__ import unicode_literals
import requests
import json
import hashlib
from ULinkPublic.models import Transaction, VdxPaper
from ULinkPublic.dao.dao_ipfs import dao_ipfs
from django.utils import timezone
from AppUlink.settings import API_PUBLIC, API_ADMIN, API_PARTNER




class dao_transaction(object):
    '''Smart Contract Interaction'''

    @staticmethod
    def convertDataPost(**kwargs):
        return kwargs

    @staticmethod
    def create(issuer, paperNumber, createDateTime, nid, nvh, fullname, nas, lines = "", file = ""):
        '''Chaincode Ctx Context Param initializing the SC'''

        try:
            docHash = dao_ipfs.toUploadDocument(file) #Getting the Hash from IPFS
            paper = VdxPaper.createInstance(issuer, paperNumber, createDateTime, nid, nvh, fullname, nas, lines)
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, createDateTime = createDateTime.strftime('%Y-%m-%d %H:%M:%S'), nid = nid,
                nvh = nvh, fullname = fullname, nas = nas, lines = lines, docHash = docHash.publicUrlDocument
            )
            response = requests.post(f'{API_PUBLIC}/api/create', json = data).json()
            hashTx = response["response"]["TxID"] #hashlib.sha256(str(issueDateTime).encode("utf-8")).hexdigest()
            ### End SC Request
            Transaction(
                hashTx = hashTx, 
                txn = 1, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = issuer, newOperator = issuer, 
                lines = lines, docHash = docHash, createdAt = createDateTime
            ).save()
            return paper
        except Exception as e:
            print("Smart Contract create: ", e)
    
    @staticmethod
    def issue(issuer, paperNumber, currentOperator, newOperator, issueDateTime ):
        '''Nota: CurrentOperator is the old one, on the request, the requester of issue method 
        should know who is the current operator by getting info in paper object. Same for other'''
        try:
            #retrieving the paper
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            if paper.operator != currentOperator:
                raise Exception(f"Paper {paperNumber} is not operate by {currentOperator}")
            if paper.isCreated():
                paper.setIssued()
            if paper.isIssued():
                paper.operator = newOperator
                paper.issueDateTime = issueDateTime
                paper.save()
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, issueDateTime = issueDateTime.strftime('%Y-%m-%d %H:%M:%S')
            )
            response = requests.post(f'{API_PUBLIC}/api/issue', json = data).json()
            hashTx = response["response"]["TxID"]
            ### End SC Request
            Transaction(
                hashTx = hashTx,
                txn = 2, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = currentOperator, newOperator = newOperator,
                createdAt = issueDateTime
            ).save()
            return paper
        except Exception as e:
            print("Smart contract Issue:", e)
    
    @staticmethod
    def check(issuer, paperNumber, currentOperator, newOperator, checkDateTime, comment ):
        
        try:
            #retrieving the paper
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            if paper.operator != currentOperator:
                raise Exception(f"Paper {paperNumber} is not operate by {currentOperator}")
            if paper.isIssued():
                paper.setChecked()
            if paper.isChecked():
                paper.operator = newOperator
                paper.save()
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, checkDateTime = checkDateTime.strftime('%Y-%m-%d %H:%M:%S'),
                comment = comment
            )
            response = requests.post(f'{API_ADMIN}/api/check', json = data).json()
            hashTx = response["response"]["TxID"]
            ### End SC Request
            transaction = Transaction(
                hashTx =hashTx,
                txn = 3, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = currentOperator, newOperator = newOperator,
                createdAt = checkDateTime, comment = comment
            )
            transaction.save()
            return transaction
        except Exception as e:
            print("Smart contract Check:", e)
    
    @staticmethod
    def treat(issuer, paperNumber, currentOperator, newOperator, treatDateTime, file, vat ):
        
        try:
            #retrieving the paper
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            
            if paper.operator != currentOperator:
                raise Exception(f"Paper {paperNumber} is not operate by {currentOperator}")
            if paper.isChecked():
                paper.setTreated()
            docHash = dao_ipfs.toUploadDocument(file) #Getting the Hash from IPFS
            if paper.isTreated():
                paper.operator = newOperator
                paper.save()
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, treatDateTime = treatDateTime.strftime('%Y-%m-%d %H:%M:%S'),
                docHash = docHash.publicUrlDocument, vat = vat
            )
            response = requests.post(f'{API_ADMIN}/api/treat', json = data).json()
            hashTx = response["response"]["TxID"]
            ### End SC Request

            Transaction(
                hashTx = hashTx,
                txn = 4, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = currentOperator, newOperator = newOperator,
                createdAt = treatDateTime, vat = vat, docHash = docHash
            ).save()
            return paper
        except Exception as e:
            print("Smart contract Treat:", e)

    @staticmethod
    def pay(issuer, paperNumber, currentOperator, newOperator, payDateTime, file, reference ):
        
        try:
            #retrieving the paper
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            if paper.operator != currentOperator:
                raise Exception(f"Paper {paperNumber} is not operate by {currentOperator}")
            if paper.isTreated():
                paper.setPaid()
            docHash = dao_ipfs.toUploadDocument(file) #Getting the Hash from IPFS
            if paper.isPaid():
                paper.operator = newOperator
                paper.save()
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, payDateTime = payDateTime.strftime('%Y-%m-%d %H:%M:%S'),
                docHash = docHash.publicUrlDocument, reference = paperNumber
            )
            response = requests.post(f'{API_PUBLIC}/api/pay', json = data).json()
            hashTx = response["response"]["TxID"]
            ### End SC Request

            Transaction(
                hashTx = hashTx,
                txn = 5, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = currentOperator, newOperator = newOperator,
                createdAt = payDateTime, payRef = reference, docHash = docHash
            ).save()
            return paper
        except Exception as e:
            print("Smart contract Pay:", e)
    
    @staticmethod
    def receive(issuer, paperNumber, currentOperator, newOperator, receiveDateTime, comment ):
        
        try:
            #retrieving the paper
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            if paper.operator != currentOperator:
                raise Exception(f"Paper {paperNumber} is not operate by {currentOperator}")
            if paper.isPaid():
                paper.setReceived()
            if paper.isReceived():
                paper.operator = newOperator
                paper.save()
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, receiveDateTime = receiveDateTime.strftime('%Y-%m-%d %H:%M:%S'),
                comment = comment
            )
            response = requests.post(f'{API_PARTNER}/api/receive', json = data).json()
            hashTx = response["response"]["TxID"]
            ### End SC Request
            Transaction(
                hashTx = hashTx,
                txn = 6, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = currentOperator, newOperator = newOperator,
                createdAt = receiveDateTime, comment = comment
            ).save()
            return paper
        except Exception as e:
            print("Smart contract Receive:", e)
    
    @staticmethod
    def deliver(issuer, paperNumber, currentOperator, newOperator, deliverDateTime, fileNumber, file ):
        
        try:
            #retrieving the paper
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            
            if paper.operator != currentOperator:
                raise Exception(f"Paper {paperNumber} is not operate by {currentOperator}")
            if paper.isReceived():
                paper.setDelivered()
            docHash = dao_ipfs.toUploadDocument(file) #Getting the Hash from IPFS
            if paper.isDelivered():
                paper.operator = newOperator
                paper.deliveredDateTime = deliverDateTime
                paper.fileNumber = fileNumber
                paper.docImma = docHash
                paper.save()
            
            ### SC Request
            data = dao_transaction.convertDataPost(
                paperNumber = paperNumber, deliverDateTime = deliverDateTime.strftime('%Y-%m-%d %H:%M:%S'),
                fileNumber = fileNumber, docImma = docHash.publicUrlDocument
            )
            response = requests.post(f'{API_PARTNER}/api/deliver', json = data).json()
            hashTx = response["response"]["TxID"]
            ### End SC Request

            Transaction(
                hashTx = hashTx,
                txn = 7, paper = paper, paperNumber = paperNumber,
                issuer = issuer, currentOperator = currentOperator, newOperator = newOperator,
                createdAt = deliverDateTime, docHash = docHash
            ).save()
            return paper
        except Exception as e:
            print("Smart contract Deliver:", e)
    
    ### Method from Contract about Getting State on Node Ledger
    @staticmethod
    def getPaper(ref):
        try:
            return VdxPaper.objects.get(pk = ref)
        except Exception as e:
            return None
    
    ### Method from Contract about getting State from paperNumber
    @staticmethod
    def getPaperByPaperNumber(paperNumber):
        try:
            return VdxPaper.objects.filter(paperNumber = paperNumber).first()
        except Exception as e:
            return None
    
    #Method Only for SAAQ according to the state
    @staticmethod
    def getPaperByPaperNumberSAAQ(paperNumber):
        try:
            return VdxPaper.objects.filter(paperNumber = paperNumber, currentState = 5).first()
        except Exception as e:
            return None
    
   

    ################## STANDARD METHOD

    @staticmethod
    def getPapersOfIssuer(issuer):
        try:
            return VdxPaper.objects.filter(issuer = issuer)
        except Exception as e:
            return []
    
    @staticmethod
    def getPapersOfState(currentState):
        try:
            return VdxPaper.objects.filter(currentState = currentState)
        except Exception as e:
            return []
    
    @staticmethod
    def getAllPapers():
        try:
            return VdxPaper.objects.all()
        except Exception as e:
            return [None]

    
    @staticmethod
    def getAttachements(issuer, paperNumber):
        try:
            paper = VdxPaper.objects.filter(paperNumber = paperNumber, issuer = issuer).first()
            return paper.files
        except Exception:
            return []






    
    
