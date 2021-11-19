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
def index():
  all_donations = donations.find()
  all_charities = charities.find()
  return render_template('home_page.html', donations=all_donations, charities=all_charities)

# Donations Page (This will show specifically donations in a listed format with key information)
@app.route('/donations', methods=['GET'])
def donations_show_all():
  all_donations = donations.find()
  return render_template('donations_page.html', donations=all_donations)

# Donations Page (This will show specifically donations in a listed format with key information)
@app.route('/donations/<donation_id>', methods=['GET'])
def donations_single(donation_id):
  new_donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donations_single_page.html', new_donation=new_donation)

# Donations Page (Create and submit a donation form)
@app.route('/donations', methods=['POST'])
def donations_create():
  new_donation = {
    'charity': request.form.get('title'),
    'amount': request.form.get('amount'),
    'notes': request.form.get('notes'),
    'user_id': request.form.get('user_id'),
    'created_at': datetime.now()
  }
  donation_new = donations.insert_one(new_donation)
  all_donations = donations.find()
  return redirect(url_for('donations_page.html', all_donations=all_donations))

# Donations Page (Edit donation)
@app.route('/donations/<donation_id>', methods=['POST'])
def donations_single(donation_id):
  updated_donation = {
    'charity': request.form.get('title'),
    'amount': request.form.get('amount'),
    'notes': request.form.get('notes'),
    'user_id': request.form.get('user_id'),
    'created_at': datetime.now()
  }
  donations.update_one({'_id': ObjectId(donation_id)}, {'$set': updated_donation})
  all_donations = donations.find()
  return render_template('donations_single_page.html', all_donations=all_donations)

# Donation Deletion
@app.route('/donations/<donation_id>', methods=['DELETE'])
def donation_delete(donation_id):
  donations.delete_one({'_id': ObjectId(donation_id)})
  all_donations = donations.find()
  return render_template('donations_single_page.html', all_donations=all_donations)

# # Get All Charities
# @app.route('/charities', methods=['GET'])
# def charity_show_all():
#   all_charities = charities.find()
#   return render_template('charities_page.html', all_charities=all_charities)

# # Get Single Charities
# @app.route('/charities/<charity_id>', methods=['GET'])
# def charity_single(charity_id):
#   single_charity = charities.find_one({'_id': ObjectId(charity_id)})
#   return render_template('charities_single_page.html', single_charity=single_charity)

# # Update Charities
# @app.route('/charities/<charity_id>', methods=['POST'])
# def charity_sinsgle(charity_id):
#   single_charity = charities.find_one({'_id': ObjectId(charity_id)})
#   return render_template('charities_single_page.html', single_charity=single_charity)

if __name__ == '__main__':
    app.run(debug=True)