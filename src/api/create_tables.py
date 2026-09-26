from .database import engine, Base

from .products.models import *

Base.metadata.create_all(bind=engine)