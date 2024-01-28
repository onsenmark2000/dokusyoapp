import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry


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
        print("update")

    def delete(self):
        print("delete")


class SubWindow:
    def __init__(self, master, mode):
        # パラメタの受け取り
        self.master = master
        self.mode = mode

        # サブウィンドウの描画
        self.sub_window = tk.Toplevel()
        self.sub_window.title("Description")
        self.sub_window.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = MainWindow(master=root)
    mainWindow.mainloop()
