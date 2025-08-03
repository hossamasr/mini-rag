from urllib import response
from prometheus_client import Counter,Histogram,generate_latest,CONTENT_TYPE_LATEST

from fastapi import FastAPI,Request,Response

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import time

REQUEST_COUNT=Counter('http_req_total','total http req',['method','endpoint','status'])
REQUEST_LATENCY=Histogram('http_req_deration_seconds','http latency','[method,endpoint]')

class PromeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time=time.time()
        response= await call_next(request)

        duration=time.time()-start_time
        endpoint=request.url.path

        REQUEST_COUNT.labels(endpoint=endpoint,status=response.status_code,method=request.method).inc()
        REQUEST_LATENCY.labels(method=request.method,endpoint=endpoint).observe(duration)

        return response
    

def setup_metrics(app:FastAPI):
    app.add_middleware(PromeMiddleware)
    @app.get('/bWV0cmljcw==',include_in_schema=False)
    def metrics():
        return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)