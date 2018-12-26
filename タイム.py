import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import random
import sys
from tkinter import messagebox
import datetime
import csv
import time


class App(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.pack()

        self.st = 0  # スタート位置
        self.go = 15  # ゴール位置
        self.end = 10  # 何問で終了するか
        self.i = 0  # 間違えた回数のカウント
        self.k = 0  # 問題数

        # セーブ用データ
        self.times = [0] * 100  # 出題問題数
        self.miss = [0] * 100  # 間違えた問題

        self.chance = 2  # 答えられる回数

        # 上の句、下の句を初期化
        self.up = None
        self.under = None

        # データの読み込み
        self.df = pd.read_csv("uta.csv")
        self.uta = [(up, under) for up, under in zip(self.df["上"], self.df["下"])]

        # 問題番号を初期化
        self.o = None

        self.start = None  # スタート時間

        # 問題のラベル
        self.var = tk.StringVar()  # ラベル更新用
        self.var.set("Enterで")

        # ラベルの表示
        self.label = tk.Label(textvariable=self.var, font=("", 50, "bold"))
        self.label.place(x=50, y=70)

        # n問目の表示
        self.n = tk.StringVar()
        self.n.set("1問目")
        self.n_lr = tk.Label(textvariable=self.n, font=("", 20, "bold"))
        self.n_lr.place(x=0, y=0)

        # 正解のラベル
        self.correct = tk.StringVar()
        self.correct.set("")
        self.co_label = tk.Label(textvariable=self.correct, font=("", 80, "bold"), fg="#FF0000")
        self.co_label.place(x=100, y=350)

        # 不正解のラベル
        self.incorrect = tk.StringVar()
        self.incorrect.set("スタート")
        self.inc_label = tk.Label(textvariable=self.incorrect, font=("", 80, "bold"), fg="#0000FF")
        self.inc_label.place(x=50, y=350)

        # 前の問題の答えのラベル
        self.num = tk.StringVar()
        self.num.set("")
        self.num_label = tk.Label(textvariable=self.num, font=("", 15))
        self.num_label.place(x=50, y=300)

        # 入力ボタン
        self.btn = tk.Button(text="入力(Enter)", command=self.decision, width=50)
        self.btn.place(x=80, y=250)

        # 終了ボタン
        self.fin_btn = tk.Button(text="終了", command=self.fin)
        self.fin_btn.place(x=450, y=450)

        # 入力ボックス
        self.box = ttk.Entry(width=50)
        self.box.place(x=80, y=200)
        self.box.bind("<Return>", self.decision)
        self.box.bind("<Escape>", self.fin)

        # 1問目を表示
        # self.question()

    def fin(self, event=0):
        """終了"""
        goal = time.time()
        # 本当に終了するか確認
        ret = messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
        if ret:
            # 画面とプログラムの終了
            elapsed_time = goal - start
            print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
            self.quit()
            sys.exit()

    def timeout(self):
        goal = time.time()
        elapsed_time = goal - self.start
        goes = str(self.st) + "番から" + str(self.go) + "番まで, " + str(self.end) + "問正解で終了."
        res = messagebox.showinfo('結果', str(elapsed_time) + "秒でした.\n" + goes)
        if res:
            save_yn = messagebox.askyesno("Save", "セーブしますか？")
            if save_yn:
                self.save(elapsed_time)
                print("セーブ")

    def save(self, tm):
        """問題数、間違えた回数をcsvファイルに保存"""
        # 日付を取得
        date = datetime.date.today()
        date.isoformat()

        # 日付を追加
        save_data = [date, tm, self.end, self.st, self.go]

        # 間違えた回数を保存
        with open('Time_save.csv', 'a', newline='') as f:
            writer = csv.writer(f)  # 行末は改行
            writer.writerow(save_data)

    def question(self):
        """問題作成"""
        if sum(self.times) - sum(self.miss) == self.end:  # 正解数が10(通常)になったら…
            self.timeout()
        else:
            self.k += 1
            # 前の問題の答え表示
            set_label = str(self.up) + "の答えは" + str(self.under) + "でした。"

            # 問題数、（正解数）/（解いた問題数）
            num_label = str(self.k) + "問目   " + str(sum(self.times) - sum(self.miss)) + "/" + str(sum(self.times))

            self.num.set(set_label)
            self.n.set(num_label)
            self.i = 0  # 答える回数を初期化
            self.o = random.randint(self.st, self.go)  # 問題番号生成

            self.up, self.under = self.uta[self.o]  # 上の句と下の句
            self.var.set(self.up)  # 問題の上の句のラベルに更新

            self.times[self.o] += 1  # 問題数をカウント

    def over(self):
        """回数オーバーか判定"""
        if self.i == self.chance:
            print("回数オーバーです")
            self.miss[self.o] += 1
            return True
        else:
            return False

    def decision(self, event=0):  # eventは使わない
        """正解か不正解か判定"""
        if self.k == 0:
            self.incorrect.set("")
            self.start = time.time()
            self.question()
        else:
            ans = self.box.get()
            self.box.delete(0, tk.END)

            self.i += 1

            # 正誤判定
            if ans == self.under:
                self.incorrect.set("")
                self.correct.set("正解!!!")
                self.question()
            else:
                self.correct.set("")
                self.incorrect.set("不正解…")

            if self.over():  # 回数オーバーしているか判定
                self.question()


if __name__ == "__main__":
    start = time.time()
    app = tk.Tk()
    app.geometry("500x500")
    app.title("チズチズの百人一首トレーニング")
    frame = App(app)  # クラス呼び出し
    app.mainloop()
