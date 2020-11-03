from flask import Flask,render_template,request
import pickle
import sklearn


app = Flask(__name__)
Model = pickle.load(open("Price_Prediction_Model.pkl","rb"))

@app.route("/",methods=['POST','GET'])
def price_prediction():
    if request.method == 'POST':
        Present_Price     = float(request.form['Present_Price'])
        No_Year           = int(request.form['No_Year'])
        Kms_Driven        = int(request.form['Kms_Driven'])
        Seller_Type       = request.form['Seller_Type']
        Transmission_Type = request.form['Transmission_Type']
        Fuel_Type         = request.form['Fuel_Type']

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

        No_Year = 2020 - No_Year                            
        data = [Present_Price,Kms_Driven,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type,Transmission_Type,No_Year]
        predicted_Value = Model.predict([data])
        selling_price = round(predicted_Value[0],2)

        if selling_price < 0:
            return render_template('index.html',text='you cant sell this car')
        else:
            return render_template('index.html',text='You can sell your Car at {} Lakh INR '.format(selling_price))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost',debug=False)