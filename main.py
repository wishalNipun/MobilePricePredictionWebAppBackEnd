from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Float, String, Integer, DateTime
from datetime import datetime
from sqlalchemy import desc 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "mysql+mysqlconnector://root:wishal123@machinelearningdatabase.c3wk8ouk4g8g.us-east-1.rds.amazonaws.com/machineLearningProjectDatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class MobileForm(BaseModel):
    brand: str
    color: str
    model: str
    memory: str
    storage: str

class savePredictionTable(Base):
    __tablename__ = "prediction_details"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), index=True)
    color = Column(String(50), index=True)
    model = Column(String(50), index=True)
    memory = Column(String(50), index=True)
    storage = Column(String(50), index=True)
    predicted_value = Column(Float)
    save_date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)    

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

    brand_list = ['ASUS','Apple','GIONEE','Google Pixel','HTC','IQOO','Infinix','LG',
                  'Lenovo','Motorola','Nokia','OPPO','POCO','SAMSUNG','Xiaomi','realme','vivo']
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
        
        lkrRupee = predicted_value * 3.85
        
        print(predicted_value, 'd' , lkrRupee)

        db_data = savePredictionTable(
            brand=brand,
            color=color,
            model=model,
            memory=memory,
            storage=storage,
            predicted_value= float(lkrRupee)
        )
        print("DB Data:", db_data)
        db = SessionLocal()
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        db.close()
        
        return {"message": "Form data submitted successfully?", "predicted_value": round(lkrRupee,3)}
    
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/allData")
def get_all_table_data():
    db = SessionLocal()
    try:
        data = db.query(savePredictionTable).order_by(desc(savePredictionTable.save_date)).all()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

