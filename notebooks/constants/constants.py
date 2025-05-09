import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(ROOT, 'data')

RAW_PATH = os.path.join(DATA_PATH, 'raw')

PROCESSED_PATH = os.path.join(DATA_PATH, 'processed')

IMAGE_PATH = os.path.join(DATA_PATH, 'image')

MODEL_PATH = os.path.join(ROOT, 'models') 

METRICS_PATH = os.path.join(DATA_PATH, 'metrics')


# カラム
MAIN_FEATURES = [
    'log_total_sf',
    'house_age', 'remod_age', 'yrs_before_remod', 'year_price',
    'OverallQual_weight', 'ExterQual_weight', 'KitchenQual_weight',
    'neighbor_log_price_stdscaled', 
    'has_2nd', 'has_bsmt', 'has_garage', 'has_pool'
    ]

TARGET = 'log_price'