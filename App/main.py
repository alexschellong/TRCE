from fastapi import FastAPI
import uvicorn
from App.TRCE_endpoint.TRCE import TRCE_router

# Create FastAPI instance
app = FastAPI()
app.include_router(TRCE_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)




