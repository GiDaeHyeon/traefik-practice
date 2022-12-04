from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse, RedirectResponse


app = FastAPI()


@app.get("/ping")
def ping() -> JSONResponse:
    """Health check endpoint"""
    return JSONResponse({"message": "pong"},
                        status_code=status.HTTP_200_OK)


@app.get("/get-test")
def simple_test(request: Request):
    return JSONResponse({"header": request.headers},
                        status_code=status.HTTP_200_OK)


@app.post("/post-test")
def simple_test(request: Request):
    return JSONResponse({"header": request.headers},
                        status_code=status.HTTP_200_OK)


@app.get("/redirect-test")
def redirect_test(request: Request):
    print(request.headers)
    return RedirectResponse("https://google.com",
                            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
