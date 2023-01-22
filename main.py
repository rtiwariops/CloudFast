from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from docs.redoc import setup_redoc
from modules.vpc import router as vpc_router
import uvicorn

from fastapi import FastAPI

app = FastAPI(redoc_url=None)
setup_redoc(app)
app.include_router(vpc_router)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi

    
if __name__ == '__main__':
    uvicorn.run("vpc:app", host="0.0.0.0", port=5000, reload=True, workers=2)

