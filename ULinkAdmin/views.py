from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import transaction
from django.utils import timezone
from django.template import loader
from ULinkBackOffice.utils.identite import identite
from django.contrib import messages
from ULinkAdmin.dao.dao_rqpaper import dao_rqpaper
from ULinkAdmin.dao.dao_historic import dao_historic
from ULinkBackOffice.dao.dao_utils import dao_utils


# Create your views here.


def get_bootstrap(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("ULinkAdmin_connexion"))
	return get_index(request)

def get_connexion(request):

	context = {
			'title' : 'Identifiez-vous au système !'
	}
	template = loader.get_template("ulinkadmin/login.html")
	return HttpResponse(template.render(context, request))

def post_connexion(request):
	try:
		password = request.POST["password"]
		username = request.POST["email"].lower().strip()

		utilisateur = authenticate(request, password = password, username = username)
		if(utilisateur is not None):
			login(request, utilisateur)
			return HttpResponseRedirect(reverse("ULinkAdmin_accueil"))	
		else:
			messages.add_message(request, messages.ERROR, "Nous ne reconnaissons pas ces identifiants !")
			return HttpResponseRedirect(reverse("ULinkAdmin_connexion"))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de connexion")
		return HttpResponseRedirect(reverse("ULinkAdmin_connexion"))


def get_deconnexion(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("ULinkAdmin_connexion"))

	logout(request)
	return HttpResponseRedirect(reverse("ULinkAdmin_connexion"))

def get_index(request):
    author = identite.utilisateur(request)
    label = 1
    if 'label' in request.GET:
        label = int(request.GET['label'])
    papers = dao_rqpaper.toListPapersByCat(label)
    context = {
    "title" : "Bienvenu(e)",
	"user": author,
	"papers": papers,
    }
    template = loader.get_template("ulinkadmin/index.html")
    return HttpResponse(template.render(context, request))



def get_item(request, ref):
	try:
		ref = int(ref)
		author = identite.utilisateur(request)
		paper = dao_rqpaper.toGetPaper(ref)
		lines = dao_utils.processingLines(paper.lines)
		files = dao_historic.toGetFilesIPFS(paper.issuer, paper.paperNumber)
		context = {
			'title' : 'Panel !',
			'model': paper,
			'lines': lines,
			'files': files,
			'utilisateur' : author
		}
		template = loader.get_template("ulinkadmin/panel.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la requête")
		return HttpResponseRedirect(reverse("ULinkAdmin_accueil"))


def post_wkf_request(request):
	try:
		author = identite.utilisateur(request) #Actually this is the id at Blockchain
		etape_id = request.POST["etape_id"]
		doc_id = request.POST["doc_id"]		
		file = None
		vat = None
		if 'vat' in request.POST:
			vat = request.POST["vat"]
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
		
		if int(etape_id) == 1:#Means it's created
			paper = dao_historic.sendToPrivate(doc_id, author)
		elif int(etape_id) == 2: #Means it's uploaded
			paper = dao_historic.uploadVDE23(doc_id, file, vat, author) 
		else:
			raise Exception("Step not recognized")

		return HttpResponseRedirect(reverse("ULinkAdmin_accueil") + f"?label={paper.currentState}")
		
	except Exception as e:
		#transaction.savepoint_rollback(sid)
		print(f"Erreur on Post Workflow: {e}")
		return HttpResponseRedirect(reverse('ULinkAdmin_accueil'))

#####Papers on Blockchain

def get_blocpapers_list(request):
    author = identite.utilisateur(request)
    papers = dao_historic.toListAllBlocPapers()
    context = {
    "title" : "Bienvenu(e)",
	"user": author,
	"papers": papers,
    }
    template = loader.get_template("ulinkadmin/blocpapers/list.html")
    return HttpResponse(template.render(context, request))


def get_blocpapers_item(request, ref):
	try:
		ref = int(ref)
		author = identite.utilisateur(request)
		paper = dao_historic.toGetBlocPaperTxnID(ref)
		lines = dao_utils.processingLines(paper.lines)
		context = {
			'title' : 'Panel !',
			'model': paper,
			'lines': lines,
			'utilisateur' : author
		}
		template = loader.get_template("ulinkadmin/blocpapers/panel.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la requête")
		return HttpResponseRedirect(reverse("ULinkAdmin_blocpapers_list"))