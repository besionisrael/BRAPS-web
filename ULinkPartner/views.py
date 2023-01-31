from django.shortcuts import render
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
from ULinkAdmin.dao.dao_rqpaper import dao_rqpaper
from ULinkBackOffice.dao.dao_utils import dao_utils
from ULinkPublic.dao.dao_transaction import dao_transaction
# Create your views here.


def get_bootstrap(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("ULinkPartner_connexion"))
	return get_index(request, "")

def get_connexion(request):

	context = {
			'title' : 'Identifiez-vous au système !'
	}
	template = loader.get_template("ulinkpartner/login.html")
	return HttpResponse(template.render(context, request))

def post_connexion(request):
	try:
		password = request.POST["password"]
		username = request.POST["email"].lower().strip()

		utilisateur = authenticate(request, password = password, username = username)
		if(utilisateur is not None):
			login(request, utilisateur)
			return HttpResponseRedirect(reverse("ULinkPartner_accueil"))	
		else:
			messages.add_message(request, messages.ERROR, "Nous ne reconnaissons pas ces identifiants !")
			return HttpResponseRedirect(reverse("ULinkPartner_connexion"))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de connexion")
		return HttpResponseRedirect(reverse("ULinkPartner_connexion"))


def get_deconnexion(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("ULinkPartner_connexion"))

	logout(request)
	return HttpResponseRedirect(reverse("ULinkPartner_connexion"))

def get_index(request, keyword = ""):
    author = identite.utilisateur(request)
    data = 0
    if keyword:
        data = dao_transaction.getPaperByPaperNumberSAAQ(keyword)
    context = {
    "title" : "Bienvenu(e)",
	"user": author,
    "data": data,
    "keyword": keyword,
    }
    template = loader.get_template("ulinkpartner/index.html")
    return HttpResponse(template.render(context, request))

def post_search(request):
    keyword = request.POST['keyword']
    keyword = f'PAPER-{keyword}'
    return HttpResponseRedirect(reverse("ULinkPartner_index", args=(keyword,)))

def get_item(request, keyword):
	try:
		author = identite.utilisateur(request)
		data = dao_transaction.getPaperByPaperNumber(keyword)
		lines = dao_utils.processingLines(data.lines)
		context = {
			'title' :  data.paperNumber,
			'model': data,
			'lines': lines,
			'utilisateur' : author
		}
		template = loader.get_template("ulinkpartner/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print("ERREUR")
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la requête")
		return HttpResponseRedirect(reverse("ULinkPartner_accueil"))

def post_received(request):
	paperNumber = request.POST["paperNumber"]
	try:
		issuer = identite.utilisateur(request) #Actually this is the id at Blockchain
		etape_id = request.POST["etape_id"]
		doc_id = request.POST["doc_id"]

		paper  = dao_transaction.getPaper(doc_id)
		
		if int(etape_id) == 5:#Means it's paid
			paper = dao_transaction.receive(paper.issuer, paperNumber, paper.operator, issuer, timezone.now(),"")
		
		else:
			raise Exception("Step not recognized")

		return HttpResponseRedirect(reverse('ULinkPartner_item', args=(paperNumber.split('-')[1],) ))
		
	except Exception as e:
		#transaction.savepoint_rollback(sid)
		print(f"Erreur on Post Received: {e}")
		return HttpResponseRedirect(reverse('ULinkPartner_item', args=(paperNumber.split('-')[1],) ))



def get_historic_list(request):
    author = identite.utilisateur(request)
    papers = dao_transaction.getPapersOfState(6) #6 = Received by SAAQ
    context = {
    "title" : "Bienvenu(e)",
	"user": author,
	"papers": papers,
    }
    template = loader.get_template("ulinkpartner/list.html")
    return HttpResponse(template.render(context, request))