from fastapi import FastAPI
from docs.redoc import setup_redoc
from modules.vpc import router as vpc_router
import uvicorn

from fastapi import FastAPI

app = FastAPI()
setup_redoc(app)
app.include_router(vpc_router)

    
if __name__ == '__main__':
    uvicorn.run("vpc:app", host="0.0.0.0", port=5000, reload=True, workers=2)

