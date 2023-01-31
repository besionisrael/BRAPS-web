from __future__ import unicode_literals

class identite(object):
    @staticmethod
    def est_connecte(request):
        if request.user.is_authenticated == False : return False
        else: return True

    @staticmethod
    def utilisateur(request):
        if identite.est_connecte(request) == False: return None
        utilisateur = request.user
        return utilisateur

    @staticmethod
    def user(request):
        if identite.est_connecte(request) == False: return None
        return request.user