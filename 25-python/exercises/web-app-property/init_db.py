import sqlite3
import csv
import os

def initialize_database():
    """Initialize the property database with tables and data"""
    
    # Connect to database
    conn = sqlite3.connect('property.db')
    
    # Create tables
    QUERIES = [
        """CREATE TABLE IF NOT EXISTS "User" (
            "UserID"    TEXT NOT NULL UNIQUE,
            "Name"      TEXT NOT NULL UNIQUE,
            "Contact"   TEXT NOT NULL,
            "Email"     TEXT NOT NULL,
            PRIMARY KEY("UserID")
        )""",
        """CREATE TABLE IF NOT EXISTS "Property" (
            "PropertyID"    TEXT NOT NULL UNIQUE,
            "Address"       TEXT NOT NULL,
            "Postal"        INTEGER NOT NULL,
            "TotalArea"     INTEGER NOT NULL,
            "NoOfBedroom"   INTEGER NOT NULL,
            "NoOfToilet"    INTEGER NOT NULL,
            "AskingPrice"   REAL NOT NULL,
            "Status"        TEXT NOT NULL DEFAULT 'False' CHECK("Status" IN ('True', 'False')),
            PRIMARY KEY("PropertyID")
        )""",
        """CREATE TABLE IF NOT EXISTS "Record" (
            "RecordID"      INTEGER NOT NULL UNIQUE,
            "SellerID"      TEXT NOT NULL,
            "PropertyID"    TEXT NOT NULL,
            "DateListed"    INTEGER NOT NULL,
            "BuyerID"       TEXT,
            "SoldPrice"     REAL,
            "SoldDate"      INTEGER,
            PRIMARY KEY("RecordID" AUTOINCREMENT),
            FOREIGN KEY("BuyerID") REFERENCES "User"("UserID"),
            FOREIGN KEY("PropertyID") REFERENCES "Property"("PropertyID"),
            FOREIGN KEY("SellerID") REFERENCES "User"("UserID")
        )"""
    ]
    
    for query in QUERIES:
        conn.execute(query)
    
    # Clear existing data (for clean initialization)
    conn.execute("DELETE FROM Record")
    conn.execute("DELETE FROM Property") 
    conn.execute("DELETE FROM User")
    
    # Insert sample users data
    users_data = [
        ("User001", "Christiana Castaneda", "9002601", "christiana_castaneda@gmail.com"),
        ("User002", "Matas Mcgowan", "8296800", "matas_mcgowan@outlook.com"),
        ("User003", "Evie-Grace Gale", "8333617", "evie-grace_gale@yahoo.com.sg"),
        ("User004", "Terence Knight", "8157192", "terence_knight@gmail.com"),
        ("User005", "Phyllis Burt", "9585675", "phyllis_burt@gmail.com"),
        ("User006", "Aiza Crossley", "9325634", "aiza_crossley@outlook.com"),
        ("User007", "Huxley Chang", "8971337", "huxley_chang@gmail.com"),
        ("User008", "Sanjay Reeves", "8805514", "sanjay_reeves@outlook.com"),
        ("User009", "Lillie-Rose Blackwell", "9990552", "lillie-rose_blackwell@gmail.com"),
        ("User010", "Harriett Robin", "9923961", "harriett_robin@gmail.com"),
        ("User011", "Shahid Trevino", "9073824", "shahid_trevino@yahoo.com.sg"),
        ("User012", "Ayrton Summers", "9496613", "ayrton_summers@outlook.com"),
        ("User013", "Jonas Lott", "8934935", "jonas_lott@gmail.com"),
        ("User014", "Lianne Rosa", "9565994", "lianne_rosa@outlook.com"),
        ("User015", "Kaja Holding", "8200827", "kaja_holding@yahoo.com.sg"),
        ("User016", "Hilda Forrest", "8471132", "hilda_forrest@gmail.com"),
        ("User017", "Augustus Orr", "8352059", "augustus_orr@yahoo.com.sg"),
        ("User018", "Nabila Odling", "9418684", "nabila_odling@yahoo.com.sg"),
        ("User019", "Freja Rowley", "9622055", "freja_rowley@gmail.com"),
        ("User020", "Cairon Alvarado", "9436148", "cairon_alvarado@gmail.com")
    ]
    
    # Insert properties data
    properties_data = [
        ("Property001", "583 Orchard Road", 238884, 75, 2, 1, 1081000.00, "False"),
        ("Property002", "141 Market Street", 48944, 90, 2, 2, 919000.00, "False"),
        ("Property003", "27 Wilby Road", 276302, 110, 3, 3, 703000.00, "False"),
        ("Property004", "9 penang road", 238459, 100, 3, 3, 1046000.00, "False"),
        ("Property005", "194 Pandan Loop", 128383, 94, 3, 2, 756000.00, "False"),
        ("Property006", "514 chai chee lane", 469029, 108, 3, 3, 530000.00, "False"),
        ("Property007", "77 Commonwealth Drive", 140077, 106, 3, 3, 749000.00, "False"),
        ("Property008", "290 Orchard Road", 238859, 99, 2, 2, 871000.00, "False"),
        ("Property009", "238 Thomson Road", 307684, 124, 4, 3, 935000.00, "False"),
        ("Property010", "16a Bali Lane", 189852, 60, 1, 1, 1292000.00, "False"),
        ("Property011", "85 Science Park Drive", 118259, 96, 3, 2, 636000.00, "False")
    ]
    
    # Insert records data
    records_data = [
        (1, "User017", "Property007", 20200103, None, None, None),
        (2, "User002", "Property003", 20200124, "User010", 692000.00, 20200605),
        (3, "User004", "Property005", 20200201, None, None, None),
        (4, "User014", "Property010", 20200202, None, None, None),
        (5, "User015", "Property004", 20200203, "User012", 1035000.00, 20200620),
        (6, "User013", "Property011", 20200225, None, None, None),
        (7, "User016", "Property009", 20200229, None, None, None),
        (8, "User008", "Property001", 20200305, None, None, None),
        (9, "User009", "Property008", 20200318, None, None, None),
        (10, "User005", "Property002", 20200320, "User001", 910000.00, 20200510),
        (11, "User018", "Property006", 20200401, None, None, None)
    ]
    
    # Insert data
    conn.executemany("INSERT INTO User VALUES (?, ?, ?, ?)", users_data)
    conn.executemany("INSERT INTO Property VALUES (?, ?, ?, ?, ?, ?, ?, ?)", properties_data)
    conn.executemany("INSERT INTO Record VALUES (?, ?, ?, ?, ?, ?, ?)", records_data)
    
    # Update property status for already sold properties
    conn.execute("UPDATE Property SET Status = 'True' WHERE PropertyID IN ('Property002', 'Property003', 'Property004')")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
