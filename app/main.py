from app.db.db import SessionLocal
from app.db import crud


def print_data():
	with SessionLocal() as db:
		categories = crud.list_categories(db)
		if not categories:
			print("No categories found.")
			return

		for category in categories:
			print(f"Category {category.id}: {category.title}")
			for book in category.books:
				print(
					f"  Book {book.id}: {book.title} | price={book.price} | url={book.url or '<empty>'}"
				)

		print("\nAll books summary:")
		books = crud.list_books(db)
		for book in books:
			print(
				f"Book {book.id}: {book.title} | category_id={book.category_id} | price={book.price}"
			)


if __name__ == "__main__":
	print_data()
