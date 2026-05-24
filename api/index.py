"""
NOVOPLAST Store — Vercel Serverless FastAPI Backend
Handles custom orders with personalization text, file uploads, and Razorpay payment integration.
Deployed as a Vercel Python Serverless Function.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from mangum import Mangum
import uuid
import os
import json
from datetime import datetime

# ── Optional: Razorpay SDK ──
try:
    import razorpay
    RAZORPAY_ENABLED = True
except ImportError:
    RAZORPAY_ENABLED = False

# ── Config ──
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_XXXXXXXXXX")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "your_razorpay_secret")

# In-memory store for serverless (use a database in production)
orders_store = []

# ── App ──
app = FastAPI(
    title="NOVOPLAST Store API",
    description="API for handling custom non-tearable print orders",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ──
def create_razorpay_order(amount_paise: int):
    """Create a Razorpay order. Returns order details or None if SDK unavailable."""
    if not RAZORPAY_ENABLED:
        return None
    try:
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
        })
        return order
    except Exception as e:
        print(f"Razorpay error: {e}")
        return None


# ── Routes ──
@app.get("/api")
async def root():
    return {
        "service": "NOVOPLAST Store API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /api/orders": "Create a new custom order",
            "GET /api/orders": "List all orders",
            "GET /api/orders/{order_id}": "Get order details",
        },
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/orders")
async def create_order(
    product_id: str = Form(...),
    product_name: str = Form(...),
    size: str = Form(""),
    quantity: str = Form("1"),
    personalization_text: str = Form(""),
    shloka: str = Form(""),
    total_price: float = Form(...),
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    design_file: Optional[UploadFile] = File(None),
):
    """
    Create a new custom order.

    - Captures personalization text (for Spiritual Prints / Custom Posters)
    - Handles file upload metadata (for Custom Stickers)
    - Creates a Razorpay payment order (if SDK is available)
    """

    order_id = str(uuid.uuid4())[:8].upper()
    file_info = None

    # Handle file upload metadata
    if design_file:
        allowed_types = ["image/jpeg", "image/png", "image/svg+xml"]
        if design_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {design_file.content_type}. Allowed: JPG, PNG, SVG",
            )
        contents = await design_file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Max 10MB.")
        file_info = {
            "filename": design_file.filename,
            "content_type": design_file.content_type,
            "size": len(contents),
        }

    # Build order record
    order = {
        "order_id": order_id,
        "product_id": product_id,
        "product_name": product_name,
        "size": size,
        "quantity": quantity,
        "personalization_text": personalization_text,
        "shloka": shloka,
        "total_price": total_price,
        "customer": {
            "name": customer_name,
            "email": customer_email,
            "phone": customer_phone,
        },
        "design_file": file_info,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }

    orders_store.append(order)

    # Create Razorpay order
    amount_paise = int(total_price * 100)
    razorpay_order = create_razorpay_order(amount_paise)

    response = {
        "message": "Order created successfully",
        "order_id": order_id,
        "order": order,
    }

    if razorpay_order:
        response["razorpay_order_id"] = razorpay_order["id"]
        response["razorpay_key_id"] = RAZORPAY_KEY_ID
        response["amount"] = amount_paise

    return response


@app.get("/api/orders")
async def list_orders():
    """List all orders."""
    return {"orders": orders_store}


@app.get("/api/orders/{order_id}")
async def get_order(order_id: str):
    """Get a specific order by ID."""
    for o in orders_store:
        if o["order_id"] == order_id:
            return {"order": o}
    raise HTTPException(status_code=404, detail="Order not found")


# ── Vercel Serverless Handler ──
handler = Mangum(app)
