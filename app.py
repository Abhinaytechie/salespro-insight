from flask import Flask, render_template, request
import numpy as np
import datetime as dt
import joblib

app = Flask(__name__)


current_year = dt.datetime.today().year

def predict_sales(Item_MRP, Outlet_Identifier, Outlet_Size, Outlet_Type, Outlet_Establishment_Year, Outlet_Location_Type):
    p2 = outlet_mapping.get(Outlet_Identifier, 0)
    p3 = size_mapping.get(Outlet_Size, 0)
    p4 = type_mapping.get(Outlet_Type, 0)
    p5 = current_year - Outlet_Establishment_Year
    p6 = location_mapping.get(Outlet_Location_Type, 0)  # New mapping for Outlet_Location_Type
    model = joblib.load('bigmart_model')
    result = model.predict(np.array([[Item_MRP, p2, p3, p4, p5, p6]]))[0]
    
    return render_template('result.html', result=result)
# Dropdown mappings
outlet_mapping = {'OUT010': 0, 'OUT013': 1, 'OUT017': 2, 'OUT018': 3, 'OUT019': 4,
                  'OUT027': 5, 'OUT035': 6, 'OUT045': 7, 'OUT046': 8, 'OUT049': 9}

size_mapping = {'High': 0, 'Medium': 1, 'Small': 2}

type_mapping = {'Grocery Store': 0, 'Supermarket Type1': 1, 'Supermarket Type2': 2, 'Supermarket Type3': 3}
location_mapping = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        Item_MRP = float(request.form['e1'])
        Outlet_Identifier = request.form['e2']
        Outlet_Size = request.form['e3']
        Outlet_Type = request.form['e4']
        Outlet_Establishment_Year = int(request.form['e5'])
        Outlet_Location_Type = request.form['e6']  # Extract Outlet_Location_Type

        return predict_sales(Item_MRP, Outlet_Identifier, Outlet_Size, Outlet_Type, Outlet_Establishment_Year, Outlet_Location_Type)


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change the port number to 5001 or another available port
