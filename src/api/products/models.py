from sqlalchemy import Column, Integer, String, Boolean
from api.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Product(Base):
    __tablename__="products"
    product_id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name=Column(String(50), nullable=True)
    price=Column(String, nullable=False)
    description=Column(String, nullable=True)
    quantity=Column(Integer, default=1)