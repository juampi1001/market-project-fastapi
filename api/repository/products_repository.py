from typing import List, Optional
from fastapi import APIRouter, Query, UploadFile, status
from fastapi.responses import JSONResponse
from api.datasource.products_datasource import (insert_product,get_product,
                                                modify_product,delete_product,
                                                read_all_products)
from api.helpers.firebase.firebase_storage import upload_lists_to_firebase
from api.models.product_model import Product

router = APIRouter(tags=['products'])

@router.post("/product-images")
async def upload_product_images(images: List[UploadFile]):
    response = await upload_lists_to_firebase(images, "products")
    return response

@router.post("/products")
async def create_new_product(product: Product):
    return await insert_product(product)

@router.get("/products/{product_id}")
async def see_product_info(product_id: str):
    return await get_product(product_id)

@router.get("/products/")
async def read_all_products_api(
    page: Optional[int] = Query(1, gt=0),
    per_page: Optional[int] = Query(10, gt=0),
    queryParams: Optional[str] = None
):
    if queryParams:
        queryParams = dict(item.split("=") for item in queryParams.split("&"))
    else:
        queryParams = {}
    skip = (page - 1) * per_page
    return await read_all_products(**queryParams, limit=per_page, skip=skip)

@router.put("/products/{product_id}")
async def update_product_info(product_id: str, product: Product):
    return await modify_product(product_id, product)

@router.delete("/products/{product_id}")
async def delete_this_product(product_id: str):
    return await delete_product(product_id)