from datetime import datetime
# You will probably need more methods from flask but this one is a good start.
from flask import render_template, request, Response
from sqlalchemy.orm.exc import NoResultFound
from utils import PolicyAccounting

# Import things from Flask that we need.
from accounting import app, db

# Import our models
from models import Contact, Invoice, Policy, Payment

# Routing for the server.
@app.route("/")
def index():
    # You will need to serve something up here.
    return render_template('index.html')


@app.route("/policies/")
def policies():
    """ View for policy search page """

    return render_template('policies.html')


@app.route("/policy/", methods=['GET'])
def policy():
    """ Returns policy detail """

    policy_id = request.args.get('policy_id')
    date = request.args.get('date')

    if policy_id is None or policy_id == '':
        return Response(status=400)

    # Default date
    if not date:
        date = datetime.now().date()
    else:
        date = datetime.strptime(date, '%Y-%m-%d').date()

    # Return error page if policy not found
    try:
        policy_account = PolicyAccounting(policy_id)
    except NoResultFound as ex:
        return render_template('error.html', status=404, resource_type='Policy')

    # Retrieve relevant information about policy for view
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


@app.route("/contacts/")
def contacts():
    """ View for contacts page """

    contacts_list = Contact.query.all()

    return render_template('contacts.html', contacts=contacts_list)

@app.route("/contacts/<contact_id>/", methods=['GET'])
def contact(contact_id):
    """ View for contacts page """

    try:
        contact = Contact.query.filter_by(id=contact_id).one()
    except:
        return render_template('error.html', status=404, resource_type='Contact')

    # Get contact's policy
    contact.policy = Policy.query.filter_by(named_insured=contact.id).first()

    # Get last payment
    contact.last_payment = Payment.query.filter_by(contact_id=contact.id)\
                                        .order_by(Payment.transaction_date.desc())\
                                        .first()

    return render_template('contact_detail.html', contact=contact)
