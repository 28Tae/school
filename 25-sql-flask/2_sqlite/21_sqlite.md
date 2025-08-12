# SQLITE3 with Python
--- 
## **`2.1` - CRUD Syntax**
SELECT, INSERT INTO, UPDATE (increment), DELETE FROM, DROP TABLE


```python
-- Creating
CREATE TABLE blackies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price INTEGER DEFAULT 0 CHECK (price >= 0),
    sold INTEGER DEFAULT 0 CHECK (sold IN (0, 1)),
    name TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES blackie_audits(id)
);

-- Select
SELECT col1, col2 FROM t1 [WHERE condition] [ORDER by col DESC];

-- Inserting
INSERT INTO t1 (col1, col2) VALUES (v1, v2);

-- Updating
UPDATE t1 SET col1 = v1, col2 = v2, col3 = v3 [WHERE condition];
UPDATE enrolment SET "count" = "count" + 5 WHERE condition; --Increment by 5

-- Deleting
DELETE FROM t1 WHERE condition;
```

### 2.1.1 - Functions
> To concantenate strings, do `s1||s2`


| f(x) | Use | Eg |
| --- | --- | --- |
| __**`COUNT()`**__ | Count rows | `SELECT COUNT(*) FROM table` |
| __**`MAX()/MIN()`**__ | Max/min of | ... |
| __**`SUM()`**__ | Returns a sum | ... |
| __**`AVG()`**__ | Averages | ... |
| `GROUP BY col` | Aggregate by group | `SELECT company FROM sales GROUP BY agent` |
| `LIMIT n` | Limits no. of rows | `SELECT * FROM Books LIMIT 5` |
| __**`DISTINCT col`**__ | Unique | `SELECT DISTINCT PublisherID AS UniquePublishers FROM Book` |
| __**`INNER JOIN`**__ | Join tables | `SELECT ... FROM t1 INNER JOIN t2 ON t1.col=t2.col` |

### 2.1.2 - SQLITE3 in Python


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

## **`2.2` - CSV Reading**
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
