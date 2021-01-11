from flask import Flask,render_template,request
from datetime import datetime
import pickle


app = Flask(__name__,template_folder='Templates')
Model = pickle.load(open("Price_Prediction_Model.pkl","rb"))

@app.route("/",methods=['POST','GET'])
def price_prediction():
    if request.method == 'POST':
        Present_Price     = float(request.form['Present_Price'])
        Bought_Year           = int(request.form['Bought_Year'])
        Kms_Driven        = int(request.form['Kms_Driven'])
        Seller_Type       = request.form['Seller_Type']
        Transmission_Type = request.form['Transmission_Type']
        Fuel_Type         = request.form['Fuel_Type']
        Current_Year = datetime.now().year
        car = {
            'present_price':Present_Price,
            'bought_year': Bought_Year,
            'total_kms':Kms_Driven,
            'fuel_type':Fuel_Type,
            'seller_type':Seller_Type,
            'transmission_type':Transmission_Type
        }
        
        if(Seller_Type == 'Individual'):
            Seller_Type = 1
        else:
            Seller_Type = 0  

        if(Transmission_Type == 'Manual'):
            Transmission_Type=1
        else:
            Transmission_Type=0 

        if(Fuel_Type == 'Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif(Fuel_Type == 'Diesel'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0 

        No_Year = Current_Year - Bought_Year
        Present_Price = Present_Price/100000                            
        data = [Present_Price,Kms_Driven,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type,Transmission_Type,No_Year]
        predicted_Value = Model.predict([data])
        selling_price = round(predicted_Value[0],2)


        if selling_price < 0:
            selling_price = None
            
        return render_template('prediction.html',selling_price=selling_price,car=car)
    
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
