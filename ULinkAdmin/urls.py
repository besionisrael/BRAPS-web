from django.urls import include, re_path
from . import views

urlpatterns=[
    # DASHBOARD URL
    re_path(r'^$', views.get_bootstrap, name='ULinkAdmin_accueil'),
    re_path(r'^login/$', views.get_connexion, name='ULinkAdmin_connexion'),
    re_path(r'^post_connexion/$', views.post_connexion, name='ULinkAdmin_post_connexion'),
    re_path(r'^logout/$', views.get_deconnexion, name='ULinkAdmin_deconnexion'),

    re_path(r'^item/(?P<ref>[0-9]+)/$', views.get_item, name='ULinkAdmin_item'),

    re_path(r'^blocpapers/$', views.get_blocpapers_list, name='ULinkAdmin_blocpapers_list'),
    re_path(r'^blocpapers/item/(?P<ref>[0-9]+)/$', views.get_blocpapers_item, name='ULinkAdmin_blocpapers_item'),
    
    #url for all post wkf
    re_path(r'^post_wkf/', views.post_wkf_request, name = 'ULinkAdmin_post_wkf_requete'),

]