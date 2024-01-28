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

        # 縦スクロールバー
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        vscrollbar.grid(row=0, column=1, sticky=tk.NS)

        # 横スクロールバー
        hscrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=tk.EW)

        # スタイルの適用
        style = ttk.Style()
        style.theme_use("clam")

    def add(self):
        print("add")

    def update(self):
        print("update")

    def delete(self):
        print("delete")


if __name__ == "__main__":
    root = tk.Tk()
    mainWindow = MainWindow(master=root)
    mainWindow.mainloop()
