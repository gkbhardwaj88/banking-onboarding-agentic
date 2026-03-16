from backend.db.session import Base, engine

def run_migrations():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    run_migrations()
