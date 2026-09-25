from .database import engine, Base

from .products.models import *
from .users.models import *

Base.metadata.create_all(bind=engine)