from __future__ import unicode_literals
import os
import hashlib
from ULinkBackOffice.dao.dao_utils import dao_utils
from ULinkAdmin.models import RqPaper
from django.utils import timezone
#from ULinkBackOffice.utils.timezone import timezone
from django.conf import settings
from django.core.files.storage import default_storage


class dao_rqpaper(object):
    '''Interaction with IPFS Model'''
     
    @staticmethod
    def toListPapersByCat(label = 1):
        try:
            result = {}
            papers = RqPaper.objects.all()
            print(papers[0].currentState)
            received = [x for x in papers if x.currentState == 1]
            sent = [x for x in papers if x.currentState == 2]
            completed = [x for x in papers if x.currentState == 3]
            result['received'] = { 'number': len(received), 'list': received, 'title': 'Demandes reçues' }
            result['sent'] = { 'number': len(sent), 'list': sent, 'title': 'En cours de traitement' }
            result['completed'] = { 'number': len(completed), 'list': completed, 'title': 'Demandes traitées' }
            result['all'] = {'number': papers.count(), 'list': papers, 'title': 'Toutes les demandes'}
            result['label'] = label
            if label == 2: result['model'] = sent; result['title'] = 'En cours de traitement'
            elif label == 3: result['model'] = completed; result['title'] = 'Demandes traitées'
            elif label == 4: result['model'] = list(papers); result['title'] = 'Toutes les demandes'
            else :result['model'] = received; result['title'] = 'Demandes reçues'
            return result
        except Exception as e:
            print("Get toListRQPapersByCat", e)
            return None
        
    
    @staticmethod
    def toGetPaper(id):
        try:
            return RqPaper.objects.get(pk = id)
        except Exception as e:
            print("Error on toGetPaper", e)
            return None
    
    @staticmethod
    def toSetOperator(id, operator):
        try:
            paper = RqPaper.objects.get(pk = id)
            paper.operator = operator 
            paper.save()
        except Exception as e:
            print("Error on toGetPaper", e)
            return None
    
    @staticmethod
    def toGetPaperByNumberID(numberID):
        try:
            paperNumber = f'PAPER-{numberID}'
            return RqPaper.objects.filter(paperNumber = paperNumber).first()
        except Exception as e:
            print("Error on toGetPaper", e)
            return None
    
    
