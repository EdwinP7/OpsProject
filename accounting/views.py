from datetime import datetime
# You will probably need more methods from flask but this one is a good start.
from flask import render_template, request, Response
from sqlalchemy.orm.exc import NoResultFound
from utils import PolicyAccounting

# Import things from Flask that we need.
from accounting import app, db

# Import our models
from models import Contact, Invoice, Policy

# Routing for the server.
@app.route("/")
def index():
    # You will need to serve something up here.
    return render_template('index.html')


@app.route("/policies/")
def policies():
    """ Returns all policies """

    policies = Policy.query.all()
    return render_template('policies.html', policies=policies)


@app.route("/policy/", methods=['GET'])
def policy():
    """ Returns policy detail """

    policy_id = request.args.get('policy_id')
    date = request.args.get('date')

    if policy_id is None or policy_id == '':
        return Response(status=400)

    if not date:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y-%m-%d').date()

    try:
        policy_account = PolicyAccounting(policy_id)
    except NoResultFound as ex:
        return render_template('error.html', status=404, )

    policy_details = {
        'account_balance': policy_account.return_account_balance(date),
        'agent': policy_account.agent,
        'annual_premium': policy_account.policy.annual_premium,
        'named_insured': policy_account.named_insured,
        'invoices': policy_account.policy.invoices,
        'payments': policy_account.policy.payments,
        'policy_number': policy_account.policy.policy_number,
        'date': date,
    }

    return render_template('policy_detail.html', policy_details=policy_details)
