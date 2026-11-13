"""ゲームの実行入口。

このファイルを実行すると、AI物語ミックスが起動します。
"""

import tkinter as tk

from ai_story_mix import StoryGame


def main():
    root = tk.Tk()
    StoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
