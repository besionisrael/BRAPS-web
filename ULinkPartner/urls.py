from django.urls import include, re_path
from . import views

urlpatterns=[
    # DASHBOARD URL
    re_path(r'^$', views.get_bootstrap, name='ULinkPartner_accueil'),
    re_path(r'^search/(?P<keyword>[a-zA-Z0-9_\-]*)/$', views.get_index, name='ULinkPartner_index'),
    re_path(r'^login/$', views.get_connexion, name='ULinkPartner_connexion'),
    re_path(r'^post_connexion/$', views.post_connexion, name='ULinkPartner_post_connexion'),
    re_path(r'^logout/$', views.get_deconnexion, name='ULinkPartner_deconnexion'),
    re_path(r'^post_search/$', views.post_search, name='ULinkPartner_post_search'),
    re_path(r'^item/(?P<keyword>[a-zA-Z0-9_\-]+)/$', views.get_item, name='ULinkPartner_item'),
    re_path(r'^post_received/', views.post_received, name = 'ULinkPartner_post_received'),
    re_path(r'^historic/$', views.get_historic_list, name='ULinkPartner_historic_list'),

    

]