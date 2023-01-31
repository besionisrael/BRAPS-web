from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

############################## MODEL WORKFLOW

class Wkf_Workflow(models.Model):
    type_document        =    models.CharField(max_length=30, unique=True)
    content_type         =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.type_document

class Wkf_Etape(models.Model):
    designation          =    models.CharField(max_length=50)
    label                =    models.CharField(max_length=50, blank=True, null=True)
    workflow             =    models.ForeignKey(Wkf_Workflow, on_delete=models.CASCADE, related_name="etapes_workflows")
    est_initiale         =    models.BooleanField(default=False)
    est_finale           =    models.BooleanField(default=False)
    est_decisive         =    models.BooleanField(default = False)
    num_ordre            =    models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.workflow.type_document +' / '+ self.designation

    def etat_initial(self):
        if self.est_initiale == True : return "Initiale"
        else : return "Non initiale"

class Wkf_Condition(models.Model):
    designation         =    models.CharField(max_length=50)

    def __str__(self):
        return self.designation

class Wkf_Transition(models.Model):
    etape_source        =    models.ForeignKey(Wkf_Etape, on_delete=models.CASCADE, related_name="transitions_etapes_source")
    etape_destination   =    models.ForeignKey(Wkf_Etape, on_delete=models.CASCADE, related_name="transitions_etapes_destination")
    group               =    models.ForeignKey(Group, on_delete=models.SET_NULL, related_name="group_of_transition", blank=True, null=True)
    condition           =    models.ForeignKey(Wkf_Condition, on_delete=models.SET_NULL, blank=True, null=True , related_name="conditions_transitions")
    url                 =    models.CharField(max_length = 250, blank=True, null=True)
    traitement          =    models.CharField(max_length=250, blank=True, null=True)
    num_ordre           =    models.IntegerField(blank=True, null=True)
    identifiant_cle     =    models.IntegerField(blank=True, null = True)


    def __str__(self):
        return self.etape_source.designation + ' > ' + self.etape_destination.designation

class Wkf_Historique(models.Model):
    user             =    models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name="workflow_utilisateurs", blank=True, null=True)
    etape                =    models.ForeignKey(Wkf_Etape,on_delete=models.DO_NOTHING, related_name="workflow_etapes")
    timestamp             =   models.DateTimeField(auto_now_add=True)
    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    document_id             =    models.PositiveIntegerField(blank=True, null=True)
    content_object          =    GenericForeignKey('content_type', 'document_id')
    
    def __str__(self):
        return self.etape.designation


class Document(models.Model):
    numero_document                 =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    type_document                   =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    url_document                    =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    description                     =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    est_verifie                     =     models.BooleanField(default = False)
    index                           =   models.TextField(blank=True)

    content_type            =    models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    source_document_id             =    models.PositiveIntegerField(blank=True, null=True)
    content_object          =    GenericForeignKey('content_type', 'source_document_id')

    status                          =     models.CharField(max_length = 600, null = True, blank=True, default = '')
    metadonnees                     =     models.TextField(null = True, blank=True)
    created_at                       =     models.DateTimeField(auto_now = True)
    update_at                       =     models.DateTimeField(auto_now = True)
    auteur                          =     models.ForeignKey(User, on_delete = models.SET_NULL, related_name = 'auteur_de_model_document_oej', null = True, blank = True)
    url                                =         models.CharField(max_length = 600, blank=True, null=True)
    taille                           =      models.CharField(max_length = 100, blank=True, null=True)

    def __str__(self):
        return str(self.description)
