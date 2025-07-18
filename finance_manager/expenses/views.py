from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from .forms import ExpenseForm
from .ai_utils import predict_savings, get_chart, get_saving_tips

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    
    if not expenses.exists():
        return render(request, 'expenses/dashboard.html', {
            'message': 'No expenses added yet.',
        })

    # Convert to DataFrame
    df = pd.DataFrame(list(expenses.values()))

    # Safety check
    if 'category' not in df.columns or 'amount' not in df.columns:
        return render(request, 'expenses/dashboard.html', {
            'message': 'Required data is missing.',
        })

    # ✅ Convert 'amount' to numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # Drop NaNs just in case
    df.dropna(subset=['amount', 'category'], inplace=True)

    # Group and plot
    category_group = df.groupby('category')['amount'].sum()

    fig, ax = plt.subplots()
    category_group.plot(kind='bar', ax=ax)
    ax.set_title('Expenses by Category')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'expenses/dashboard.html', {
        'chart': image_base64,
    })


def get_chart(expenses):
    df = pd.DataFrame(list(expenses.values('category', 'amount')))
    df = df.groupby('category').sum()

    plt.figure(figsize=(6,4))
    df.plot(kind='bar')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode()
    buffer.close()
    return img

def get_saving_tips(predicted_spending):
    tips = []
    if predicted_spending > 10000:
        tips.append("Try reducing dining or travel expenses.")
    if predicted_spending < 5000:
        tips.append("Great job! Consider investing more.")
    return tips
