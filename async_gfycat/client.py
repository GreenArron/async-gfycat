import aiohttp
import time
import json

from async_gfycat.errors import GfycatClientError

GFYCAT_ENDPOINT = 'https://api.gfycat.com/v1/gfycats'
FILE_ENDPOINT = 'https://filedrop.gfycat.com'
CHECK_UPLOAD_ENDPOINT = 'https://api.gfycat.com/v1/gfycats/fetch/status/'
OAUTH_ENDPOINT = 'https://api.gfycat.com/v1/oauth/token'
ERROR_KEY = 'errorMessage'

class GfycatClient(object):
    
    
    def __init__(self, client_id:str, client_secret:str, username:str=None, password:str=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.refresh_token = None 
        self.access_token = None 

    async def upload_from_url(self, url:str, title:str=None, desc:str=None, tags=None, 
                              nsfw:int=0, no_md5:bool=True, keep_audio:bool=False, private:bool=False) -> str:
        """
        Upload a GIF from a URL.
        
        
        Returns the gfyname of upload
        
        
        note that the wrapper does not handle md5 issues if `no_md5` is set to `False`
        for more information about the optional params visit:
        https://developers.gfycat.com/api/?curl#gfycat-creation-parameters-and-options
        """
        await self.check_token()

        if title == None:
            title = ''
        if desc == None:
            desc = ''
        
     
        data = {
            'fetchUrl':url,
            "title": title,
            'description':desc,
            "tags": tags,
            "keepAudio": keep_audio,
            "noMd5": no_md5,
            'nsfw': nsfw,
            'private':private
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(GFYCAT_ENDPOINT, data=json.dumps(data), headers=self.headers) as r:
                if r.status != 200:
                    raise GfycatClientError('Error fetching the URL', r.status, r.__dict__)

                response = await r.json()
                if 'error' in response:
                    raise GfycatClientError(response['error'], response_data=r.__dict__)

        return response['gfyname']

    async def upload_from_file(self, filepath:str, title:str=None, desc:str=None, tags=None, 
                               nsfw:int=0, no_md5:bool=True, keep_audio:bool=False, private:bool=False) -> str:
        """
        Upload a local file to Gfycat
        
        Returns the gfyname of the upload
        """
        await self.check_token()
        
        data = {
            "title": title,
            'description':desc,
            "tags": tags,
            "keepAudio": keep_audio,
            "noMd5": no_md5,
            'nsfw': nsfw,
            'private':private
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(GFYCAT_ENDPOINT, data=json.dumps(data), headers=self.headers) as r:      
                response = await r.json()
                gfyname = response['gfyname']

            async with session.post(FILE_ENDPOINT, data={'key': gfyname, 'file':open(filepath, 'rb')}) as r:
                if not 200 <= r.status <= 209:
                    raise GfycatClientError('Error uploading the GIF', r.status, r.__dict__)
            
        return gfyname
       
    async def check_upload(self, gfyname:str) -> dict:
        """
        Checks the status of an upload.
        
        Returns the response data
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(CHECK_UPLOAD_ENDPOINT + gfyname) as r:
                if r.status != 200:
                    raise GfycatClientError('Unable to check the link',
                                            r.status, r.__dict__)
        
                return await r.json()

    async def query_gfy(self, gfyname:str) -> dict:
        """
        Query a gfy name for URLs and more information.
        
        Returns the response data 
        """
        await self.check_token()
        async with aiohttp.ClientSession() as session:
            async with session.get(GFYCAT_ENDPOINT + f"/{gfyname}", headers=self.headers) as r:

                response = await r.json()

                if r.status != 200 and not ERROR_KEY in response:
                    raise GfycatClientError('Bad response from Gfycat',
                                            r.status, r.__dict__)
                elif ERROR_KEY in response:
                    raise GfycatClientError(response[ERROR_KEY], r.status, r.__dict__)

        return response

    
    async def check_token(self) -> None:
        """
        Checks if Token is still valid and updates if it's not
        """
        if self.access_token == None:
            await self._get_token()
        elif time.time() > self.token_expires_at:
            if self.refresh_token and time.time() > self.refresh_expires_at:
                await self._refresh_autho()
            else:
                await self._get_token()

    async def _refresh_autho(self) -> None:
        '''Refreshes the access token for username based tokens''' 
        payload = {'grant_type': 'refresh', 'client_id': self.client_id, 'client_secret': self.client_secret, 'refresh_token':self.refresh_token}
        
        
        async with aiohttp.ClientSession() as session:
            async with session.get(OAUTH_ENDPOINT, data=json.dumps(payload), headers={'content-type': 'application/json'}) as r:
                response = await r.json()

                if r.status != 200 and not ERROR_KEY in response:
                    raise GfycatClientError('Error fetching the OAUTH URL', r.status)
                elif ERROR_KEY in response:
                    raise GfycatClientError(response[ERROR_KEY], r.status)

                self.token_type = response['token_type']
                self.access_token = response['access_token']
                self.token_expires_at = time.time() + response['expires_in'] - 5
                
                self.refresh_token = response['refresh_token']
                self.refresh_expires_at = time.time() + response['refresh_token_expires_in'] - 5
                    
                
                self.headers = {'content-type': 'application/json', 'Authorization': self.token_type + ' ' + self.access_token}
    
    async def _get_token(self) -> None:
        """
        Gets the authorization token
        """

        payload = {'grant_type': 'client_credentials', 'client_id': self.client_id, 'client_secret': self.client_secret}
        if self.password and self.username:
            payload['grant_type'] = 'password'
            payload['username'] = self.username
            payload['password'] = self.password
            
        async with aiohttp.ClientSession() as session:
            async with session.get(OAUTH_ENDPOINT, data=json.dumps(payload), headers={'content-type': 'application/json'}) as r:
                response = await r.json()
                if r.status != 200 and not ERROR_KEY in response:
                    raise GfycatClientError('Error fetching the OAUTH URL', r.status, r.__dict__)
                elif ERROR_KEY in response:
                    raise GfycatClientError(response[ERROR_KEY], r.status, r.__dict__)

                self.token_type = response['token_type']
                self.access_token = response['access_token']
                self.token_expires_at = time.time() + response['expires_in'] - 5
                
                if 'refresh_token' in response:
                    self.refresh_token = response['refresh_token']
                    self.refresh_expires_at = time.time() + response['refresh_token_expires_in'] - 5
                    
                
                self.headers = {'content-type': 'application/json', 'Authorization': self.token_type + ' ' + self.access_token}
