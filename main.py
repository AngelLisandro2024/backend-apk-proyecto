from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechShop API - Tienda de Componentes",
    description="API RESTful para catálogo de laptops, RAM y tarjetas gráficas",
    version="1.0.0"
)

# Precargar datos de prueba
def seed_data():
    db = next(get_db())
    if db.query(models.Category).count() == 0:
        laptops = models.Category(name="Laptops", slug="laptops")
        gpus = models.Category(name="Tarjetas de Video", slug="gpus")
        ram = models.Category(name="Memorias RAM", slug="ram")
        
        db.add_all([laptops, gpus, ram])
        db.commit()

        prods = [
            models.Product(
                title="Laptop Gamer ASUS ROG Strix G16",
                description="Core i7-13650HX, 16GB RAM, 1TB SSD, RTX 4060",
                price=1399.99,
                stock=5,
                image_url="https://via.placeholder.com/400x300?text=ASUS+ROG+Strix",
                brand="ASUS",
                category_id=laptops.id
            ),
            models.Product(
                title="NVIDIA GeForce RTX 4070 Super 12GB",
                description="Tarjeta gráfica de alto rendimiento para gaming 1440p",
                price=649.99,
                stock=8,
                image_url="https://via.placeholder.com/400x300?text=RTX+4070+Super",
                brand="NVIDIA",
                category_id=gpus.id
            ),
            models.Product(
                title="Memoria RAM Corsair Vengeance DDR5 32GB (2x16GB)",
                description="6000MHz CL36 Expo & XMP 3.0",
                price=115.00,
                stock=20,
                image_url="https://via.placeholder.com/400x300?text=Corsair+DDR5",
                brand="Corsair",
                category_id=ram.id
            )
        ]
        db.add_all(prods)
        db.commit()

seed_data()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de TechShop"}

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

@app.post("/products", response_model=schemas.ProductResponse, tags=["Administración"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product