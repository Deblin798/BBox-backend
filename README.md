# BBox-backend

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload --port 8000
