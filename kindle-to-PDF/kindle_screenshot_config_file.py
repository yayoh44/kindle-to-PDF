#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kindle for PC 自動スクリーンショットツール（設定ファイル版）
設定ファイルから設定を読み込んで実行するツール
"""

import os
import time
import pyautogui
from PIL import Image
import sys
import argparse
import json

def load_config(config_file="config.json"):
    """設定ファイルを読み込み"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"設定ファイル '{config_file}' を読み込みました")
        return config
    except FileNotFoundError:
        print(f"設定ファイル '{config_file}' が見つかりません")
        print("デフォルト設定を使用します")
        return {
            "wait_time": 10,
            "page_count": 50,
            "region": [200, 150, 800, 1000],
            "page_delay": 3,
            "output_folder": "screenshots",
            "page_method": "auto",
            "max_pages": 1000
        }
    except json.JSONDecodeError as e:
        print(f"設定ファイルの形式が正しくありません: {e}")
        sys.exit(1)

def create_screenshots_folder(folder_name):
    """スクリーンショット保存用のフォルダを作成"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"フォルダ '{folder_name}' を作成しました")
    return folder_name

def take_screenshot(region, filename):
    """指定した領域のスクリーンショットを取得して保存"""
    try:
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(filename)
        print(f"保存完了: {filename}")
        return True
    except Exception as e:
        print(f"スクリーンショット保存エラー: {e}")
        return False

def page_turn_keyboard():
    """キーボードでページ送り"""
    print("キーボードでページ送り...")
    pyautogui.press('right')
    time.sleep(0.5)

def page_turn_mouse(region):
    """マウスクリックでページ送り"""
    print("マウスクリックでページ送り...")
    click_x = region[0] + region[2] - 50
    click_y = region[1] + region[3] // 2
    pyautogui.click(click_x, click_y)
    time.sleep(0.5)

def page_turn_scroll(region):
    """スクロールでページ送り"""
    print("スクロールでページ送り...")
    scroll_x = region[0] + region[2] // 2
    scroll_y = region[1] + region[3] // 2
    pyautogui.scroll(-3, x=scroll_x, y=scroll_y)
    time.sleep(0.5)

def page_turn_hotkey():
    """ホットキーでページ送り"""
    print("ホットキーでページ送り...")
    pyautogui.hotkey('ctrl', 'right')
    time.sleep(0.5)

def page_turn_auto(region, attempt=1):
    """自動的に最適なページ送り方法を選択"""
    methods = [
        ('keyboard', page_turn_keyboard),
        ('mouse', lambda: page_turn_mouse(region)),
        ('scroll', lambda: page_turn_scroll(region)),
        ('hotkey', page_turn_hotkey)
    ]
    
    for method_name, method_func in methods:
        try:
            print(f"ページ送り方法 {attempt}: {method_name}")
            method_func()
            return True
        except Exception as e:
            print(f"ページ送り方法 {method_name} でエラー: {e}")
            continue
    return False

def parse_arguments():
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(description='Kindle for PC 自動スクリーンショットツール（設定ファイル版）')
    parser.add_argument('--config', type=str, default='config.json',
                       help='設定ファイルのパス（デフォルト: config.json）')
    parser.add_argument('--pages', type=int,
                       help='ページ数を上書き（設定ファイルより優先）')
    parser.add_argument('--no-countdown', action='store_true',
                       help='カウントダウンを表示しない')
    
    return parser.parse_args()

def main():
    """メイン処理"""
    args = parse_arguments()
    
    # 設定ファイルを読み込み
    config = load_config(args.config)
    
    # コマンドライン引数で上書き
    if args.pages:
        config['page_count'] = args.pages
    
    print("Kindle for PC 自動スクリーンショットツール（設定ファイル版）")
    print("=" * 60)
    
    # 設定を表示
    print("設定:")
    print(f"  待機時間: {config['wait_time']}秒")
    print(f"  取得回数: {config['page_count']}回")
    print(f"  取得領域: x={config['region'][0]}, y={config['region'][1]}, width={config['region'][2]}, height={config['region'][3]}")
    print(f"  ページ間待機: {config['page_delay']}秒")
    print(f"  出力フォルダ: {config['output_folder']}")
    print(f"  ページ送り方法: {config['page_method']}")
    print()
    
    # ページ数確認
    if config['page_count'] > config['max_pages']:
        print(f"警告: ページ数({config['page_count']})が最大値({config['max_pages']})を超えています")
        response = input("続行しますか？ (y/N): ")
        if response.lower() != 'y':
            print("処理を中止しました")
            return
    
    # スクリーンショット保存用フォルダを作成
    screenshots_folder = create_screenshots_folder(config['output_folder'])
    
    print(f"{config['wait_time']}秒後に処理を開始します...")
    print("Kindle for PCで書籍を開いてください")
    print("Kindleウィンドウをクリックしてアクティブにしてください")
    
    # 待機時間
    if not args.no_countdown:
        for i in range(config['wait_time'], 0, -1):
            print(f"開始まで {i} 秒...")
            time.sleep(1)
    else:
        time.sleep(config['wait_time'])
    
    print("処理を開始します！")
    
    # スクリーンショットを取得
    for page_num in range(1, config['page_count'] + 1):
        filename = os.path.join(screenshots_folder, f"page_{page_num:03d}.png")
        
        if take_screenshot(tuple(config['region']), filename):
            print(f"ページ {page_num}/{config['page_count']} をキャプチャしました")
        
        # 最後のページ以外はページ送り
        if page_num < config['page_count']:
            print("次のページに移動します...")
            
            if config['page_method'] == 'auto':
                success = page_turn_auto(tuple(config['region']))
                if not success:
                    print("全てのページ送り方法が失敗しました")
            elif config['page_method'] == 'keyboard':
                page_turn_keyboard()
            elif config['page_method'] == 'mouse':
                page_turn_mouse(tuple(config['region']))
            elif config['page_method'] == 'scroll':
                page_turn_scroll(tuple(config['region']))
            elif config['page_method'] == 'hotkey':
                page_turn_hotkey()
            
            time.sleep(config['page_delay'])
    
    print("=" * 60)
    print("スクリーンショット取得が完了しました！")
    print(f"保存先: {os.path.abspath(screenshots_folder)}")
    print(f"取得したページ数: {config['page_count']}")
    print("\nPDF化するには以下のコマンドを実行してください:")
    print("python create_pdf.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1) 