from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'property.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main page with buy form"""
    conn = get_db_connection()
    
    # Get all available records (where BuyerID is NULL - unsold properties)
    available_records = conn.execute('''
        SELECT r.RecordID, r.PropertyID, p.Address, p.AskingPrice, 
               'Available' as Status, r.BuyerID, r.SoldPrice
        FROM Record r
        JOIN Property p ON r.PropertyID = p.PropertyID
        WHERE r.BuyerID IS NULL
        ORDER BY r.RecordID
    ''').fetchall()
    
    # Get all sold records (where BuyerID is NOT NULL - sold properties)
    sold_records = conn.execute('''
        SELECT r.RecordID, r.PropertyID, p.Address, p.AskingPrice, 
               'Sold' as Status, r.BuyerID, r.SoldPrice
        FROM Record r
        JOIN Property p ON r.PropertyID = p.PropertyID
        WHERE r.BuyerID IS NOT NULL
        ORDER BY r.RecordID
    ''').fetchall()
    
    # Get all users for buyer dropdown
    users = conn.execute('''
        SELECT UserID, Name, Email
        FROM User
        ORDER BY UserID
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         available_records=available_records, 
                         sold_records=sold_records,
                         users=users)

@app.route('/buy', methods=['POST'])
def buy():
    """Handle the property purchase"""
    # Get form data
    record_id = request.form['recordID']
    buyer_id = request.form['buyerID']
    sold_price = request.form['soldPrice']
    sold_date = request.form['soldDate']
    
    conn = get_db_connection()
    
    # Update the record with buyer information
    conn.execute('''
        UPDATE Record 
        SET BuyerID = ?, SoldPrice = ?, SoldDate = ? 
        WHERE RecordID = ?
    ''', (buyer_id, sold_price, sold_date, record_id))
    
    # Update property status to sold
    conn.execute('''
        UPDATE Property 
        SET Status = 'True' 
        WHERE PropertyID = (
            SELECT PropertyID FROM Record WHERE RecordID = ?
        )
    ''', (record_id,))
    
    conn.commit()
    
    # Get buyer information
    buyer = conn.execute('''
        SELECT * FROM User WHERE UserID = ?
    ''', (buyer_id,)).fetchone()
    
    # Get property information with record details
    property_info = conn.execute('''
        SELECT r.RecordID, r.SellerID, r.PropertyID, r.DateListed, r.BuyerID, 
               r.SoldPrice, r.SoldDate, p.Address, p.Postal, p.TotalArea, 
               p.NoOfBedroom, p.NoOfToilet, p.AskingPrice, p.Status,
               u.Name as SellerName, u.Contact as SellerContact, u.Email as SellerEmail
        FROM Record r
        JOIN Property p ON r.PropertyID = p.PropertyID
        JOIN User u ON r.SellerID = u.UserID
        WHERE r.RecordID = ?
    ''', (record_id,)).fetchone()
    
    conn.close()
    
    return render_template('buy.html', buyer=buyer, property_info=property_info)

if __name__ == '__main__':
    app.run(debug=True)
