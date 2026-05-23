import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    # Validate inputs
    if sqft < 100:
        raise ValueError("Area must be at least 100 sq ft")
    if sqft > 50000:
        raise ValueError("Area cannot exceed 50,000 sq ft")
    if bhk < 1 or bhk > 10:
        raise ValueError("BHK must be between 1 and 10")
    if bath < 1 or bath > 10:
        raise ValueError("Bathrooms must be between 1 and 10")
    if not location or location.strip() == "":
        raise ValueError("Please select a valid location")
    
    # Find location in the list (case-insensitive)
    loc_index = -1
    if __locations:
        for i, loc in enumerate(__locations):
            if loc.lower() == location.lower():
                loc_index = i + 3  # +3 because first 3 columns are sqft, bath, bhk
                break
    
    if loc_index < 0:
        raise ValueError(f"Location '{location}' not found in our database")

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Get the directory where this file is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(base_dir, 'artifacts')
    
    columns_path = os.path.join(artifacts_dir, 'columns.json')
    model_path = os.path.join(artifacts_dir, 'banglore_home_prices_model.pickle')
    
    print(f"Loading artifacts from: {artifacts_dir}")
    print(f"Columns file exists: {os.path.exists(columns_path)}")
    print(f"Model file exists: {os.path.exists(model_path)}")

    with open(columns_path, 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    with open(model_path, 'rb') as f:
        __model = pickle.load(f)
    print("loading saved artifacts...done")


def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2))
