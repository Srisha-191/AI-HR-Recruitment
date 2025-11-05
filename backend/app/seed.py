from database import Base, engine, SessionLocal
from models import User, Department, Job

# ✅ Create tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    # Seed departments
    if not db.query(Department).first():
        dept1 = Department(name="HR")
        dept2 = Department(name="Engineering")
        db.add_all([dept1, dept2])
        db.commit()

    # Seed user admin
    if not db.query(User).first():
        user = User(name="Admin", email="admin@hr.com", password="admin123")
        db.add(user)
        db.commit()

    print("✅ Seed data inserted!")

if __name__ == "__main__":
    seed_data()
