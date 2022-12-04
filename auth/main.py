from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse, RedirectResponse


app = FastAPI()


@app.get("/ping")
def ping() -> JSONResponse:
    """Health check endpoint"""
    return JSONResponse({"message": "pong"},
                        status_code=status.HTTP_200_OK)


@app.post("/sign-up")
def simple_sign_up(request: Request):
    return JSONResponse({"header": request.headers},
                        status_code=status.HTTP_200_OK)


@app.post("/sign-in")
def simple_sign_in(request: Request):
    return JSONResponse({"header": request.headers},
                        status_code=status.HTTP_200_OK)


@app.post("/auth")
def validate_token(request: Request):
    return JSONResponse({"header": request.headers},
                        status_code=status.HTTP_200_OK)
