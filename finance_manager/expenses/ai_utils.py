import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime

def predict_savings(expense_qs):
    df = pd.DataFrame(list(expense_qs.values('date', 'amount')))
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
    monthly = df.groupby('month')['amount'].sum().reset_index()
    monthly['month_num'] = range(1, len(monthly)+1)

    X = monthly[['month_num']]
    y = monthly['amount']

    model = LinearRegression()
    model.fit(X, y)

    next_month = [[len(monthly)+1]]
    prediction = model.predict(next_month)[0]

    return round(prediction, 2)
