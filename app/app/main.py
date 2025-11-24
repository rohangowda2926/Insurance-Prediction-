import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# 1. Load data
df = pd.read_csv("/workspaces/Insurance-Prediction-/ml/insurance.csv")

X = df.drop("charges", axis=1)
y = df["charges"]

# 2. Define feature types
categorical = ["sex", "smoker", "region"]
numeric = ["age", "bmi", "children"]

preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric),
    ]
)

# 3. Model
model = GradientBoostingRegressor(random_state=42)

pipe = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", model),
])

# 4. Train/test split and fit
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipe.fit(X_train, y_train)

# 5. Evaluate
y_pred = pipe.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"R2: {r2:.3f}, RMSE: {rmse:.2f}")

# 6. Save model into app/ directory
os.makedirs("../app/app", exist_ok=True)
joblib.dump(pipe, "../app/app/model.joblib")
print("Saved model to ../app/app/model.joblib")
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent

# Load model
model_path = BASE_DIR / "model.joblib"
model = joblib.load(model_path)

app = FastAPI(title="Insurance Charges Predictor")

# Static files and templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class InsuranceFeatures(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(features: InsuranceFeatures):
    data = pd.DataFrame([{
        "age": features.age,
        "sex": features.sex,
        "bmi": features.bmi,
        "children": features.children,
        "smoker": features.smoker,
        "region": features.region,
    }])

    pred = model.predict(data)[0]
    return {"predicted_charge": float(pred)}
