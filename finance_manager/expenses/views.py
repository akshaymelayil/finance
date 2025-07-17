from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(e.amount for e in expenses)
    return render(request, 'expenses/dashboard.html', {
        'expenses': expenses,
        'total': total
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
