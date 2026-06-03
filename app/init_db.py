from app.db.db import init_db, SessionLocal
from app.db import crud


def seed_data():
    init_db()

    with SessionLocal() as db:
        if crud.get_category_by_title(db, "Fiction") or crud.get_category_by_title(db, "Non-fiction"):
            print("Data already seeded.")
            return

        fiction = crud.create_category(db, "Fiction")
        nonfiction = crud.create_category(db, "Non-fiction")

        crud.create_book(
            db,
            title="The Strange Case of Dr. Jekyll and Mr. Hyde",
            description="A classic novel about dual personality and morality.",
            price=8.99,
            category_id=fiction.id,
            url="",
        )
        crud.create_book(
            db,
            title="1984",
            description="A dystopian novel about surveillance and totalitarianism.",
            price=11.50,
            category_id=fiction.id,
            url="",
        )
        crud.create_book(
            db,
            title="Sapiens: A Brief History of Humankind",
            description="A wide-ranging history of human development.",
            price=14.99,
            category_id=nonfiction.id,
            url="",
        )
        crud.create_book(
            db,
            title="Atomic Habits",
            description="Practical strategies for building good habits and breaking bad ones.",
            price=12.80,
            category_id=nonfiction.id,
            url="",
        )

        print("Seed data created.")


if __name__ == "__main__":
    seed_data()
