# main
"""
va a inicializar la api
va a iniciar la app del backend
va a tener las rutas de la api
lo levanta en el servidor
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db

from app.routes.product_routes import router as product_router
from app.routes.product_payment_routes import router as product_payment_router
from app.routes.payment_method_routes import router as payment_method_router
from app.routes.customer_routes import router as customer_router
from app.routes.customer_address_routes import router as customer_address_router
from app.routes.orders_routes import router as orders_router
from app.routes.order_detail_routes import router as order_detail_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db
    yield

app = FastAPI(
    title= "pasteleria API MVC",
    version= "1.0.0",
    lifespan= lifespan
    )

app.include_router(product_router)
app.include_router(product_payment_router)
app.include_router(payment_method_router)
app.include_router(customer_router)
app.include_router(customer_address_router)
app.include_router(orders_router)
app.include_router(order_detail_router)

if __name__ = "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()

