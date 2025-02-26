
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World from home page"}

@app.get("/hello")
async def hello():
    return {"message": "Hello World from /hello"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
    
    