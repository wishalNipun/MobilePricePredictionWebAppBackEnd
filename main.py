from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import pandas as pd

import pickle

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class MobileForm(BaseModel):
    brand: str
    color: str
    model: str
    memory: str
    storage: str

def prediction(input_list):
    file_path = 'model/predictor.pickle'
   
    feature_names = ['Memory', 'Storage', 'Brand_ASUS', 'Brand_Apple', 'Brand_GIONEE',
       'Brand_Google Pixel', 'Brand_HTC', 'Brand_IQOO', 'Brand_Infinix',
       'Brand_LG', 'Brand_Lenovo', 'Brand_Motorola', 'Brand_Nokia',
       'Brand_OPPO', 'Brand_POCO', 'Brand_SAMSUNG', 'Brand_Xiaomi',
       'Brand_realme', 'Brand_vivo', 'model_name_Galaxy', 'model_name_Hot',
       'model_name_Other', 'model_name_Redmi', 'model_name_Zenfone',
       'model_name_iPhone', 'color_name_Black', 'color_name_Blue',
       'color_name_Gold', 'color_name_Other', 'color_name_Silver',
       'color_name_White']
    
    input_value = pd.DataFrame([input_list], columns=feature_names)

    with open(file_path, 'rb') as file:
            
        model = pickle.load(file)
        print("Pickle file is running correctly.")
        print("Loaded data:", model)
    pred_value = model.predict(input_value)
    
   
    return pred_value

  

@app.post("/featureMobile")
async def submit_mobile_form(mobile_data: MobileForm):
    # Access the submitted data using mobile_data
    brand = mobile_data.brand
    color = mobile_data.color
    model = mobile_data.model
    memory = mobile_data.memory
    storage = mobile_data.storage

    brand_list = ['ASUS','Apple','GIONEE','Google Pixel','HTC','IQOO','Infinix','LG','Lenovo','Motorola','Nokia','OPPO','POCO','SAMSUNG','Xiaomi','realme','vivo']
    model_list = ['Galaxy','Hot','Other','Redmi','Zenfone','iPhone']
    color_list = ['Black','Blue','Gold','Other','Silver','White']
    
    featur_Mobile_list=[]
    featur_Mobile_list.append(float(memory))
    featur_Mobile_list.append(float(storage))

    def setDataArray(list,value):
        for item in list:
            if item == value:
                featur_Mobile_list.append(1)
            else:
                featur_Mobile_list.append(0)

    setDataArray(brand_list,brand)
    setDataArray(model_list,model)
    setDataArray(color_list,color)

    print(brand,color,model,memory,storage)
    print(featur_Mobile_list)
    
    try:
        predvalue = prediction(featur_Mobile_list)
        predicted_value = predvalue[0]
        print(predicted_value)

        return {"message": "Form data submitted successfully?", "predicted_value": predicted_value}
    except Exception as e:
       
        raise HTTPException(status_code=500, detail=str(e))