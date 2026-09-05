from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

import models, schemas
from database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechShop API - Tienda de Componentes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def seed_data():
    db = SessionLocal()
    try:
        if db.query(models.Category).count() == 0:
            laptops = models.Category(name="Laptops", slug="laptops")
            gpus = models.Category(name="Tarjetas de Video", slug="gpus")
            ram = models.Category(name="Memorias RAM", slug="ram")
            
            db.add_all([laptops, gpus, ram])
            db.commit()

            prods = [
                models.Product(
                    title="Laptop Gamer ASUS ROG Strix G16",
                    description="Procesador Intel Core i7-13650HX, 16GB RAM DDR5, 1TB SSD NVMe, NVIDIA RTX 4060 8GB, Pantalla 16'' 165Hz.",
                    price=1399.99,
                    stock=5,
                    image_url="https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80",
                    brand="ASUS",
                    category_id=laptops.id
                ),
                models.Product(
                    title="NVIDIA GeForce RTX 4070 Super 12GB",
                    description="Arquitectura Ada Lovelace, DLSS 3, Ray Tracing de 3ra generación. Rendimiento masivo para gaming a 1440p y renderizado 3D.",
                    price=649.99,
                    stock=8,
                    image_url="https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800&auto=format&fit=crop&q=80",
                    brand="NVIDIA",
                    category_id=gpus.id
                ),
                models.Product(
                    title="Memoria RAM Corsair Vengeance DDR5 32GB",
                    description="Kit de 32GB (2x16GB) 6000MHz CL36. Disipador de aluminio anodizado, compatibilidad total con Intel XMP 3.0 y AMD EXPO.",
                    price=115.00,
                    stock=20,
                    image_url="https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&auto=format&fit=crop&q=80",
                    brand="Corsair",
                    category_id=ram.id
                )
            ]
            db.add_all(prods)
            db.commit()
    finally:
        db.close()

seed_data()

@app.get("/", include_in_schema=False)
def read_index():
    return FileResponse(os.path.join("templates", "index.html"))

@app.get("/categories", response_model=List[schemas.CategoryResponse], tags=["Catálogo"])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.get("/products", response_model=List[schemas.ProductResponse], tags=["Catálogo"])
def get_products(category_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    return query.all()

@app.get("/products/{product_id}", response_model=schemas.ProductResponse, tags=["Catálogo"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product