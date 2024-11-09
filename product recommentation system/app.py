from flask import Flask, render_template, request
import pandas as pd
from apyori import apriori

app = Flask(__name__)
bill = []

def load_data():
    dataset = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
    transactions = []
    for i in range(0, 7501):
        transactions.append([str(dataset.values[i, j]) for j in range(0, 20) if str(dataset.values[i, j]) != 'nan'])
    return transactions

def get_recommendations(item):
    transactions = load_data()
    rules = apriori(transactions, min_support=0.002, min_confidence=0.1, min_lift=1, min_length=2, max_length=2)
    results = list(rules)

    lhs = []
    rhs = []
    for result in results:
        for relation_record in result.ordered_statistics:
            lhs.append(tuple(relation_record.items_base))
            rhs.append(tuple(relation_record.items_add))
    
    recommendations = []
    for left, right in zip(lhs, rhs):
        if item in left:
            recommendations.extend([x for x in right if x != item])
    
    return list(set(recommendations))

@app.route('/', methods=['GET', 'POST'])
def index():
    global bill
    recommendations = []
    if request.method == 'POST':
        item = request.form.get('item')
        if item:
            bill.append(item)
            recommendations = get_recommendations(item)
            print(f"Item received: {item}")  # Debug statement
            print(f"Recommendations: {recommendations}")  # Debug statement

    return render_template('index.html', bill=bill, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
