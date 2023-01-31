from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import transaction
from django.utils import timezone
#from ULinkBackOffice.utils.timezone import timezone
from django.template import loader
from ULinkBackOffice.utils.identite import identite
from django.contrib import messages

from ULinkBackOffice.utils.wkf_task import wkf_task
from ULinkBackOffice.dao.dao_utils import dao_utils
from ULinkPublic.dao.dao_transaction import dao_transaction
# Create your views here.


def get_bootstrap(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("ULinkPublic_connexion"))
	return get_index(request)

def get_connexion(request):

	context = {
			'title' : 'Identifiez-vous au système !'
	}
	template = loader.get_template("ulinkpublic/login.html")
	return HttpResponse(template.render(context, request))

def post_connexion(request):
	try:
		password = request.POST["password"]
		username = request.POST["email"].lower().strip()

		utilisateur = authenticate(request, password = password, username = username)
		if(utilisateur is not None):
			login(request, utilisateur)
			return HttpResponseRedirect(reverse("ULinkPublic_accueil"))	
		else:
			messages.add_message(request, messages.ERROR, "Nous ne reconnaissons pas ces identifiants !")
			return HttpResponseRedirect(reverse("ULinkPublic_connexion"))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentive de connexion")
		return HttpResponseRedirect(reverse("ULinkPublic_connexion"))


def get_deconnexion(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("ULinkPublic_connexion"))

	logout(request)
	return HttpResponseRedirect(reverse("ULinkPublic_connexion"))

def get_index(request):
    issuer = identite.utilisateur(request)
    papers = dao_transaction.getPapersOfIssuer(issuer)
    context = {
    "title" : "Bienvenu(e)",
	"papers": papers,
	"user": issuer
    }
    template = loader.get_template("ulinkpublic/index.html")
    return HttpResponse(template.render(context, request))

def get_creer_requete(request):
	is_connect=identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('ULinkPublic_connexion'))
	
	context ={
		'title' : 'Effectuer une demande',
		'utilisateur' : identite.utilisateur(request),
		}
	template = loader.get_template('ulinkpublic/request/add.html')
	return HttpResponse(template.render(context, request))

#@transaction.atomic
def post_creer_requete(request):
	#sid = transaction.savepoint()
	try:
		issuer = identite.utilisateur(request)
		nid = request.POST['nid']
		nas = request.POST['nas']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		fullname = f'{firstname} {lastname}'
		paperNumber = dao_utils.generatePaperNumber()
		createDateTime = timezone.now()
		file = ""

		if 'file_upload' in request.FILES:
			file = request.FILES["file_upload"]

		list_brand = request.POST.getlist('brand', None)
		list_model = request.POST.getlist('model', None)
		list_year = request.POST.getlist('year', None)
		list_carId = request.POST.getlist('carId', None)
		list_plateId = request.POST.getlist('plateId', None)
		nvh = len(list_brand)
		lines = []

		for i in range(0, len(list_brand)) :
			brand = list_brand[i]
			model = list_model[i]
			year = list_year[i]
			carId = list_carId[i]
			plateId = list_plateId[i]
			lines.append(f"{brand},{model},{year},{carId},{plateId}")

		lines = "|".join(lines) #delimiter of lines
		paper = dao_transaction.create(issuer, paperNumber, createDateTime, nid, nvh, fullname, nas, lines, file)	
		#transaction.savepoint_commit(sid)
		isPopup = 1

		return HttpResponseRedirect(reverse("ULinkPublic_detail_requete", args=(paper.id, isPopup)))
		
	except Exception as e:
		#transaction.savepoint_rollback(sid)
		print(f"Erreur on Post Creer Requete: {e}")
		return HttpResponseRedirect(reverse('ULinkPublic_add_requete'))


def get_details_requete(request,ref, isPopup = 0):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('dataforchildren_connexion'))
	try:
		ref=int(ref)
		utilisateur = identite.utilisateur(request)
		isPopup = int(isPopup)

		
		paper = dao_transaction.getPaper(ref)
		lines = dao_utils.processingLines(paper.lines)
		
		template = loader.get_template('ulinkpublic/request/item.html')
		context ={
			'title' : 'Informations',
			'stylebody': 'page-profile',
			'model' : paper,
			'lines': lines,
			'isPopup': isPopup,
			'utilisateur' : utilisateur
			}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print("Erreur on Get Item Requete", e)
		return HttpResponseRedirect(reverse('ULinkPublic_accueil'))


def post_wkf_request(request):
	try:
		issuer = identite.utilisateur(request)
		etape_id = request.POST["etape_id"]
		doc_id = request.POST["doc_id"]

		paper = dao_transaction.getPaper(doc_id)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']

		if int(etape_id) == 1:
			paper = dao_transaction.issue(issuer, paper.paperNumber, paper.operator, issuer, timezone.now())
		elif int(etape_id) == 4:
			paper = dao_transaction.pay(issuer, paper.paperNumber, paper.operator, issuer, timezone.now(), file, "")
		else:
			raise Exception(f"Step {etape_id} not recognized")

		isPopup = 1
		return HttpResponseRedirect(reverse("ULinkPublic_detail_requete", args=(paper.id, isPopup)))
		
	except Exception as e:
		#transaction.savepoint_rollback(sid)
		print(f"Erreur on Post Creer Requete: {e}")
		return HttpResponseRedirect(reverse('ULinkPublic_add_requete'))