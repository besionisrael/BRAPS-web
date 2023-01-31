# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ULinkBackOffice.models import Wkf_Transition, Wkf_Etape
from ULinkBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow

from django.utils import timezone

class dao_wkf_transition(object):
    id = 0
    etape_source_id	= None
    etape_destination_id = None
    role_utilisateur_id = None
    condition_id = None
    url = ""
    num_ordre = ""
    traitement = ""
    unite_fonctionnelle_id = None

    @staticmethod
    def toListTransitions():
        return Wkf_Transition.objects.all()

    @staticmethod
    def toListTransitionsOfWorkflow(workflow_id):
        #print(workflow_id)  
        return Wkf_Transition.objects.filter(etape_destination__workflow_id = workflow_id).order_by('num_ordre')

    @staticmethod
    def toListTransitionsOfSource(etape_id,service_referent_id=0):
        if service_referent_id == 0:
            return Wkf_Transition.objects.filter(etape_source_id = etape_id)
        else:
            return Wkf_Transition.objects.filter(etape_source_id = etape_id).filter(unite_fonctionnelle_id = service_referent_id)

    """
    @staticmethod
    def toListTransitionsOfWorkflow(workflow_id):
        workflow = dao_wkf_workflow.toGetWorkflow(pk = workflow_id)
        etapes = dao_wkf_etape.toListEtapeOfWorkflows(workflow.id)

        data = []

        for etape in etapes:

            """

    @staticmethod
    def toCreateTransition(etape_source_id , etape_destination_id, role_utilisateur_id, condition_id, url, num_ordre, traitement = "", unite_fonctionnelle_id = None):        
        try:
            transition = dao_wkf_transition()
            transition.etape_source_id = etape_source_id
            transition.etape_destination_id = etape_destination_id
            transition.role_utilisateur_id = role_utilisateur_id
            transition.condition_id = condition_id
            transition.url = url
            transition.traitement = traitement
            transition.unite_fonctionnelle_id = unite_fonctionnelle_id
            transition.num_ordre = num_ordre
            return transition
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE TRANSITION WORKFLOW")
            #print(e)
            return None

    @staticmethod
    def toSaveTransition(auteur, object_dao_wkf_transition):
        try:
            transition = Wkf_Transition()
            transition.etape_source_id = object_dao_wkf_transition.etape_source_id
            transition.etape_destination_id = object_dao_wkf_transition.etape_destination_id
            transition.role_utilisateur_id = object_dao_wkf_transition.role_utilisateur_id
            transition.condition_id = object_dao_wkf_transition.condition_id
            transition.url = object_dao_wkf_transition.url
            transition.traitement  = object_dao_wkf_transition.traitement
            transition.unite_fonctionnelle_id = object_dao_wkf_transition.unite_fonctionnelle_id
            transition.num_ordre = object_dao_wkf_transition.num_ordre
            transition.save()
            return transition
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE TRANSITION WORKFLOW")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateTransition(id, object_dao_wkf_transition):
        try:
            transition = Wkf_Transition.objects.get(pk = id)
            transition.etape_source_id = object_dao_wkf_transition.etape_source_id
            transition.etape_destination_id = object_dao_wkf_transition.etape_destination_id
            transition.role_utilisateur_id = object_dao_wkf_transition.role_utilisateur_id
            transition.condition_id = object_dao_wkf_transition.condition_id
            transition.url = object_dao_wkf_transition.url
            transition.traitement  = object_dao_wkf_transition.traitement
            transition.unite_fonctionnelle_id = object_dao_wkf_transition.unite_fonctionnelle_id
            transition.num_ordre = object_dao_wkf_transition.num_ordre
            transition.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE TRANSITION WORKFLOW")
            #print(e)
            return False
  
    @staticmethod
    def toGetTransition(id):
        try:
            return Wkf_Transition.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetTransitionsOfSource(etape_id, service_referent_id=0):
        if service_referent_id == 0:
            return Wkf_Transition.objects.filter(etape_source_id = etape_id).first()
        else:
            return Wkf_Transition.objects.filter(etape_source_id = etape_id).filter(unite_fonctionnelle_id = service_referent_id)
    
    @staticmethod
    def toGetNextEtapeFromTransitionsOfSource(etape_id, numero_ordre):
        return Wkf_Transition.objects.filter(etape_source_id = etape_id).filter(etape_destination__num_ordre = numero_ordre).first()

    @staticmethod
    def toGetEtapeDestinationOfTRansition(transition_id):
        try:
            trans = Wkf_Transition.objects.get(pk = transition_id)
            #print("TRANS ID %s" % trans)
            etape = Wkf_Etape.objects.get(pk = trans.etape_destination_id)
            #print("ETAPE SUI %s" % etape)
            return etape
        except Exception as e:
            #print("ERREUR LOG")
            #print(e)
            return False


    @staticmethod
    def toDeleteTransition(id):
        try:
            transition = Wkf_Transition.objects.get(pk = id)
            transition.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE TRANSITION WORKFLOW")
            #print(e)
            return False
        					
            