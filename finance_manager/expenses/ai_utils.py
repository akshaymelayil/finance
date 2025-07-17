import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64


def predict_savings(expense_qs):
    if not expense_qs:
        return 0

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

def get_saving_tips(predicted_spending):
    tips = []
    if predicted_spending > 10000:
        tips.append("🧾 Try reducing food or travel expenses.")
    if predicted_spending < 5000:
        tips.append("✅ Great job! Consider investing or saving more.")
    if predicted_spending == 0:
        tips.append("📉 Start recording your expenses to get predictions.")
    return tips

def get_chart(expenses):
    if not expenses.exists():
        return None

    df = pd.DataFrame(list(expenses.values('category', 'amount')))

    if df.empty or 'category' not in df.columns:
        return None

    df = df.groupby('category').sum()

    plt.figure(figsize=(6, 4))
    df.plot(kind='bar', legend=False)
    plt.title("Expenses by Category")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return img
