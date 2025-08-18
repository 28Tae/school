# 2.0 - SQLITE3 and Database Integration
--- 
<sup>[Return Home](../README.md)</sup>

## `2.1` - Relational Databases
A relational table is as follows:
- Values are _atomic_ (one key to one value correspondence)
- Column values are of the same kind
- Rows are unique
- The order of columns is insignificant
- Each column must have a unique name

A **primary key** is the main & unique identifier of rows in a table. It is typically an ID or the NRIC equivalent.

**Foreign keys** build r/s in tables by pointing to the primary key.

### **2.1.1** - Normalisation of Tables
We can break down data into proper relational tables of either one-one, one-many or many-many dependencies.

> In **1<sup>st</sup>** Normal Form, all columns become atomic, such that **information per column cannot be broken down further.**
- If a column such as "CCAInfo" contains value "CCA-Teacher-ID" (with multiple values embedded), then in 1NF, split into columns "CCA", "CCA-Teacher", "CCA-ID"

> In **2<sup>nd</sup>** Normal Form, **every non-key must be fully dependent on the primary key**. This means if the information doesn't fully rely on the PK, it probably belongs in another table with an established relationship.
- This can look like Student(ID, Name, Gender, Class, ClassTeacher), StudentCCA(ID, CCAName), CCAInfo(CCAName, CCA-Teacher, CCA-Times...)

> In **3<sup>rd</sup>** Normal Form, there should be **no transitive dependencies**, i.e. no non-keys are reliant on other non-keys in any way.
- Student(ID, Name, Gender, Class, ClassTeacher) is not in 3NF since ClassTeacher is dependent on Class
- Hence we can break down to Student(ID, Name, Gender, Class) and Class(Class, ClassTeacher)
<hr>

## `2.2` - Using SQLITE3

SQLITE3 operates on `.db` files using SQL tables and commands.
| Datatype | ? |
| --- | --- |
| INTEGER | Signed int value | 
| REAL | Floating point with decimal pt |
| TEXT | String |

To replace **booleans**, use INTEGER and restrain the values such that `CHECK(bool in (0, 1))`, where 0 is False and 1 is True (just for convention sake).<br>You don't need to know BLOB (Binary Large Object) or Numerics for datatypes.

### **2.2.1** - CRUD

| CRUD | SQLITE3 Statements |
| --- | --- |
| Create (Tables) | `CREATE` |
| Read | `SELECT ... FROM ...` |
| Update | `UPDATE ... SET ...` or `INSERT INTO ... VALUES ...` |
| Delete | `DELETE FROM ...` |


```python
-- Creating
CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price INTEGER DEFAULT 0 CHECK (price >= 0),
    sold INTEGER DEFAULT 0 CHECK (sold IN (0, 1)),
    name TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES pet_audits(id)
);
```


```python
-- Select
SELECT col1, col2 FROM t1 [WHERE condition] [ORDER by col DESC];

SELECT Count(*) AS "Pets", parentName as "Parent Name" FROM pets INNER JOIN pet_family ON pets.id = pet_family.id GROUP BY parentName WHERE year < 2020;
```


```python
-- Inserting
INSERT INTO t1 (col1, col2) VALUES (v1, v2);
```


```python
-- Updating
UPDATE t1 SET col1 = v1, col2 = v2, col3 = v3 [WHERE condition];
UPDATE enrolment SET "count" = "count" + 5 WHERE condition; --Increment the count attribute by 5
```


```python
-- Deleting
DELETE FROM t1 WHERE condition;
```

### **2.2.2** - CRUD Functions
> To concantenate strings, do `s1||s2`

| Function | ? | Eg |
| --- | --- | --- |
| __**`COUNT()`**__ | Count rows | `SELECT COUNT(*) FROM table` |
| __**`MAX()/MIN()`**__ | Max/min of | ... |
| __**`SUM()`**__ | Returns a sum | ... |
| __**`AVG()`**__ | Averages | ... |
| `GROUP BY col` | Aggregate by group | `SELECT company FROM sales GROUP BY agent` |
| `LIMIT n` | Limits no. of rows | `SELECT * FROM Books LIMIT 5` |
| __**`DISTINCT col`**__ | Unique | `SELECT DISTINCT PublisherID AS UniquePublishers FROM Book` |
| __**`INNER JOIN`**__ | Join tables | `SELECT ... FROM t1 INNER JOIN t2 ON t1.col=t2.col` |

### **2.2.3** - SQLITE3 in Python
Check the implementation below, including the importing of `sqlite3` library.<br>
- `conn = sqlite3.connect(DB_FILE)` establishes a SQL connection to run statements
- `cursor = conn.execute(query, tup)` to execute a command. The cursor variable is only necessary for SELECT statements
- In SELECT statements, you do `data = cursor.fetchall()` ready to process
    - This will generate a **list of tuples**, where **each tuple is a row of data**
- In other CRUD statements, `conn.commit()` and `conn.rollback()` commits/undoes data edits respectively.
- Remember to close connections (and cursors if any) via `conn.close()`


```python
import sqlite3
DB_FILE = "your_file.db"
some_tuple = ('', '')


def select_query(query, tup=None):
    # Use question marks
    # connect, execute("SELECT ... WHERE val = ?", tuple)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(query, tup) if tup else conn.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def commit_query(query, tup):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(query, tup)
    conn.commit()
    conn.close()


select_query("SELECT * FROM books WHERE PublisherID = ? LIMIT ?", some_tuple)
commit_query("INSERT INTO books (c1, c2) VALUES (?, ?)", some_tuple)
commit_query('UPDATE books SET "age" = "age" + 1 WHERE id = ?', some_tuple)
```

Take note, when dealing with **custom inputs**, do not use f-strings or concatenation, but use `?` **question mark placeholders**, with a supplementary tuple of args:<br>
❌ `conn.execute(f"SELECT ... WHERE id = {id}")` <br>
✅ `conn.execute(f"SELECT ... WHERE id = ?", (id, ))`
<hr>

## **`2.3` - CSV Reading**
To read a CSV file and populate it into a SQLITE3 .db file via Python,
1. Open each file using `with open(file_path, mode)`<br>
2. Use a **csv reader** by `csv.reader()`<br>
3. Store **header row** by `next(reader)`<br>
4. Generate `(?, ?...)` placeholder tuple<br>
5. Tuple row & header into query, and execute in for loop of reader


```python
import csv, sqlite3
TABLE_FILES: dict = {
    "User": "users.csv",
    "Job": "jobs.csv",
    "WorkerJob": "workerjobs.csv",
    "ContractRecord": "records.csv",
}
DB_FILE = "your_file.db"

def csv_read():
    for table in TABLE_FILES:
        conn = sqlite3.connect(DB_FILE)
        with open("/data_files/{table}") as f:

            # Generate reader & get header
            read = csv.reader(f)
            header = next(read)
            placeholders = ", ".join(["?" for _ in header])

            # Dump values into placeholders per row
            for row in read:
                conn.execute(
                    f"INSERT INTO {table} ({tuple(header)}) VALUES ({placeholders})",
                    tuple(row)
                )

        # Remember to commit and close
        conn.commit()
        conn.close()
```
