# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 00:16:41 2022

@author: root
"""

import tkinter as tk
from tkinter import *
import random
from tkinter import messagebox

window = tk.Tk()
window.geometry("350x500")  # Size of the window
window.title("max_it_to_win_it")  # Adding a title

import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os

vis = np.zeros((105, 105), bool)
dp = np.zeros((105, 105), int)
prefix = np.zeros((105, 105), bool)
path = np.zeros((105, 105), int)
test = []

totalH = ""
numH = 0
totalC = ""
numC = 0
isAI = True

# numbers = [-23,56,1,-78,8,-9,11]
lastPressed = 0
lastSelected = -1

buttons = []  # to store button references

window.config(bg="black")

resultH = tk.Frame(window)

resultC = tk.Frame(window)

finalC = StringVar()
finalH = StringVar()
label = tk.Label(window, text="Max it to win it", fon=("Arial Bold", 28), bg="black", fg="#99ffff")

label.pack(side=tk.TOP, pady=20)
captionH = Label(window, text="HUMAN SCORE:", fon=("Arial Bold", 10), bg="black", fg="white").place(x=220, y=230)
captionC = Label(window, text="AI SCORE:", fon=("Arial Bold", 10), bg="black", fg="white").place(x=5, y=230)
scoreH = Entry(window, textvariable=finalH).place(x=220, y=250)
scoreC = Entry(window, textvariable=finalC).place(x=5, y=250)
AIW = Label(window, text="AI wins!!!", fon=("Arial Bold", 14), bg="black", fg="white")
HumanW = Label(window, text="Human wins!!!", fon=("Arial Bold", 14), bg="black", fg="white")

# game_over = Entry(window,textvariable=go).place(x=-0,y=350)

hi = 0
lo = 0


# valid = []


# ------------------ after a number is selected ---------------------

def show_press(press, lastPressed):
    global numH, numC, totalH, totalC, lo, hi, lastSelected, test

    # lo = valid[0]
    # hi = valid[1]
    # lastSelected = -1

    # ---------------------------------- IF IT IS HUMAN ---------------------------------

    # print(local_isAI)

    print("it is human\'s move")
    for i in range(len(buttons)):
        if i == lastPressed:
            # print(lastPressed)

            print("\nthe button now pressed is {} and valid are {}, {}.\nthe last selected was {}".format(i, lo, hi,
                                                                                                          lastSelected))

            if ((lastSelected == -1 and (lo == i or hi == i)) or (lo == i and lastSelected == i - 1) or (
                    hi == i and lastSelected == i + 1)):

                if lo == i:
                    lo = i + 1
                    print("lo being updated")
                    # valid[0] = i+1
                elif hi == i:
                    hi = i - 1
                    print("hi being updated")
                    # valid[1] = i-1
                lastSelected = i

                numH = numH + int(test[i])
                test[i] = 0
                buttons[i].config(bg="#80f6c3")

            else:
                messagebox.showerror("showerror", "Can't select the number")

        i = i + 1

    # print("in show press: hi = {}, lo = {} ".format(hi, lo))


# ----------------------- after pressing the pass buttton ----------------------

def passval(btn):
    global numH, numC, totalH, totalC, isAI, lastSelected, valid, hi, lo

    # if( not(local_isAI) ):
    totalH = str(numH)
    finalH.set(totalH)
    '''else:
        totalC=str(numC)
        finalC.set(totalC)
    isAI = not(isAI)'''

    print("after pass: hi = {}, lo = {}".format(hi, lo))

    lastSelected = -1

    minmax(lo, hi)

    if (lo < hi):

        if (prefix[lo][hi]):

            for i in range(lo, lo + path[lo][hi]):
                # comp_val+=numbers[i]
                numC = numC + int(test[i])
                test[i] = 0
                buttons[i].config(bg="#c2f1ff")

            lo += path[lo][hi]


        else:

            for i in range(hi, hi - path[lo][hi], -1):
                # comp_val+=numbers[i]
                numC = numC + int(test[i])
                test[i] = 0
                buttons[i].config(bg="#c2f1ff")

            hi -= path[lo][hi]
    else:
        print("shesh")
        if numC > numH:
            AIW.pack(pady=20)
        elif numH > numC:
            HumanW.pack(pady=20)
        else:
            print("draw")

    # i = i+1

    print("After AI move hi = {}, lo = {}".format(hi, lo))

    totalC = str(numC)
    finalC.set(totalC)
    totalH = str(numH)
    finalH.set(totalH)

    # valid[0] = lo
    # valid[1] = hi
    # isAI = not(isAI)


# --------------------------------------------minimax algo-----------------------------------------


def minmax(l, r):
    if l > r:
        return 0

    if vis[l][r]:
        return dp[l][r]

    x = -99999999
    a = 0

    for i in range(l, r + 1):

        a += test[i]
        y = a - minmax(i + 1, r)
        if y > x:
            x = y
            prefix[l][r] = True
            path[l][r] = (i - l) + 1

        # x=max(x,a-call(i+1,r))

    a = 0
    for i in range(r, l - 1, -1):

        a += test[i]
        y = a - minmax(l, i - 1)
        if y > x:
            x = y
            prefix[l][r] = False
            path[l][r] = (r - i) + 1

        # x=max(x,a-call(l,i-1));

    vis[l][r] = True
    dp[l][r] = x

    print("the best sum calculated by minmax in range {},{} is {}\n".format(l, r, dp[l][r]))
    print("the number of value taken to calculate it is {} where prefix is {}\n".format(path[l][r], prefix[l][r]))

    return dp[l][r]


# ---------------------------------------------delay----------------------------------------------------

def delay(sec):
    for i in range(sec):
        time.sleep(1)
        print(".")


# --------------------------------------------- GAME --------------------------------------------

def game():
    global lastPressed, window, lo, hi, NumC, NumH, go

    test.clear()

    # --------------------------------------- LEVEL -------------------------------------------

    while (1):
        level = int(input("Choose a level among 1 to 10: "))
        # delay(1)
        if level >= 1 and level <= 10:
            print("\n")
            break
        print("Chose a level within the limit!!!")
        # delay(1)

    play = 1

    # ---------------------------------------- TAKE INPUT FROM TEXT FILE ---------------------------------------

    # with open('/G:/fourone/AI/lab/test.txt', 'r') as file:
    with open('test.txt', 'r') as file:
        input_lines = [line.strip() for line in file]

    # sys.stdin = open('/content/sample_data/test.txt', 'r')

    line_num = 0
    t = int(input_lines[line_num])
    # print(t)
    line_num += 1
    for i in range(t):
        n = int(input_lines[line_num])

        # print(n)
        line_num += 1

        num_list = input_lines[line_num].split()
        line_num += 1

        if (level == ((line_num) // 2)):
            len_arr = n
            for j in range(n):
                test.append(int(num_list[j]))
                # line_num +=1
                print(num_list[j])

    # delay(3)

    # ----------------------------------------- START GAME ----------------------------------------------

    valid = [0, len(test) - 1]
    # len_test = len(test)
    lo = 0
    hi = len_arr - 1

    while play:

        play = 0

        # make all the options unvisited intially
        for i in range(lo, hi + 1):
            for j in range(lo, hi + 1):
                vis[i][j] = False

        # ------------------------------- CHOOSE FIRST PLAYER ------------------------------

        while (1):

            print("Choose first player..\n1. Computer\n2. You\n")

            choice = int(input("Enter your choice: "))

            if (choice == 1 or choice == 2):
                break

            print("Wrong selection of player!!! Try again..\n\n")

        isAI = True
        print("the value of choice is :{}".format(choice))
        if (choice == 2):
            isAI = False
            print("the value of isAI is being changed to {}".format(isAI))

        # set initial points to zero
        user_val = 0
        comp_val = 0
        turn = 0

        while (lo <= hi):

            # ----------------------------------------If HUMAN MOVES FIRST--------------------------------------------

            if choice == 2:

                # global NumC, NumH, go
                # print("available values:")
                for i in range(lo, hi + 1):
                    # print(test[i])
                    btn = tk.Button(window, text=test[i], height=1, width=8,
                                    command=lambda lastPressed=lastPressed, press=i: show_press(press, lastPressed))
                    btn.pack()
                    lastPressed += 1
                    buttons.append(btn)

                print("\n\n")

                passBtn = Button(window, text=' PASS', fg='black', bg='#66ff33', height=2, width=9,
                                 command=lambda: passval(passBtn))
                passBtn.pack(pady=10)

                window.mainloop()

            # ----------------------------------------If AI MOVES FIRST--------------------------------------------
            elif choice == 1:

                global numC, NumH, go

                # isAI = True

                print("Initially, hi = {}, lo = {}".format(hi, lo))

                for i in range(lo, hi + 1):
                    # print(test[i])
                    btn = tk.Button(window, text=test[i], height=1, width=8,
                                    command=lambda lastPressed=lastPressed, press=i: show_press(press, lastPressed))
                    btn.pack()
                    lastPressed += 1
                    buttons.append(btn)

                print("\n\n")

                passBtn = Button(window, text=' PASS', fg='black', bg='#66ff33', height=2, width=9,
                                 command=lambda: passval(passBtn))
                passBtn.pack(pady=10)

                minmax(lo, hi)

                # print("After MinMAX, hi = {}, lo = {}".format(hi,lo))

                if (lo < hi):

                    if (prefix[lo][hi]):

                        # print(prefix[lo][hi])
                        # print(path[lo][hi])

                        for i in range(lo, lo + path[lo][hi]):
                            # print(i)
                            # comp_val+=numbers[i]
                            numC = numC + int(test[i])
                            test[i] = 0
                            buttons[i].config(bg="#c2f1ff")

                        lo += path[lo][hi]

                    else:

                        for i in range(hi, hi - path[lo][hi], -1):
                            # comp_val+=numbers[i]
                            numC = numC + int(test[i])
                            test[i] = 0
                            buttons[i].config(bg="#c2f1ff")

                        hi -= path[lo][hi]

                print("After MinMAX, hi = {}, lo = {}".format(hi, lo))

                totalC = str(numC)
                totalH = str(numH)
                finalC.set(totalC)
                finalH.set(totalH)

                window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
