
from fastapi import FastAPI,Request,HTTPException,Response
import requests
import random



app = FastAPI()

def get_user_info(token):
   session = requests.Session()
   session.headers.update({
    'Authorization': f'{token}',
   'Accept-Language': 'en-US',
   'Content-Type': 'application/json'
   })
   try:
       response=requests.get('http://keycloak:8080/realms/reports-realm/protocol/openid-connect/userinfo',headers=headers)
       if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Invalid access token: {response} headers: {headers}"
                )
       return response.json()
   except ConnectionError  as e:
            raise HTTPException(
                status_code=500, detail=f"Keycloak request error: {str(e)}"
        )
       


@app.get("/")
def read_root(request: Request,  status_code=200):
    user_info=get_user_info(request.headers.get("authorization"))
   
    return {'authorization':user_info}

@app.get("/reports",  status_code=200)
def reports(request: Request):
 #   user_info=get_user_info(request.headers.get("authorization")) 

    user_info=dict() #  Заглушка для отладки логики.
    user_info['roles']=['prothetic_user','test'] #

    if 'prothetic_user' in user_info['roles']:
      report = [[random.randrange(1,1000,1)] * 10000 for i in range(10)]
      return {"report": report}
    else:
       raise HTTPException(status_code=401, detail="you don't have access")
    
    