import re
from typing import Dict, List
from api.database.db_client import db
from api.models.product_model import Product
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status

collection = db.products

async def insert_product(product: Product)->JSONResponse:
    try:
        product.creation_datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        product.modification_datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        
        if product.quantity <= 0:
            return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                content="Quantity must be at least 1.")

        if product.discount != 0:
            discount = float(product.discount/100)
            product.final_price = product.price - (product.price*discount)
        else:
            product.final_price = product.price


        product = dict(product)
        inserted = collection.insert_one(product)

        collection.update_one(
            {"_id": inserted.inserted_id},
            {"$set":
            {"id":str(inserted.inserted_id)}})
        
        created = collection.find_one({"id":str(inserted.inserted_id)})
        del created["_id"]
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=created)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=str(e))
    
async def get_product(product_id: str) -> JSONResponse:
    try:

        product = collection.find_one({"id":product_id})
        if product:
            del product["_id"]
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=product)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content='Product not found.')
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=str(e))
    

async def read_all_products(skip: int, limit: int, **filters: Dict) -> List[Product]:
    try:
        filter_query = {}
        for key, value in filters.items():
            filter_query[key] = {"$regex": re.escape(value), "$options": "i"} if isinstance(value, str) else value

        products_data = collection.find(filter_query).skip(skip).limit(limit)
        
        products = [
            Product(**{**product, "id": str(product["_id"])}) for product in products_data
        ]
        reversed_products = products[::-1]
        return reversed_products
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=str(e)) 
    
async def modify_product(product_id:str, product: Product) -> JSONResponse:
    try:
        product.modification_datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

        if product.quantity <= 0:
            return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                content="Quantity must be at least 1.")

        if product.discount != 0:
            discount = float(product.discount/100)
            product.final_price = product.price - (product.price*discount)
        else:
            product.final_price = product.price

        dict_product = dict(product)
        
        collection.update_one({"id":product_id},
                              {"$set":dict_product})
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=dict_product)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=str(e))
    
async def delete_product(product_id: str)->JSONResponse:
    try:
        collection.delete_one({"id":product_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content="Successfuly deleted!")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))