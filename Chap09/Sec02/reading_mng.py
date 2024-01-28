import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Select
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session

# プルダウンリストの中身
EVALUATION_VALUE = ("－", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★")
STATUS_VALUE = ("0:欲しい", "1:購入済、未読", "2:読書中", "3:読了", "4:途中放棄")


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Dokusyo App")

        # データベースとの接続
        self.db = DatabaseSession()

        # ウィンドウを閉じられたときに処理を実行
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        # 全ウィジェットの描画
        self.set_widget()

    def close_window(self):
        self.db.disconnect()
        self.master.destroy()

    def set_widget(self):
        # ==================== 1行目
        # アプリタイトル
        label_title = ttk.Label(self.master, text="読書管理アプリ", anchor=tk.CENTER)
        label_title.grid(row=0, column=0, columnspan=3,
                         ipadx=20, ipady=5, pady=10)

        # ==================== 2行目
        # 追加ボタン
        btn_add = ttk.Button(self.master, text="追加")
        btn_add.grid(row=1, column=0)
        btn_add.config(command=self.add)
        # 更新ボタン
        btn_update = ttk.Button(self.master, text="更新")
        btn_update.grid(row=1, column=1)
        btn_update.config(command=self.update)
        # 削除ボタン
        btn_delete = ttk.Button(self.master, text="削除")
        btn_delete.grid(row=1, column=2)
        btn_delete.config(command=self.delete)

        # ==================== 3行目
        # フレーム
        frame = ttk.Frame(self.master, width=700, height=200)
        frame.grid_propagate(False)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.grid(row=2, column=0, columnspan=3,
                   padx=5, pady=5, ipadx=5, ipady=5)

        # 表
        column = ("id", "name", "auther", "evaluation", "status",
                  "purchasedate", "startdate", "enddate", "pages", "url", "comment")
        self.table_books = ttk.Treeview(
            frame, columns=column, height=10, selectmode="browse", show="headings")
        self.table_books.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.table_books.bind("<<TreeviewSelect>>", self.select_record)

        # 列の設定
        self.table_books.column("id", anchor="center", width=30, stretch=False)
        self.table_books.column("name", anchor="w", width=300, stretch=False)
        self.table_books.column("auther", anchor="w", width=100, stretch=False)
        self.table_books.column("evaluation", anchor="center",
                                width=100, stretch=False)
        self.table_books.column("status", anchor="w", width=100, stretch=False)
        self.table_books.column("purchasedate", anchor="center",
                                width=80, stretch=False)
        self.table_books.column("startdate", anchor="center",
                                width=80, stretch=False)
        self.table_books.column(
            "enddate", anchor="center", width=80, stretch=False)
        self.table_books.column("pages", anchor="e", width=60, stretch=False)
        self.table_books.column("url", anchor="w", width=300, stretch=False)
        self.table_books.column("comment", anchor="w",
                                width=300, stretch=False)

        # ヘッダ行の設定
        self.table_books.heading("id", text="#", anchor="center")
        self.table_books.heading("name", text="書籍名", anchor="center")
        self.table_books.heading("auther", text="著者", anchor="center")
        self.table_books.heading("evaluation", text="評価", anchor="center")
        self.table_books.heading("status", text="ステータス", anchor="center")
        self.table_books.heading("purchasedate", text="購入日", anchor="center")
        self.table_books.heading("startdate", text="開始日", anchor="center")
        self.table_books.heading("enddate", text="読了日", anchor="center")
        self.table_books.heading("pages", text="ページ数", anchor="center")
        self.table_books.heading("url", text="URL", anchor="center")
        self.table_books.heading("comment", text="コメント", anchor="center")

        self.display_list()

        # 縦スクロールバー
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        vscrollbar.config(command=self.table_books.yview)
        vscrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.table_books.config(yscrollcommand=vscrollbar.set)

        # 横スクロールバー
        hscrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hscrollbar.config(command=self.table_books.xview)
        hscrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.table_books.config(xscrollcommand=hscrollbar.set)

        # スタイルの適用
        style = ttk.Style()
        style.theme_use("clam")

    def add(self):
        # サブウィンドウの表示
        sub_window = SubWindow(self, "add")

    def update(self):
        # リストが選択されている場合にサブウィンドウを表示
        if self.id != -1:
            sub_window = SubWindow(self, "update")

    def delete(self):
        # リストが選択されている場合に確認メッセージを表示
        if self.id != -1:
            ret = messagebox.askyesno("削除確認", "削除して良いですか？")
            if ret:
                # 「はい」が押されてたら削除
                self.book.delete(self.db, self.id)
                # リストを再描画
                self.display_list()

    def select_record(self, e):
        # 選択行の取得
        selected_id = self.table_books.focus()
        if selected_id != "":
            # 選択行のレコードの値を取得
            values = self.table_books.item(selected_id, "values")
            self.id = values[0]

    def display_list(self):
        # 既存レコードの削除
        for row in self.table_books.get_children():
            self.table_books.delete(row)

        # 検索
        books = Books.select_all(self.db)

        # レコードの追加
        for index, book in enumerate(books):
            self.table_books.insert(
                parent="", index="end", iid=index,
                values=(book.Books.id,
                        book.Books.name,
                        book.Books.auther,
                        book.Books.evaluation,
                        book.Books.status,
                        book.Books.purchase_date,
                        book.Books.start_date,
                        book.Books.end_date,
                        book.Books.pages,
                        book.Books.url,
                        book.Books.comment))

        # リスト選択のID値を初期化(未選択状態)
        self.id = -1

        # 再描画
        self.master.update()


class SubWindow:
    def __init__(self, master, mode):
        # パラメタの受け取り
        self.master = master
        self.mode = mode
        self.db = master.db
        self.id = master.id

        # サブウィンドウの描画
        self.sub_window = tk.Toplevel()
        self.sub_window.title("Description")
        self.sub_window.grab_set()

        if mode == "add":
            self.book_info = Book()
        else:
            self.book_info = self.book.select(self.db, self.id)

        # ウィンドウを閉じられたときに処理を実行
        self.sub_window.protocol("WM_DELETE_WINDOW", self.close_window)

        # 全ウィジェットの描画
        self.set_widget()

    def close_window(self):
        # リストの再描画
        self.master.display_list()

        # サブウィンドウを閉じる
        self.sub_window.destroy()

    def set_widget(self):
        # ==================== 1行目
        # 書籍名ラベル
        label_book_title = ttk.Label(self.sub_window, text="書籍名：")
        label_book_title.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        # 書籍名入力欄
        self.str_book_title = tk.StringVar()
        text_book_title = ttk.Entry(self.sub_window, width=50)
        text_book_title.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        text_book_title.config(textvariable=self.str_book_title)
        self.str_book_title.set(self.book_info.name)

        # 著者ラベル
        label_author = ttk.Label(self.sub_window, text="著者：")
        label_author.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)
        # 著者入力欄
        self.str_auther = tk.StringVar()
        text_author = ttk.Entry(self.sub_window, width=20)
        text_author.grid(row=0, column=4, columnspan=2, sticky=tk.W)
        text_author.config(textvariable=self.str_auther)
        self.str_auther.set(self.book_info.auther)

        # ==================== 2行目
        # 評価ラベル
        label_evaluation = ttk.Label(self.sub_window, text="評価：")
        label_evaluation.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        # 評価ドロップダウンリスト
        self.str_evaluation = tk.StringVar()
        combo_evaluation = ttk.Combobox(
            self.sub_window, values=EVALUATION_VALUE, state="readonly")
        combo_evaluation.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        combo_evaluation.config(textvariable=self.str_evaluation)
        combo_evaluation.set(self.book_info.evaluation)

        # ステータスラベル
        label_status = ttk.Label(self.sub_window, text="ステータス：")
        label_status.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)
        # ステータスドロップダウンリスト
        self.str_status = tk.StringVar()
        combo_status = ttk.Combobox(
            self.sub_window, values=STATUS_VALUE, state="readonly")
        combo_status.grid(row=1, column=4, columnspan=2, sticky=tk.W)
        combo_status.config(textvariable=self.str_status)
        combo_status.set(self.book_info.status)

        # ==================== 3行目
        # 購入日ラベル
        label_purchase_date = ttk.Label(self.sub_window, text="購入日：")
        label_purchase_date.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        # 購入日カレンダ
        self.str_purcahse_date = tk.StringVar()
        self.date_purchase = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_purchase.grid(row=2, column=1, sticky=tk.W)
        self.date_purchase.config(textvariable=self.str_purcahse_date)
        self.str_purcahse_date.set(self.book_info.purchase_date)
        # 購入日クリアボタン
        btn_clear_purchase = ttk.Button(self.sub_window, text="<-Clear")
        btn_clear_purchase.grid(row=2, column=2, sticky=tk.W)
        btn_clear_purchase.config(
            command=lambda: self.date_purchase.delete(0, "end"))

        # 開始日ラベル
        label_start_date = ttk.Label(self.sub_window, text="開始日：")
        label_start_date.grid(row=2, column=3, padx=5, sticky=tk.E)
        # 開始日カレンダ
        self.str_start_date = tk.StringVar()
        self.date_start = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_start.grid(row=2, column=4, sticky=tk.W)
        self.date_start.config(textvariable=self.str_start_date)
        self.str_start_date.set(self.book_info.start_date)
        # 開始日クリアボタン
        btn_clear_start = ttk.Button(self.sub_window, text="<-Clear")
        btn_clear_start.grid(row=2, column=5, sticky=tk.W)
        btn_clear_start.config(
            command=lambda: self.date_start.delete(0, "end"))

        # ==================== 4行目
        # 読了日ラベル
        label_finish_date = ttk.Label(self.sub_window, text="読了日：")
        label_finish_date.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        # 読了日カレンダ
        self.str_end_date = tk.StringVar()
        self.date_end = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_end.grid(row=3, column=1, sticky=tk.W)
        self.date_end.config(textvariable=self.str_end_date)
        self.str_end_date.set(self.book_info.end_date)
        # 読了日クリアボタン
        btn_clear_end = ttk.Button(self.sub_window, text="<-Clear")
        btn_clear_end.grid(row=3, column=2, sticky=tk.W)
        btn_clear_end.config(command=lambda: self.date_end.delete(0, "end"))

        # 総ページ数ラベル
        label_total_page = ttk.Label(self.sub_window, text="総ページ数：")
        label_total_page.grid(row=3, column=3, padx=5, sticky=tk.E)
        # 総ページ数入力欄
        self.str_pages = tk.StringVar()
        text_total_page = ttk.Entry(self.sub_window, width=10)
        text_total_page.grid(row=3, column=4, columnspan=2, sticky=tk.W)
        text_total_page.config(textvariable=self.str_pages)
        self.str_pages.set(self.book_info.pages)

        # ==================== 5行目
        # URLラベル
        label_url = ttk.Label(self.sub_window, text="URL：")
        label_url.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        # URL入力欄
        self.str_url = tk.StringVar()
        text_url = ttk.Entry(self.sub_window, width=100)
        text_url.grid(row=4, column=1, columnspan=5, sticky=tk.W)
        text_url.config(textvariable=self.str_url)
        self.str_url.set(self.book_info.url)

        # ==================== 6行目
        # コメントラベル
        label_comment = ttk.Label(self.sub_window, text="コメント：")
        label_comment.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        # フレーム
        frame = ttk.Frame(self.sub_window)
        frame.grid(row=5, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)

        # コメント入力欄
        self.text_comment = tk.Text(frame, width=100, height=5)
        self.text_comment.pack(side=tk.LEFT)
        self.text_comment.insert(tk.END, self.book_info.comment)

        # 縦スクロールバー
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        vscrollbar.pack(side=tk.LEFT, fill=tk.Y)
        vscrollbar.config(command=self.text_comment.yview)
        self.text_comment.config(yscrollcommand=vscrollbar.set)

        # ==================== 7行目
        if self.mode == "add":
            btn_add = ttk.Button(self.sub_window, text="追加")
            btn_add.grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)
            btn_add.config(command=self.add)
        else:
            btn_update = ttk.Button(self.sub_window, text="更新")
            btn_update.grid(row=6, column=4, padx=5, pady=5, sticky=tk.E)
            btn_update.config(command=self.update)

    def get_input_data(self):

        self.book_info.name = self.str_book_title.get()
        self.book_info.auther = self.str_auther.get()
        self.book_info.evaluation = self.str_evaluation.get()
        self.book_info.status = self.str_status.get()
        self.book_info.purchase_date = self.str_purcahse_date.get()
        self.book_info.start_date = self.str_start_date.get()
        self.book_info.end_date = self.str_end_date.get()
        self.book_info.pages = self.str_pages.get()
        self.book_info.url = self.str_url.get()
        self.book_info.comment = self.text_comment.get("1.0", "end")

    def add(self):
        # 入力値の取り出し
        self.get_input_data()

        # 簡単な入力チェック
        if len(self.book_info.name.strip()) == 0:
            messagebox.showerror("エラー", "書籍名が空白です。")
            return
        elif self.book_info.pages.isdigit() == False:
            messagebox.showerror("エラー", "ページ数が数字ではありません。")
            return

        # insert実行
        Books.insert(self.db, self.book_info)

        # リストの再描画
        self.master.display_list()

        # サブウィンドウを閉じる
        self.sub_window.destroy()

    def update(self):
        # 入力値の取り出し
        self.get_input_data()

        # 簡単な入力チェック
        if len(self.book_info.name.strip()) == 0:
            messagebox.showerror("エラー", "書籍名が空白です。")
            return
        elif self.book_info.pages.isdigit() == False:
            messagebox.showerror("エラー", "ページ数が数字ではありません。")
            return

        # update実行
        self.book_info.update(self.db)

        # リストの再描画
        self.master.display_list()

        # サブウィンドウを閉じる
        self.sub_window.destroy()


