import sys
sys.path.insert(0, './backend')
from app import app

if __name__ == "__main__":
    app.run()

web: cd backend && gunicorn app:app