#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
座標取得ツール
マウス位置や画面領域の座標を取得するためのツール
"""

import pyautogui
import time
import sys
import tkinter as tk
from tkinter import messagebox

def get_mouse_position():
    """マウスの現在位置を取得"""
    print("マウス座標取得ツール")
    print("=" * 40)
    print("マウスを移動させて座標を確認してください")
    print("終了するには Ctrl+C を押してください")
    print()
    
    try:
        while True:
            x, y = pyautogui.position()
            rgb = pyautogui.screenshot().getpixel((x, y))
            print(f"マウス位置: X={x}, y={y}, RGB={rgb}", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n座標取得を終了しました")

def get_screen_info():
    """画面情報を表示"""
    print("画面情報:")
    print("=" * 40)
    width, height = pyautogui.size()
    print(f"画面サイズ: {width} x {height}")
    print(f"画面解像度: {width} x {height}")
    print()

def get_region_coordinates():
    """領域の座標を取得"""
    print("領域座標取得ツール")
    print("=" * 40)
    print("1. 開始点（左上）でEnterを押してください")
    print("2. 終了点（右下）でEnterを押してください")
    print()
    
    input("開始点（左上）の位置にマウスを移動してEnterを押してください...")
    start_x, start_y = pyautogui.position()
    print(f"開始点: X={start_x}, Y={start_y}")
    
    input("終了点（右下）の位置にマウスを移動してEnterを押してください...")
    end_x, end_y = pyautogui.position()
    print(f"終了点: X={end_x}, Y={end_y}")
    
    # 領域を計算
    x = min(start_x, end_x)
    y = min(start_y, end_y)
    width = abs(end_x - start_x)
    height = abs(end_y - start_y)
    
    print()
    print("取得した領域:")
    print(f"region = ({x}, {y}, {width}, {height})")
    print()
    print("config.json用の形式:")
    print(f'"region": [{x}, {y}, {width}, {height}]')

def create_gui():
    """GUI版の座標取得ツール"""
    root = tk.Tk()
    root.title("座標取得ツール")
    root.geometry("400x300")
    
    def show_mouse_position():
        x, y = pyautogui.position()
        rgb = pyautogui.screenshot().getpixel((x, y))
        position_label.config(text=f"マウス位置: X={x}, Y={y}, RGB={rgb}")
        root.after(100, show_mouse_position)
    
    def get_region():
        root.iconify()  # ウィンドウを最小化
        time.sleep(1)
        
        messagebox.showinfo("開始点", "開始点（左上）の位置でOKを押してください")
        start_x, start_y = pyautogui.position()
        
        messagebox.showinfo("終了点", "終了点（右下）の位置でOKを押してください")
        end_x, end_y = pyautogui.position()
        
        # 領域を計算
        x = min(start_x, end_x)
        y = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        
        result = f"region = ({x}, {y}, {width}, {height})\n\nconfig.json用:\n\"region\": [{x}, {y}, {width}, {height}]"
        messagebox.showinfo("結果", result)
        root.deiconify()  # ウィンドウを復元
    
    # GUI要素
    title_label = tk.Label(root, text="座標取得ツール", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    position_label = tk.Label(root, text="マウス位置: 移動中...", font=("Arial", 12))
    position_label.pack(pady=10)
    
    region_button = tk.Button(root, text="領域座標を取得", command=get_region, font=("Arial", 12))
    region_button.pack(pady=10)
    
    info_label = tk.Label(root, text="領域座標を取得ボタンを押すと\nウィンドウが最小化され、\n開始点と終了点を選択できます", font=("Arial", 10))
    info_label.pack(pady=10)
    
    # マウス位置の更新を開始
    show_mouse_position()
    
    root.mainloop()

def main():
    """メイン処理"""
    print("座標取得ツール")
    print("=" * 40)
    print("1. マウス座標をリアルタイム表示")
    print("2. 画面情報を表示")
    print("3. 領域座標を取得")
    print("4. GUI版を起動")
    print("5. 終了")
    print()
    
    while True:
        try:
            choice = input("選択してください (1-5): ").strip()
            
            if choice == "1":
                get_mouse_position()
                break
            elif choice == "2":
                get_screen_info()
                break
            elif choice == "3":
                get_region_coordinates()
                break
            elif choice == "4":
                create_gui()
                break
            elif choice == "5":
                print("終了します")
                break
            else:
                print("1-5の数字を入力してください")
        except KeyboardInterrupt:
            print("\n終了します")
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1) 