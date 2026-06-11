from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    description: str | None = None
    price: float
    category_id: int
    url: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None
    url: str | None = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
