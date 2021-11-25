from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.Contractor
donations = db.donations
charities = db.donations

app = Flask(__name__)

# Home Page (Shows a list of donations & charities)
@app.route('/')
def home_page():
  all_donations = donations.find()
  all_charities = charities.find()
  return render_template('home_page.html', all_donations=all_donations, all_charities=all_charities)

# Grabs all of the donations
@app.route('/donations', methods=['GET'])
def all_donations():
  all_donations = donations.find()
  all_charities = charities.find()
  return render_template('all_donations.html', all_donations=all_donations, all_charities=all_charities)

# Grabs all of the charities
@app.route('/charities', methods=['GET'])
def all_charities():
  all_charities = charities.find()
  return render_template('all_charities.html', all_charities=all_charities)

# Create single donation
@app.route('/donations', methods=['POST'])
def create_donation():
  if request.form.get('charity') == '':
    return render_template('new_charity.html')
  else:
    new_donation = {
      'charity_id': request.form.get('charity'),
      'amount': request.form.get('amount'),
      'notes': request.form.get('notes'),
      'user_name': request.form.get('name')
    }
    single_charity = charities.find_one({'_id': ObjectId(request.form.get('charity'))})
    charity_donations = int(single_charity['total_dontations'])
    charity_donated = int(single_charity['total_donated'])
    single_charity['total_dontations'] = charity_donations + 1
    single_charity['total_donated'] = charity_donated + int(request.form.get('amount'))
    single_charity['all_donations'].append(new_donation)
    charities.update_one({'_id': ObjectId(request.form.get('charity'))}, {'$set': single_charity})
    donations.insert_one(new_donation)
    all_donations = donations.find()
    all_charities = charities.find()
    return render_template('home_page.html', all_donations=all_donations, all_charities=all_charities)

# Create single charity
@app.route('/charities', methods=['POST'])
def create_charity():
  print(request.form.get('name'))
  print(request.form.get('category'))
  new_charity = {
    'name': request.form.get('name'),
    'category': request.form.get('category'),
    'total_dontations': 0,
    'total_donated': 0,
    'all_donations': [],
    'created_at': datetime.now()
  }
  charities.insert_one(new_charity)
  all_donations = donations.find()
  all_charities = charities.find()
  return render_template('home_page.html', all_donations=all_donations, all_charities=all_charities)


#update a donatoin
@app.route('/donations/<donation_id>', methods=['POST'])
def update_donation(donation_id):
  donation_to_update = donations.find_one({'_id': ObjectId(donation_id)})
  updated_donation = {
    'charity_name': request.form.get('charity_name'),
    'amount': request.form.get('amount'),
    'notes': request.form.get('notes'),
    'user_name': request.form.get('user_name')
  }
  #update the charity info to reflect the change in donation
  single_donation = donations.find_one({'_id': ObjectId(donation_id)})
  donations.update_one({'_id': ObjectId(donation_id)}, {'$set': updated_donation})
  return render_template('donation_single.html', single_donation=single_donation)

#update a charity
@app.route('/donations/<charity_id>', methods=['POST'])
def update_charity(charity_id):
  charity_to_update = charities.find_one({'_id': ObjectId(charity_id)})
  updated_charity = {
    'name': request.form.get('charity_name'),
    'category': request.form.get('amount'),
    'total_dontations': charity_to_update['total_donatoins'],
    'total_donated': charity_to_update['total_donated'],
    'all_donations': charity_to_update['all_donations'],
    'created_at': charity_to_update['created_at'],
  }
  single_charity = charities.find_one({'_id': ObjectId(charity_id)})
  charities.update_one({'_id': ObjectId(charity_id)}, {'$set': updated_charity})
  return render_template('charity_single.html', single_charity=single_charity)

# Donation Deletion
@app.route('/donations/delete/<donation_id>', methods=['GET'])
def donation_delete(donation_id):
  donation_to_delete = donations.find_one({'_id': ObjectId(donation_id)})
  charity_to_update = charities.find_one({'_id': ObjectId(donation_to_delete['charity_id'])})
  charity_to_update['total_dontations'] = int(charity_to_update['total_dontations']) - 1
  charity_to_update['total_donated'] = int(charity_to_update['total_donated']) - int(donation_to_delete['amount'])
  print(type(charity_to_update['all_donations']))
  charity_to_update['all_donations'].remove(donation_to_delete)
  charities.update_one({'_id': ObjectId(request.form.get('charity'))}, {'$set': charity_to_update})
  donations.delete_one({'_id': ObjectId(donation_id)})
  all_donations = donations.find()
  return render_template('all_donations.html', all_donations=all_donations)

# Charity Deletion
@app.route('/charities/delete/<charity_id>', methods=['GET'])
def charity_delete(charity_id):
  print(charity_id)
  charity_to_delete = charities.find_one({'_id': ObjectId(charity_id)})
  list_of_donations = charity_to_delete['all_donations']
  for donation in list_of_donations:
    current_donation = donation.find_one({'_id': ObjectId(donation['_id'])})
    donations.delete_one({'_id': ObjectId(current_donation['_id'])})
  charities.delete_one({'_id': ObjectId(charity_id)})
  all_charities = charities.find()
  return render_template('all_charities.html', all_charities=all_charities)

# Grabs single donation
@app.route('/donations/<donation_id>', methods=['GET'])
def single_donation(donation_id):
  single_donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donation_single.html', single_donation=single_donation)

# Grabs single charity
@app.route('/charities/<charities_id>', methods=['GET'])
def single_charity(charities_id):
  single_charity = charities.find_one({'_id': ObjectId(charities_id)})
  return render_template('charity_single.html', single_charity=single_charity)
  
if __name__ == '__main__':
    app.run(debug=True)