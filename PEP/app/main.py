from fastapi import FastAPI
import requests

PBAC_URLS = ["http://host.docker.internal:8001", "http://host.docker.internal:8002", "http://host.docker.internal:8003", "http://host.docker.internal:8004"] 
SECRET_DATA = "This is a secret message"

app = FastAPI()

@app.get("/health")
async def health():
    healthy = {}
    for url in PBAC_URLS[1:]:
        url = f"{url}/health"
        print(f"Checking {url}")
        try:
            response = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            healthy[url] = False
            continue
        print(response.json())
        healthy[url] = True
    return healthy


@app.get("/")
async def request_access(
    user_name: str = None,
    organization_ura: str = None,
    noodgeval: bool = False,
):
    """
    ### Endpoint Description
    These are the possibilities:

    | User      | Authorized organization(s) |
    |-----------|----------------------------|
    | tom       | 555 & 777                  |
    | john      | 555                        |
    | bea       | None                       |
    Option noodgeval is a boolean that can be set to True to simulate an emergency.
    """
    print("Requesting Access")
    print("Request sent to PDP.")

    some_json = {
        "input": {
            "user": user_name,
            "organization": organization_ura,
        }
    } if not noodgeval else {
        "input": {
            "message": "noodgeval"
        }
    }
    
    response = requests.post(f"{PBAC_URLS[1]}/v1/data/example/authz/allow", timeout=2, json=some_json)
    print(response.json())
    
    if response.json()["result"]:
        print("Access Granted")
        return {"status": "Data request Approved", "data": SECRET_DATA}
    else:
        print("Access Denied")
        return {"status": "Data request Denied", "data": None}
