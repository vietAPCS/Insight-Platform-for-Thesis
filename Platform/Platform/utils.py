from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests

def encrypt(message):
    f = Fernet(settings.ENCRYPTION_SECRET)
    mes =  bytes(message, encoding='utf8')
    token = f.encrypt(mes)
    ret = token.decode()
    return ret

def decrypt(message):
    f = Fernet(settings.ENCRYPTION_SECRET)
    print(settings.ENCRYPTION_SECRET)
    mes =  bytes(message, encoding='utf8')
    token = f.decrypt(mes)
    ret = token.decode()
    return ret

def get_cid(request):
    if(len(request.FILES) != 0):
        file = request.FILES['doc']
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        jwt_token = "Bearer " + settings.PINATA_JWT
        headers = {
            "Authorization": jwt_token
        }
        response = requests.request("POST", url, files={'file': file}, headers=headers)
        cid = response.json()["IpfsHash"]
        return cid

def get_file(request):
    file_url = 'https://ipfs.io/ipfs/'+ decrypt(request.POST.get('download'))
    response = requests.get(file_url)
    if response.status_code == 200:
        # Set the file name for the downloaded file
        filename = 'request' + '.pdf'

        # Create an HttpResponse with the file content and appropriate headers
        response = HttpResponse(
            response.content,
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse("Failed to download the file.")