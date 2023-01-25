from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from docs.redoc import setup_redoc
from modules.vpc.vpc import router as vpc_router
from modules.subnets.subnets import router as subnet_router
import os
import uvicorn

from fastapi import FastAPI

app = FastAPI(redoc_url=None)
setup_redoc(app)
app.include_router(vpc_router)
app.include_router(subnet_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cloud Fast",
        version="3.0.0",
        description="Cloud Fast",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": os.path.normpath(os.getcwd() + "/assets/flc_design20230122107992.png"),
        "backgroundColor": "#FFFFFF"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

    
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, workers=2)