class Book:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.auther = ""
        self.evaluation = EVALUATION_VALUE[0]
        self.status = STATUS_VALUE[1]
        self.purchase_date = ""
        self.start_date = ""
        self.end_date = ""
        self.pages = 0
        self.url = ""
        self.comment = ""


class Base(DeclarativeBase):
    pass


class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    auther: Mapped[Optional[str]] = mapped_column(String)
    evaluation: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[Optional[str]] = mapped_column(String)
    purchase_date: Mapped[Optional[str]] = mapped_column(String)
    start_date: Mapped[Optional[str]] = mapped_column(String)
    end_date: Mapped[Optional[str]] = mapped_column(String)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String)
    comment: Mapped[Optional[str]] = mapped_column(String)

    @classmethod
    def select_all(cls, db):
        stmt = Select(cls).order_by(cls.id.desc())
        results = db.session.execute(stmt)

        return results

    @classmethod
    def select(cls, db, id):
        stmt = Select(cls).filter(cls.id == id)
        result = db.session.execute(stmt).fetchone()

        book = Book()
        book.id = result.Books.id
        book.name = result.Books.name
        book.auther = result.Books.auther
        book.evaluation = result.Books.evaluation
        book.status = result.Books.status
        book.purchase_date = result.Books.purchase_date
        book.start_date = result.Books.start_date
        book.end_date = result.Books.end_date
        book.pages = result.Books.pages
        book.url = result.Books.url
        book.comment = result.Books.comment

        return book

    @classmethod
    def insert(cls, db, book):
        add_book = cls(
            name=book.name,
            auther=book.auther,
            evaluation=book.evaluation,
            status=book.status,
            purchase_date=book.purchase_date,
            start_date=book.start_date,
            end_date=book.end_date,
            pages=book.pages,
            url=book.url,
            comment=book.comment
        )
        db.session.add(add_book)
        db.session.commit()

    @classmethod
    def update(cls, db, book):
        stmt = Select(cls).filter(cls.id == book.id)
        result = db.session.execute(stmt).fetchone()
        result.Books.name = book.name
        result.Books.auther = book.auther
        result.Books.evaluation = book.evaluation
        result.Books.status = book.status
        result.Books.purchase_date = book.purchase_date
        result.Books.start_date = book.start_date
        result.Books.end_date = book.end_date
        result.Books.pages = book.pages
        result.Books.url = book.url
        result.Books.comment = book.comment
        db.session.commit()

    @classmethod
    def delete(cls, db, id):
        del_book = db.session.get(cls, id)
        db.session.delete(del_book)
        db.session.commit()


class DatabaseSession:
    def __init__(self):
        engine = create_engine("sqlite:///db/Books.db")
        # セッションの開始
        self.session = Session(engine)
        print("connected")

    def disconnect(self):
        self.session.close()
        print("disconnected")


if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = MainWindow(master=root)
    mainWindow.mainloop()
