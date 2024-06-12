from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

app = FastAPI()

class UserAuth(BaseModel):
    email: str
    password: str

@app.post("/signup")
async def sign_up(user: UserAuth):
    try:
        response = supabase.auth.sign_up({
            'email': user.email,
            'password': user.password
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Sign-up failed")
        return {"message": "User signed up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signin")
async def sign_in(user: UserAuth):
    try:
        response = supabase.auth.sign_in_with_password({
            'email': user.email,
            'password': user.password
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Sign-in failed")
        return {"message": "User signed in successfully", "session": response.session}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    # Make some routes unprotected
    if request.method == "OPTIONS" or request.url.path in ["/", "/docs", "/openapi.json", "/signup", "/signin"]:
        return await call_next(request)

    token = request.headers.get("authorization", "").replace("Bearer ", "")
    print(f"Token: {token}")  # Log the token for debugging

    if not token:
        return Response("Unauthorized", status_code=401)

    try:
        # auth = supabase.auth.get_user(token)
        # print(auth)
        # request.state.user_id = auth.user.id
        # print(request.state.user_id)
        # await supabase.auth.set_auth(token)
        # supabase.auth.set_auth(token)
        auth_response = supabase.auth.get_user(token)
        print(auth_response)
        if not auth_response.user:
            raise HTTPException(status_code=401, detail="Invalid user token")

        request.state.user_id = auth_response.user.id
        print(request.state.user_id)
    except Exception as e:
        print(f"Auth Error: {e}")  # Log the error for debugging
        return Response("Invalid user token", status_code=401)

    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "This is an unprotected route"}

@app.get("/protected")
async def protected_route(request: Request):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Hello, user {user_id}"}

@app.post("/protected/data")
async def protected_data(request: Request):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Data saved for user {user_id}"}

@app.post("/logout")
async def log_out(request: Request):
    user_id = request.state.user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        supabase.auth.sign_out()
        return {"message": "User logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
