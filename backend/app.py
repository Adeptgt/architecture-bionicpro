
from fastapi import FastAPI,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from keycloak import KeycloakOpenID
import random


# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://keycloak:8080/",
                                 client_id="reports-api",
                                 realm_name="reports-realm",
                                 client_secret_key="oNwoLQdvJAvRcL89SydqCWCe5ry1jMgq")


app = FastAPI()
origins = [
    # разрешенные источники
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    # сначапо все запрещаем    
    CORSMiddleware,
    # потом начинаем разрешать необходимое
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate(n):
   values = ['value1', 'value2']
   mydict = {"key " + str(i): values[0] for i in range(n)}
   mydict["key " + str(random.randrange(n))] = values[1]
   return mydict



@app.get("/")
def read_root(request: Request,  status_code=200):
    config_well_known = keycloak_openid.well_known()
   
    return {'config_well_known':config_well_known}

@app.get("/reports",  status_code=200)
def reports(request: Request):
    tmp=request.headers.get("authorization")
    token=str.split(tmp,' ')
    try: 
     token_info = keycloak_openid.decode_token(token[1])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Не валидный токен!")
    

    if 'prothetic_user' in token_info['realm_access']['roles'] :
      

      return generate(100)
    else:
       raise HTTPException(status_code=401, detail="У вас нет доступа!")
    
    