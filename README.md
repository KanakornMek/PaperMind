
# PaperMind

DSDE project: Data sci, ML model, and BI dashboard



## How to run Subject Area Prediction Model

```
1. Go to notebooks directory find model_runner.ipynb.
2. Download the ai model in model directory from google drive
3. Open the model_runner.ipynb file
4. Install all required libraries
5. Change model_name to "/path/to/model"
6. Change "label_map.json" to "path/to/label_map.json"
```



## How to run Recommendation Model

```
1. Go to notebooks directory find recommender.ipynb.
3. Open the recommender.ipynb file
4. Install all required libraries
5. Change the csv file path to "/path/to/csv"
```

## Alternatively run the ai model as a website
```
1. Go to api directory
2. source ~/venv/bin/activate
3. uvicorn ai.model_api:app --reload
```
```
1. Go to frontend/datasci-project directory
2. npm install
3. npm run dev
```
