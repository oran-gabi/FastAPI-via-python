from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for type safety and validation
class Product(BaseModel):
    """Product model with inventory details"""
    units: str = Field(..., description="Unit of measurement (e.g., boxes, bottles)")
    qty: int = Field(..., ge=0, description="Available quantity in stock")
    price: float = Field(..., gt=0, description="Price per unit")
    name: str = Field(..., description="Display name of the product")


class OrderResponse(BaseModel):
    """Response model for successful orders"""
    product: str
    product_name: str
    ordered_qty: int
    units: str
    remaining_qty: int
    total_price: float
    message: str


class InventoryResponse(BaseModel):
    """Response model for inventory queries"""
    products: Dict[str, Dict]
    total_products: int


# Initial catalog with more details
catalog: Dict[str, Product] = {
    "pizza": Product(
        units="boxes",
        qty=1000,
        price=12.99,
        name="Deluxe Pizza"
    ),
    "beer": Product(
        units="bottles",
        qty=500,
        price=4.50,
        name="Craft Beer"
    ),
    "burger": Product(
        units="pieces",
        qty=750,
        price=8.99,
        name="Classic Burger"
    ),
    "White Russians": Product(
        units="pieces",
        qty=1750,
        price=12.99,
        name="White Russians Cocktail"
    ),
    "fries": Product(
        units="servings",
        qty=1200,
        price=3.99,
        name="French Fries"
    )
}


# FastAPI app initialization
app = FastAPI(
    title="Food and Beverage Catalog API",
    description="Professional inventory management system for food products",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Food & Beverage Catalog API",
        "version": "2.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "inventory": "/warehouse/inventory",
            "order": "/warehouse/{product}",
            "health": "/health"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "products_available": len(catalog)
    }


@app.get("/warehouse/inventory", response_model=InventoryResponse, tags=["Warehouse"])
async def get_inventory():
    """Get complete inventory information"""
    inventory_data = {}
    
    for product_id, product in catalog.items():
        inventory_data[product_id] = {
            "name": product.name,
            "units": product.units,
            "qty": product.qty,
            "price": product.price,
            "in_stock": product.qty > 0
        }
    
    return {
        "products": inventory_data,
        "total_products": len(catalog)
    }


@app.get("/warehouse/{product}", response_model=OrderResponse, tags=["Warehouse"])
async def place_order(
    product: str,
    order_qty: int = Query(..., gt=0, description="Quantity to order (must be positive)")
):
    """
    Place an order for a specific product
    
    - **product**: Product ID (e.g., 'pizza', 'beer')
    - **order_qty**: Quantity to order (must be greater than 0)
    """
    
    # Validate product exists
    if product not in catalog:
        available_products = ", ".join(catalog.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product}' not found. Available products: {available_products}"
        )
    
    product_data = catalog[product]
    available = product_data.qty
    
    # Check availability
    if order_qty > available:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Insufficient stock",
                "requested": order_qty,
                "available": available,
                "product": product_data.name,
                "message": f"Sorry, only {available} {product_data.units} available"
            }
        )
    
    # Check if product is out of stock
    if available == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Out of stock",
                "product": product_data.name,
                "message": f"Sorry, {product_data.name} is currently out of stock"
            }
        )
    
    # Update inventory
    catalog[product].qty -= order_qty
    total_price = order_qty * product_data.price
    
    # Log the transaction
    logger.info(
        f"Order placed: {order_qty} {product_data.units} of {product_data.name}. "
        f"Remaining: {catalog[product].qty}"
    )
    
    return OrderResponse(
        product=product,
        product_name=product_data.name,
        ordered_qty=order_qty,
        units=product_data.units,
        remaining_qty=catalog[product].qty,
        total_price=round(total_price, 2),
        message=f"Successfully ordered {order_qty} {product_data.units} of {product_data.name}"
    )


@app.post("/warehouse/{product}/restock", tags=["Warehouse"])
async def restock_product(
    product: str,
    restock_qty: int = Query(..., gt=0, description="Quantity to add to inventory")
):
    """
    Restock a product (admin operation)
    
    - **product**: Product ID
    - **restock_qty**: Quantity to add to inventory
    """
    
    if product not in catalog:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product}' not found"
        )
    
    old_qty = catalog[product].qty
    catalog[product].qty += restock_qty
    new_qty = catalog[product].qty
    
    logger.info(f"Restocked {product}: {old_qty} -> {new_qty} (+{restock_qty})")
    
    return {
        "product": product,
        "product_name": catalog[product].name,
        "previous_qty": old_qty,
        "restocked_qty": restock_qty,
        "new_qty": new_qty,
        "message": f"Successfully restocked {restock_qty} {catalog[product].units}"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)