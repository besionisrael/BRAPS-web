from django.urls import include, re_path
from . import views

urlpatterns=[
    # DASHBOARD URL
    re_path(r'^$', views.get_bootstrap, name='ULinkPublic_accueil'),
    re_path(r'^login/$', views.get_connexion, name='ULinkPublic_connexion'),
    re_path(r'^post_connexion/$', views.post_connexion, name='ULinkPublic_post_connexion'),
    re_path(r'^logout/$', views.get_deconnexion, name='ULinkPublic_deconnexion'),

    re_path(r'^request/add', views.get_creer_requete, name = 'ULinkPublic_add_requete'),
    re_path(r'^request/post_add', views.post_creer_requete, name = 'ULinkPublic_post_add_requete'),
    re_path(r'^request/item/(?P<ref>[0-9]+)/$', views.get_details_requete, name = 'ULinkPublic_detail_requete'),
    re_path(r'^request/item/(?P<ref>[0-9]+)/(?P<isPopup>[0-1]{1})/$', views.get_details_requete, name = 'ULinkPublic_detail_requete'),

    #url for all post wkf
    re_path(r'^request/post_issuing', views.post_wkf_request, name = 'ULinkPublic_post_wkf_requete'),


]