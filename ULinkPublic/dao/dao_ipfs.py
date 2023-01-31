from __future__ import unicode_literals
import os
import hashlib
from ULinkBackOffice.dao.dao_utils import dao_utils
from ULinkPublic.models import IPFS
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
from AppUlink.settings import IPFS_CONNECT, IPFS_STRING_CONNECTION
import ipfshttpclient



class dao_ipfs(object):
    '''Interaction with IPFS Model'''
     
    @staticmethod
    def toUploadDocument(file, description = ""):
        '''Uploading One Document'''
        try:
            if file:
                #If IPFS is connected. 
                if IPFS_CONNECT:
                    client = ipfshttpclient.connect(IPFS_STRING_CONNECTION)
                    res = client.add(save_path)
                    print("**************Upload Successfuly on IPFS********")
                    hashFile = res["Hash"]
                    print(f'Hash:{hashFile}')
                else:
                    media_dir = settings.MEDIA_ROOT
                    media_url = settings.MEDIA_URL

                    docs_dir = 'documents/'
                    media_dir = media_dir + '/' + docs_dir
                    
                    extension = os.path.splitext(str(file))[1]
                    file_name = dao_utils.generateUploadNumber() + '.' + extension

                    
                    save_path = os.path.join(media_dir, str(file_name))
                    path = default_storage.save(save_path, file)
                    url = media_url + docs_dir + str(file_name)
                    hashFile = hashlib.sha256(url.encode("utf-8")).hexdigest()


                document = IPFS()
                document.privateUrlDocument = url
                document.publicUrlDocument = hashFile 
                document.description = description
                document.save()
                return document
            else: return None
                
        except Exception as e:
            print("Upload on IPFS error", e)
            return None
        
    
    @staticmethod
    def toGetDocument(publicUrlDocument):
        try:
            return IPFS.objects.filter(publicUrlDocument = publicUrlDocument).first()
        except Exception as e:
            print("Get Document IPFS error", e)
            return None
