from __future__ import unicode_literals
import os
import hashlib
from ULinkAdmin.models import WkfHistoric
from ULinkAdmin.dao.dao_rqpaper import dao_rqpaper
from ULinkPublic.dao.dao_transaction import dao_transaction
from django.utils import timezone
#from ULinkBackOffice.utils.timezone import timezone


class dao_historic(object):
    '''WKF Engine Private Operator'''

    @staticmethod
    def sendToPrivate(rqpaper_id, author): 
        '''Sending the received Docs to Private, Simulation of Private WKF Engine
        Update the Status on blockchain to become "Check" on Public Wkf'''
        try:
            paper = dao_rqpaper.toGetPaper(rqpaper_id)
            if paper.currentState == 1:
                objet = dao_transaction.check(paper.issuer, paper.paperNumber, paper.operator, author, timezone.now(), "")
                if objet:
                   WkfHistoric.createInstance(paper, 2)
                   dao_rqpaper.toSetOperator(rqpaper_id, objet.newOperator) 
            return paper
        except Exception as e:
            print("Smart Contract sendToPrivate: ", e)
    
    @staticmethod
    def uploadVDE23(rqpaper_id, file, vat, author):
        '''Uploading the Good Docs VDE23 to issue On Blockchain.
        1st. File is Upload
        2nd. File is sent to Blockchain (dao_transaction)
        3rd. Wkf_historics is MaJ
        '''
        try:
            #retrieving the paper
            paper = dao_rqpaper.toGetPaper(rqpaper_id)
            if paper.currentState == 2:                
                objet = dao_transaction.treat(paper.issuer, paper.paperNumber, paper.operator, author, timezone.now(), file, int(vat))
                if objet: #if transaction in blockchain is done
                    WkfHistoric.createInstance(paper, 3)
            return paper
        except Exception as e:
            print("Smart contract Issue:", e)

    #### OPERATIONAL METHOD CONNECTING TO SMART CONTRACT ONLY
    
    @staticmethod
    def toGetFilesIPFS(issuer, paperNumber):
        try:
            return dao_transaction.getAttachements(issuer, paperNumber)
        except Exception:
            return []
    
    @staticmethod
    def toListAllBlocPapers():
        try:
            return dao_transaction.getAllPapers()
        except Exception:
            return []
    
    @staticmethod
    def toGetBlocPaperTxnID(txnId):
        try:
            return dao_transaction.getPaper(txnId)
        except Exception:
            return None
    
   