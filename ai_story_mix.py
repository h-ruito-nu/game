"""
AI物語ミックス

冒険・恋愛・タイムトラベル・ホラー・日常の平和な話から2ジャンルを
ランダムに選び、昔話の部品と組み合わせて毎回異なる物語を作るゲーム。
物語に混ざった昔話を2つ当てるのが目的です。

外部サービスには接続せず、ジャンルごとの素材をランダムに組み合わせて
オリジナルの物語を生成します。
"""
import random
import tkinter as tk

from audio import AudioManager
from tales import NAMES, TALES


GENRES = {
    "冒険": {
        "opening": [
            "伝説の剣が眠る古城を目指していました",
            "魔王の城へ続く地図を手に入れました",
        ],
        "middle": [
            "勇者は仲間と力を合わせて険しい山を越えました",
            "封印を守る番人から勇気を試されました",
        ],
        "ending": [
            "伝説の剣を抜き、魔王を倒しました",
            "世界に平和を取り戻して、次の冒険へ旅立ちました",
        ],
    },
    "恋愛": {
        "opening": [
            "遠くの町に住む大切な人へ手紙を書きました",
            "祭りの夜、運命の人と出会いました",
        ],
        "middle": [
            "二人は離れていても同じ星を見上げていました",
            "すれ違いを乗り越えるため、まっすぐな気持ちを伝えました",
        ],
        "ending": [
            "二人は約束の場所で再会し、幸せに暮らしました",
            "想いは届き、町中が祝福する恋になりました",
        ],
    },
    "タイムトラベル": {
        "opening": [
            "古い時計を回すと、見知らぬ時代へ飛びました",
            "未来から来た不思議な手紙を受け取りました",
        ],
        "middle": [
            "過去を変えすぎないように、歴史の分かれ道を探しました",
            "未来の自分と出会い、今を大切にする理由を知りました",
        ],
        "ending": [
            "元の時代へ戻り、忘れられない一日を胸に刻みました",
            "時の流れを守りながら、未来を少しだけ良くしました",
        ],
    },
    "ホラー": {
        "opening": [
            "月のない夜、誰も住んでいない屋敷に入りました",
            "夜道で、後ろから自分の名前を呼ぶ声を聞きました",
        ],
        "middle": [
            "古い鏡の中だけに、知らない影が映っていました",
            "閉じたはずの扉が少しずつ開き、冷たい風が吹きました",
        ],
        "ending": [
            "朝になると、そこには足あとだけが残っていました",
            "振り返ると、物語は静かに最初の夜へ戻っていました",
        ],
    },
    "日常": {
        "opening": [
            "いつもの朝、町の小さなパン屋へ出かけました",
            "縁側でお茶を飲みながら、穏やかな一日を始めました",
        ],
        "middle": [
            "近所の人たちと料理を作り、たわいない話で笑いました",
            "落とし物を届けると、町のみんなからお礼を言われました",
        ],
        "ending": [
            "夕暮れの鐘を聞きながら、今日も平和だったと思いました",
            "明日も同じような日が来ることを、うれしく感じました",
        ],
    },
}

GENRE_NAMES = list(GENRES)


def make_original_story(first_genre, second_genre):
    """2つのジャンル素材から、昔話の部品を混ぜる土台を作る。"""
    first = GENRES[first_genre]
    second = GENRES[second_genre]
    return [
        f"【{first_genre}×{second_genre}】",
        f"むかしむかし、{random.choice(first['opening'])}。"
        + f"そこへ、{random.choice(second['opening'])}。".replace("。。", "。"),
        f"そのとき、{random.choice(first['middle'])}。",
        f"さらに、{random.choice(second['middle'])}。",
        f"物語の中で、{random.choice(first['ending'])}。",
        f"そして、{random.choice(second['ending'])}。",
        "そこには、昔話の不思議な出来事も重なっていました。",
        "めでたし、めでたし。",
    ]


def make_story(a_name, b_name, first_genre, second_genre):
    """ジャンル物語に、2つの昔話の部品を加えて表示用の文章にする。"""
    a, b = TALES[a_name], TALES[b_name]
    lines = make_original_story(first_genre, second_genre)
    lines.insert(2, f"旅の途中で、{a['hero']}と出会い、{b['item']}を託されました。")
    lines.insert(4, f"{a['helper']}と力を合わせ、{b['place']}へ向かいました。")
    lines.insert(6, f"そこで、{a['event']}。")
    lines.insert(8, f"最後には、{b['ending']}。")
    return "\n".join(lines)


