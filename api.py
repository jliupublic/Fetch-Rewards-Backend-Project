import flask
from flask import render_template, request, jsonify
import heapq
import collections

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

class Transaction(object):
    def __init__(self, payer, points, timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp

    def __repr__(self):
        return 'Payer: {}, Points: {}, Timestamp: {}'.format(self.payer, self.points, self.timestamp)

    def __lt__(self, other):
        return self.timestamp < other.timestamp # compare timestamps

    def to_dict(self):
        return {'payer': self.payer, 'points': self.points, 'timestamp': self.timestamp}

heap = [] # efficient access to earliest timestamp
balances = collections.OrderedDict() # preserve insertion order

@app.route('/', methods=['GET'])
def home():
    return "<h1>Fetch Rewards Backend Project</h1> \
    <p>This site is a service for tracking points paid and spent by payers and users.</p> \
    <ul><li>Add transactions by filling out the form at <a href=/add>/add</a> </li> \
    <li>Spend points at <a href=/spend>/spend</a></li> \
    <li>View payer point balances at <a href=/balances>/balances</a></li></ul>", 200

@app.route('/balances', methods=['GET'])
def get_balances():
    return jsonify(balances), 200

@app.route('/add', methods=['POST', 'GET'])
def add_transaction():
    if request.method == 'GET':
        return render_template('transaction_form.html'), 200
    if request.method == 'POST':
        if request.form['payer'] and request.form['points'] and request.form['timestamp']:
            payer = request.form['payer']
            try:
                points = int(request.form['points'])
            except ValueError:
                return 'Error: points must be an integer', 400
            timestamp = request.form['timestamp']

            balances.setdefault(payer, 0)
            if balances[payer] + points < 0:
                return 'Error: adding {} points would make {}\'s balance negative'.format(points, payer), 409
            balances[payer] += points

            new_transaction = Transaction(payer, points, timestamp)
            heapq.heappush(heap, new_transaction)
            return jsonify(new_transaction.to_dict()), 200
        else:
            return 'Error: missing argument. Please resubmit the form with a payer, points, and a timestamp', 400

@app.route('/spend', methods=['POST', 'GET'])
def spend_points():
    if request.method == 'GET':
        return render_template('spend_form.html'), 200
    if request.method == 'POST':
        if request.form['points']:
            try:
                points = int(request.form['points'])
            except ValueError:
                return 'Error: points must be an integer', 400
            output_dict = {}
            if sum([t.points for t in heap]) < points:
                return 'Error: not enough points to spend', 409
            while heap and points > 0:
                transaction = heap[0]
                # if not all points will be spent in this transaction
                if points < transaction.points:
                    transaction.points -= points
                    output_dict.setdefault(transaction.payer, 0)
                    output_dict[transaction.payer] -= points
                    balances[transaction.payer] -= points
                    break
                # all points will be spent in this transaction
                else:
                    points -= transaction.points
                    output_dict.setdefault(transaction.payer, 0)
                    output_dict[transaction.payer] -= transaction.points
                    balances[transaction.payer] -= transaction.points
                    heapq.heappop(heap)

            # ensure results are given in insertion order
            index_map = {k: i for i, k in enumerate(balances.keys())}
            sorted_tuples = sorted(output_dict.items(), key=lambda kv: index_map[kv[0]])
            sorted_dict = collections.OrderedDict(sorted_tuples)

            # formatting
            output_list = [{'payer': k, 'points': v} for k, v in sorted_dict.items()]
            return jsonify(output_list), 200
        else:
            return 'Error: missing argument. Please resubmit the form with the number of points', 400

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=8080)
# app.run()
