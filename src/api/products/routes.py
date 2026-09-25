from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from .schemas import CreateProductRequest, ProductResponse
from .models import Product
from api.database import getdb
from uuid import UUID
from typing import List

products_router=APIRouter(tags=["PRODUCTS"])

@products_router.post("/create-product")
def create_product(payload: CreateProductRequest, db: Session=Depends(getdb)):

    new_product=Product(
        product_name=payload.product_name,
        price=payload.price,
        description=payload.description,
        quantity=payload.quantity
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "product_id": new_product.product_id,
        "product_name": new_product.product_name,
        "description": new_product.description,
        "quantity": new_product.quantity
    }


@products_router.get("/retrieve-all-products", response_model=List[ProductResponse])
def retrieve_all_products(db: Session=Depends(getdb)):
    products = db.query(Product).all()

    return products

@products_router.get("/retrieve-product/{product_id}", response_model=ProductResponse)
def retrieve_product(product_id : UUID, db: Session=Depends(getdb)):
    products = db.query(Product).filter(
        Product.product_id == product_id
    ).first()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )


    return products