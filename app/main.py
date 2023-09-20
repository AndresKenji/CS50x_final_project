from fastapi                    import FastAPI, status
from fastapi.middleware.cors    import CORSMiddleware
from fastapi.middleware         import Middleware
from fastapi.staticfiles        import StaticFiles
from fastapi.responses          import RedirectResponse

import sys
sys.path.append('.')
from src.routes import users, food_drinks, menu, orders, invoice, home


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers= ["*"]
    )
]

app = FastAPI(
    title="API Restaurant",
    description="API for manage restaurant customers, food, drinks and orders",
    version="0.1",
    openapi_url="/openapi.json", 
    docs_url="/docs",
    middleware=middleware
)

app.mount("/static",StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/home", status_code=status. HTTP_302_FOUND)

app.include_router(users.router)
app.include_router(food_drinks.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(invoice.router)
app.include_router(home.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, host='0.0.0.0')