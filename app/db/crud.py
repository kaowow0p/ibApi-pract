from sqlalchemy.orm import Session

from .models import Book, Category


def create_category(db: Session, title: str) -> Category:
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_title(db: Session, title: str) -> Category | None:
    return db.query(Category).filter(Category.title == title).first()


def list_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, title: str) -> Category | None:
    category = get_category(db, category_id)
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    category = get_category(db, category_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True


def create_book(
    db: Session,
    title: str,
    description: str,
    price: float,
    category_id: int,
    url: str = "",
) -> Book:
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def list_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def list_books_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> list[Book]:
    return (
        db.query(Book)
        .filter(Book.category_id == category_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_book(
    db: Session,
    book_id: int,
    title: str | None = None,
    description: str | None = None,
    price: float | None = None,
    category_id: int | None = None,
    url: str | None = None,
) -> Book | None:
    book = get_book(db, book_id)
    if not book:
        return None
    if title is not None:
        book.title = title
    if description is not None:
        book.description = description
    if price is not None:
        book.price = price
    if category_id is not None:
        book.category_id = category_id
    if url is not None:
        book.url = url
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True
