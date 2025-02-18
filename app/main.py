from fastapi import FastAPI
from app.controllers import auth_controller
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(title="DealerHub API", version="1.0.0", docs_url=None)

app.include_router(auth_controller.router)

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)