def make_hints(a_name, b_name):
    """昔話に関するヒントだけを段階的に返す。"""
    a, b = TALES[a_name], TALES[b_name]
    pairs = [
        ("舞台", [a["place"], b["place"]]),
        ("小道具", [a["item"], b["item"]]),
        ("主人公", [a["hero"], b["hero"]]),
    ]
    hints = []
    for label, values in pairs:
        random.shuffle(values)
        hints.append(f"ヒント{len(hints) + 1}:元ネタの{label}は「{values[0]}」と「{values[1]}」")
    return hints


class StoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AI物語ミックス")
        self.root.geometry("760x700")
        self.root.minsize(620, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.colors = {
            "background": "#fff8e7",
            "title": "#7b3f00",
            "text": "#4b3832",
            "panel": "#fffdf5",
            "border": "#e6c98a",
            "button": "#f4b183",
            "button_active": "#ffd1a9",
            "card": "#fff1c1",
            "card_active": "#ffe49a",
            "selected": "#9ad7ff",
            "correct": "#ffd966",
        }
        root.configure(bg=self.colors["background"])
        self.rounds = 3
        self.round_no = 0
        self.total = 0
        self.a_name = ""
        self.b_name = ""
        self.hints = []
        self.used_hints = 0
        self.audio = AudioManager()
        self.selected_names = set()
        self.choice_cards = {}

        tk.Label(
            root,
            text="AI物語ミックス",
            font=("Yu Gothic UI", 22, "bold"),
            fg=self.colors["title"],
            bg=self.colors["background"],
        ).pack(
            pady=(15, 2)
        )
        tk.Label(
            root,
            text="2つのジャンルと2つの昔話を混ぜた物語から、昔話を2つ当ててください",
            font=("Yu Gothic UI", 11),
            fg=self.colors["text"],
            bg=self.colors["background"],
        ).pack()
        self.round_label = tk.Label(
            root,
            font=("Yu Gothic UI", 13, "bold"),
            fg=self.colors["title"],
            bg=self.colors["background"],
        )
        self.round_label.pack(pady=(14, 5))
        self.story_text = tk.Text(
            root,
            height=14,
            wrap="word",
            font=("Yu Gothic UI", 12),
            padx=10,
            pady=8,
            state="disabled",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            relief="solid",
            borderwidth=1,
        )
        self.story_text.pack(fill="both", expand=True, padx=25)
        tk.Label(
            root,
            text="混ざっている昔話を2つ選択",
            font=("Yu Gothic UI", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"],
        ).pack(pady=(12, 3))
        self.cards_frame = tk.Frame(
            root,
            bg=self.colors["background"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        self.cards_frame.pack(padx=25, pady=5)
        for index, name in enumerate(NAMES):
            card = tk.Button(
                self.cards_frame,
                text=name,
                width=15,
                height=2,
                font=("Yu Gothic UI", 11, "bold"),
                bg=self.colors["card"],
                fg=self.colors["text"],
                activebackground=self.colors["card_active"],
                activeforeground=self.colors["text"],
                relief="raised",
                borderwidth=2,
                command=lambda selected_name=name: self.toggle_card(selected_name),
            )
            card.grid(row=index // 4, column=index % 4, padx=5, pady=5)
            self.choice_cards[name] = card
        self.status_label = tk.Label(
            root,
            text="",
            font=("Yu Gothic UI", 11),
            wraplength=700,
            fg=self.colors["text"],
            bg=self.colors["background"],
        )
        self.status_label.pack(pady=8)
        buttons = tk.Frame(root, bg=self.colors["background"])
        buttons.pack()
        button_options = {
            "width": 13,
            "font": ("Yu Gothic UI", 10, "bold"),
            "bg": self.colors["button"],
            "fg": self.colors["text"],
            "activebackground": self.colors["button_active"],
            "activeforeground": self.colors["text"],
            "relief": "raised",
            "borderwidth": 2,
        }
        self.answer_button = tk.Button(
            buttons, text="答え合わせ", command=self.check_answer, **button_options
        )
        self.answer_button.pack(side="left", padx=4)
        self.hint_button = tk.Button(
            buttons, text="ヒントを見る", command=self.show_hint, **button_options
        )
        self.hint_button.pack(side="left", padx=4)
        self.give_up_button = tk.Button(
            buttons, text="降参", command=self.give_up, **button_options
        )
        self.give_up_button.pack(side="left", padx=4)
        self.next_button = tk.Button(
            buttons,
            text="次の問題",
            command=self.next_round,
            state="disabled",
            **button_options,
        )
        self.next_button.pack(side="left", padx=4)
        self.next_round()

    def close(self):
        self.audio.close()
        self.root.destroy()

    def set_story(self, story):
        self.story_text.config(state="normal")
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert("1.0", story)
        self.story_text.config(state="disabled")

    def toggle_card(self, name):
        if name in self.selected_names:
            self.selected_names.remove(name)
        elif len(self.selected_names) < 2:
            self.selected_names.add(name)
            self.audio.play("select")
        self.update_card_colors()

    def update_card_colors(self, correct=False):
        for name, card in self.choice_cards.items():
            if correct and name in {self.a_name, self.b_name}:
                card.config(
                    bg=self.colors["correct"],
                    activebackground="#fff2a8",
                    relief="sunken",
                )
            elif name in self.selected_names:
                card.config(
                    bg=self.colors["selected"],
                    activebackground="#c9ecff",
                    relief="sunken",
                )
            else:
                card.config(
                    bg=self.colors["card"],
                    activebackground=self.colors["card_active"],
                    relief="raised",
                )

    def set_cards_state(self, state):
        for card in self.choice_cards.values():
            card.config(state=state)

    def next_round(self):
        if self.round_no >= self.rounds:
            self.audio.play("finish")
            self.round_label.config(text=f"ゲーム終了　{self.total} / {self.rounds * 10}点")
            self.set_story("おつかれさまでした！")
            self.status_label.config(text="全問終了です。")
            for button in (self.answer_button, self.hint_button, self.give_up_button):
                button.config(state="disabled")
            self.next_button.config(state="disabled")
            self.set_cards_state("disabled")
            return
        self.round_no += 1
        self.a_name, self.b_name = random.sample(NAMES, 2)
        first_genre, second_genre = random.sample(GENRE_NAMES, 2)
        self.hints = make_hints(self.a_name, self.b_name)
        self.used_hints = 0
        self.selected_names.clear()
        self.round_label.config(text=f"第{self.round_no}問　（得点: {self.total}点）")
        self.set_story(make_story(self.a_name, self.b_name, first_genre, second_genre))
        self.update_card_colors()
        self.set_cards_state("normal")
        self.status_label.config(text="昔話を2つ選んでください。")
        self.answer_button.config(state="normal")
        self.hint_button.config(state="normal")
        self.give_up_button.config(state="normal")
        self.next_button.config(state="disabled")

    def finish_round(self, message):
        self.status_label.config(text=message)
        for button in (self.answer_button, self.hint_button, self.give_up_button):
            button.config(state="disabled")
        self.next_button.config(
            state="normal", text="結果を見る" if self.round_no == self.rounds else "次の問題"
        )
        self.set_cards_state("disabled")

    def check_answer(self):
        selected = self.selected_names
        if len(selected) != 2:
            self.status_label.config(text="昔話を2つ選択してください。")
            return
        if selected != {self.a_name, self.b_name}:
            self.audio.play("wrong")
            self.status_label.config(text="ざんねん、ちがいます。もう一度選んでください。")
            return
        point = max(1, 10 - 3 * self.used_hints)
        self.total += point
        self.audio.play("correct")
        self.update_card_colors(correct=True)
        self.finish_round(f"正解！ +{point}点　元ネタは「{self.a_name}」と「{self.b_name}」でした。")

    def show_hint(self):
        if self.used_hints < len(self.hints):
            self.audio.play("hint")
            self.status_label.config(text=self.hints[self.used_hints])
            self.used_hints += 1
        else:
            self.audio.play("wrong")
            self.status_label.config(text="ヒントはもうありません。")

    def give_up(self):
        self.audio.play("give_up")
        self.finish_round(f"正解は「{self.a_name}」と「{self.b_name}」でした。 +0点")


def main():
    root = tk.Tk()
    StoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
