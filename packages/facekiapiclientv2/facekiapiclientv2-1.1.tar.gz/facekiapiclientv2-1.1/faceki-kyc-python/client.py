import requests

class FacekiAPIClientV2:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://sdk.faceki.com'
        self.token = self.generate_token()

    def generate_token(self):
        auth_url = f'{self.base_url}/auth/api/access-token?clientId='+self.client_id+"&clientSecret="+self.client_secret 
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.get(auth_url)
        if response.status_code == 200:
            resp = response.json()
            print(resp)
            return resp["data"]["access_token"]
        else:
            raise Exception('Failed to generate token')

    def getKYCRules(self, params=None):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        url = f'{self.base_url}/kycrules/api/kycrules'
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')

    def requestKYC(self,selfie_image,id_front_image,id_back_image,dl_front_image,dl_back_image,pp_front_image,pp_back_image=None):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        files = {
        'selfie_image': ('selfie_image.jpg', open(selfie_image, 'rb')),
        'id_front_image': ('id_front_image.jpg', open(id_front_image, 'rb')),
        'id_back_image': ('id_back_image.jpg', open(id_back_image, 'rb')),
        'dl_front_image': ('dl_front_image.jpg', open(dl_front_image, 'rb')),
        'dl_back_image': ('dl_back_image.jpg', open(dl_back_image, 'rb')),
        'pp_front_image': ('pp_front_image.jpg', open(pp_front_image, 'rb')),
        'pp_back_image': ('pp_back_image.jpg', open(pp_back_image, 'rb')),
        }


        url = f'{self.base_url}/kycverify/api/kycverify/multi-kyc-verification'
        
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')
        
    def getKycSummary(self):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        url = f'{self.base_url}/kycverify/api/kycverify/kyc-verify-summary'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')
        
    def generateKYCLink(self,expireTime=0,applicationId=None):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        payload ={
            'expiryTime':expireTime,
            'applicationId':applicationId
        }

        url = f'{self.base_url}/kycverify/api/kycverify/kyc-verify-link'
        response = requests.post(url, headers=headers,json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')

    def getKYCrecords(self,linkId=None):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        params = None
        if linkId != None:
            params ={
                'linkId':linkId,
            }

        url = f'{self.base_url}/kycverify/api/kycverify/link'
        response = requests.get(url, headers=headers,params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')

    def getKYCrecords(self,selfie_image):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
        'selfie_image': ('selfie_image.jpg', open(selfie_image, 'rb'))
        }

        url = f'{self.base_url}/facelink/api/face-check'
        response = requests.post(url, headers=headers,files=files)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')