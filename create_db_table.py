import sqlite3

conn = sqlite3.connect("./DB/Books.db")
cur = conn.cursor()

cur.execute("create table books("
            "id integer primary key autoincrement,"
            "name text,"
            "auther text,"
            "evaluation text,"
            "status text,"
            "purchase_date text,"
            "start_date text,"
            "end_date text, "
            "pages integer,"
            "url text,"
            "comment text)")

cur.execute("insert into books ("
            "name,"
            "auther,"
            "evaluation,"
            "status,"
            "purchase_date,"
            "start_date,"
            "end_date,"
            "pages,"
            "url,"
            "comment"
            ") values ("
            "'Pythonでつくるデスクトップアプリケーション',"
            "'岩田秀樹',"
            "'★★★☆☆',"
            "'3:読了',"
            "'2024/01/02',"
            "'2024/01/03',"
            "'2024/01/04',"
            "146,"
            "'https://www.amazon.co.jp/dp/B0CRQHTHM1',"
            "'コメントお願いします')"
            )

conn.commit()
conn.close()
