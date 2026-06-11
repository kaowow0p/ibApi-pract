from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import BookResponse, BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookResponse])
def list_books(
    skip: int = 0,
    limit: int = 100,
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    """Получить список книг с опциональной фильтрацией по категории"""
    if category_id is not None:
        # Проверим, что категория существует
        category = crud.get_category(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        books = crud.list_books_by_category(db, category_id, skip=skip, limit=limit)
    else:
        books = crud.list_books(db, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    # Валидация: проверяем, что категория существует
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url or "",
    )


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу по ID"""
    # Проверяем, что книга существует
    existing_book = crud.get_book(db, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Если обновляем категорию, валидируем её существование
    if book.category_id is not None:
        category = crud.get_category(db, book.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    updated = crud.update_book(
        db,
        book_id,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url,
    )
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу по ID"""
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
