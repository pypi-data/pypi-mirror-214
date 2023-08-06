from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}"}


if __name__ == "__main__":

    class UvicornRequired(Exception):
        pass

    msg = "\n\nPlease run this script with Uvicorn, for example:\n\n  uvicorn service_api:app\n\n"
    raise UvicornRequired(msg)
