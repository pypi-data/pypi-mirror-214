from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import argparse

def HTTPException(status_code, detail):
    from fastapi import HTTPException
    return HTTPException(status_code=status_code, detail=detail)

class ConvertToJson():

    def __init__(self, request, key):
        self.type = request.headers.get("content-type")
        self.request = request
        self.key = key

    async def get(self):
        if self.type == "application/json":
            return await self.get_request() 
        else:
            raise HTTPException(status_code=404, detail="type not application/json")

    async def get_request(self):
        _json = await self.request.json()
        
        if not _json.get(self.key):
            raise HTTPException(status_code=404, detail=f"{self.key} not found")

        for key in dict(self.request.query_params):
            if key != self.key:
                _json[key] = dict(self.request.query_params).get(key)

        return _json


def rush_serving(Inference):

  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--http-port", default=9000)
  args = parser.parse_args()

  app = FastAPI()

  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  inference = Inference()
  
  @app.on_event("startup")
  def init():
      inference.load()

  @app.get('/healthz')
  async def health_endpoint(request: Request):
    return {"status": "healthy"}

  @app.get('/version')
  async def health_endpoint(request: Request):
    try:
      return {"version": inference.version}
    except:
      return {"version": "demo"}

  @app.post('/predict')
  async def inference_endpoint(request: Request):
      _json = await ConvertToJson(request, "input").get()
      return inference.predict(_json) 
      
  uvicorn.run(app, host='0.0.0.0', port=int(args.http_port))
