import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(ROOT, 'data')

RAW_PATH = os.path.join(DATA_PATH, 'raw')

PROCESSED_PATH = os.path.join(DATA_PATH, 'processed')

IMAGE_PATH = os.path.join(DATA_PATH, 'image')

MODEL_PATH = os.path.join(ROOT, 'models') 