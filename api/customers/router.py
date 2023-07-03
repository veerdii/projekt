from fastapi import APIRouter, HTTPException, Query

from .storage import get_customers_storage
from .schema import CustomerCreateSchema, CustomerUpdateSchema, Customer

router = APIRouter()


CUSTOMERS_STORAGE = get_customers_storage()


@router.get("/customers")
async def get_customers() -> list[Customer]:
    return list(get_customers_storage().values())


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: int) -> Customer:
    try:
        return CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )


@router.patch("/customers/{customer_id}")
async def update_customer(
    customer_id: int, updated_customer: CustomerUpdateSchema
) -> Customer:
    if customer_id not in CUSTOMERS_STORAGE:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )
    customer = CUSTOMERS_STORAGE[customer_id]
    if updated_customer.name is not None:
        customer.name = updated_customer.name
    if updated_customer.surname is not None:
        customer.surname = updated_customer.surname
    if updated_customer.email is not None:
        customer.email = updated_customer.email
    if updated_customer.phone_number is not None:
        customer.phone_number = updated_customer.phone_number
    return customer


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int) -> None:
    try:
        del CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )


@router.post("/customers")
async def create_customer(customer: CustomerCreateSchema) -> Customer:
    new_customer = Customer(
        id=len(CUSTOMERS_STORAGE) + 1,
        name=customer.name,
        surname=customer.surname,
        email=customer.email,
        phone_number=customer.phone_number,
    )   
    CUSTOMERS_STORAGE[new_customer.id] = new_customer
    return new_customer  