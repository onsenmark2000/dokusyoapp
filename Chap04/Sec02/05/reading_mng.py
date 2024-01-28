import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# プルダウンリストの中身
EVALUATION_VALUE = ("－", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★")
STATUS_VALUE = ("0:欲しい", "1:購入済、未読", "2:読書中", "3:読了", "4:途中放棄")


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Dokusyo App")

        # 全ウィジェットの描画
        self.set_widget()

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

        # ダミーデータ
        self.table_books.insert(parent="", index="end", iid=0, values=(
            0, "あいうえお", "かきくけこ", "－", "", "2023/12/01", "2023/12/02", "2023/12/25",
            999, "http://hoge.hoge.co.jp/あいうえお", "コメント"))
        self.id = -1

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
            print(f"update id={self.id}")
            sub_window = SubWindow(self, "update")

    def delete(self):
        # リストが選択されている場合に確認メッセージを表示
        if self.id != -1:
            ret = messagebox.askyesno("削除確認", "削除して良いですか？")
            if ret:
                # 「はい」が押されてたら削除
                print(f"delete id={self.id}")

    def select_record(self, e):
        # 選択行の取得
        selected_id = self.table_books.focus()
        if selected_id != "":
            # 選択行のレコードの値を取得
            values = self.table_books.item(selected_id, "values")
            self.id = values[0]


class SubWindow:
    def __init__(self, master, mode):
        # パラメタの受け取り
        self.master = master
        self.mode = mode

        # サブウィンドウの描画
        self.sub_window = tk.Toplevel()
        self.sub_window.title("Description")
        self.sub_window.grab_set()

        # 全ウィジェットの描画
        self.set_widget()

    def set_widget(self):
        # ==================== 1行目
        # 書籍名ラベル
        label_book_title = ttk.Label(self.sub_window, text="書籍名：")
        label_book_title.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        # 書籍名入力欄
        text_book_title = ttk.Entry(self.sub_window, width=50)
        text_book_title.grid(row=0, column=1, columnspan=2, sticky=tk.W)

        # 著者ラベル
        label_author = ttk.Label(self.sub_window, text="著者：")
        label_author.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)
        # 著者入力欄
        text_author = ttk.Entry(self.sub_window, width=20)
        text_author.grid(row=0, column=4, columnspan=2, sticky=tk.W)

        # ==================== 2行目
        # 評価ラベル
        label_evaluation = ttk.Label(self.sub_window, text="評価：")
        label_evaluation.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        # 評価ドロップダウンリスト
        combo_evaluation = ttk.Combobox(
            self.sub_window, values=EVALUATION_VALUE, state="readonly")
        combo_evaluation.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        # ステータスラベル
        label_status = ttk.Label(self.sub_window, text="ステータス：")
        label_status.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)
        # ステータスドロップダウンリスト
        combo_status = ttk.Combobox(
            self.sub_window, values=STATUS_VALUE, state="readonly")
        combo_status.grid(row=1, column=4, columnspan=2, sticky=tk.W)

        # ==================== 3行目
        # 購入日ラベル
        label_purchase_date = ttk.Label(self.sub_window, text="購入日：")
        label_purchase_date.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        # 購入日カレンダ
        self.date_purchase = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_purchase.grid(row=2, column=1, sticky=tk.W)
        # 購入日クリアボタン
        btn_clear_purchase = ttk.Button(self.sub_window, text="<-Clear")
        btn_clear_purchase.grid(row=2, column=2, sticky=tk.W)

        # 開始日ラベル
        label_start_date = ttk.Label(self.sub_window, text="開始日：")
        label_start_date.grid(row=2, column=3, padx=5, sticky=tk.E)
        # 開始日カレンダ
        self.date_start = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_start.grid(row=2, column=4, sticky=tk.W)
        # 開始日クリアボタン
        btn_clear_start = ttk.Button(self.sub_window, text="<-Clear")
        btn_clear_start.grid(row=2, column=5, sticky=tk.W)

        # ==================== 4行目
        # 読了日ラベル
        label_finish_date = ttk.Label(self.sub_window, text="読了日：")
        label_finish_date.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        # 読了日カレンダ
        self.date_end = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_end.grid(row=3, column=1, sticky=tk.W)
        # 読了日クリアボタン
        btn_clear_end = ttk.Button(self.sub_window, text="<-Clear")
        btn_clear_end.grid(row=3, column=2, sticky=tk.W)

        # 総ページ数ラベル
        label_total_page = ttk.Label(self.sub_window, text="総ページ数：")
        label_total_page.grid(row=3, column=3, padx=5, sticky=tk.E)
        # 総ページ数入力欄
        text_total_page = ttk.Entry(self.sub_window, width=10)
        text_total_page.grid(row=3, column=4, columnspan=2, sticky=tk.W)

        # ==================== 5行目
        # URLラベル
        label_url = ttk.Label(self.sub_window, text="URL：")
        label_url.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        # URL入力欄
        text_url = ttk.Entry(self.sub_window, width=100)
        text_url.grid(row=4, column=1, columnspan=5, sticky=tk.W)

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

        # 縦スクロールバー
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        vscrollbar.pack(side=tk.LEFT, fill=tk.Y)
        vscrollbar.config(command=self.text_comment.yview)
        self.text_comment.config(yscrollcommand=vscrollbar.set)

        # ==================== 7行目
        if self.mode == "add":
            btn_add = ttk.Button(self.sub_window, text="追加")
            btn_add.grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)
        else:
            btn_update = ttk.Button(self.sub_window, text="更新")
            btn_update.grid(row=6, column=4, padx=5, pady=5, sticky=tk.E)


if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = MainWindow(master=root)
    mainWindow.mainloop()
