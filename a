"""
むかしばなしミックス(仮)
テーマ「組み合わさる」:2つの昔話を混ぜた新作物語から、元ネタを当てるゲーム。

遊び方:物語を読んで、混ざっている昔話を2つ当てる。
ヒントを使うほど得点が下がる。
"""
import random
import tkinter as tk

# ---- 昔話データ(部品) -------------------------------------------------
# 各部品は文章に埋め込めるよう、言い回しをそろえてある。
# event / ending は「〜した」という過去形の文にしておく。
TALES = {
    "桃太郎": {
        "hero": "桃から生まれた男の子",
        "helper": "犬とサルとキジ",
        "item": "きびだんご",
        "place": "川のほとりの村",
        "event": "鬼が村を荒らしていた",
        "ending": "宝物を持って村に帰った",
    },
    "浦島太郎": {
        "hero": "心優しい漁師",
        "helper": "海の亀",
        "item": "玉手箱",
        "place": "海辺の村",
        "event": "子どもにいじめられている亀を見つけた",
        "ending": "玉手箱を開けておじいさんになってしまった",
    },
    "かぐや姫": {
        "hero": "光る竹から見つかった女の子",
        "helper": "竹取りのおじいさん",
        "item": "光る竹",
        "place": "竹やぶ",
        "event": "貴族たちから次々に結婚を申し込まれた",
        "ending": "月へ帰っていった",
    },
    "かさじぞう": {
        "hero": "貧しいおじいさん",
        "helper": "六体のお地蔵さま",
        "item": "手編みの笠",
        "place": "雪の降る山道",
        "event": "雪をかぶったお地蔵さまを見つけた",
        "ending": "お礼の品々が家に届いた",
    },
    "花咲かじいさん": {
        "hero": "正直なおじいさん",
        "helper": "しゃべる白い犬",
        "item": "不思議な灰",
        "place": "畑のある村",
        "event": "犬が「ここ掘れワンワン」と鳴いた",
        "ending": "枯れ木に満開の花を咲かせた",
    },
    "一寸法師": {
        "hero": "親指ほどの小さな男の子",
        "helper": "都のお姫さま",
        "item": "針の刀",
        "place": "にぎやかな都",
        "event": "お姫さまが鬼にさらわれそうになった",
        "ending": "打ち出の小づちで大きくなった",
    },
    "さるかに合戦": {
        "hero": "子ガニ",
        "helper": "栗とハチと臼",
        "item": "柿の種",
        "place": "山のふもと",
        "event": "ずるいサルにおにぎりを取られた",
        "ending": "サルをこらしめた",
    },
    "わらしべ長者": {
        "hero": "貧しい若者",
        "helper": "観音さま",
        "item": "一本のわらしべ",
        "place": "旅の道",
        "event": "転んだ拍子にわらを握った",
        "ending": "物々交換を重ねて大金持ちになった",
    },
}

NAMES = list(TALES.keys())


# ---- 物語の組み立て -----------------------------------------------------
def make_story(a_name, b_name):
    """Aを土台に、Bの部品を混ぜて新しい物語を作る。"""
    a, b = TALES[a_name], TALES[b_name]
    lines = [
        f"むかしむかし、{a['place']}に{a['hero']}がいました。",
        f"ある日、{a['event']}のです。",
        f"そこへ{b['helper']}が現れ、{b['item']}を差し出しました。",
        f"{a['hero']}は{a['helper']}といっしょに、{b['place']}へ向かいます。",
        f"やがて、{b['event']}ではありませんか。",
        f"こうして、{a['ending']}。さらに、{b['ending']}。",
        "めでたし、めでたし。",
    ]
    return "\n".join(lines)


def make_hints(a_name, b_name):
    """ヒントを段階的に返す(後ろほど答えに近い)。"""
    a, b = TALES[a_name], TALES[b_name]
    places = [a["place"], b["place"]]
    items = [a["item"], b["item"]]
    heroes = [a["hero"], b["hero"]]
    for lst in (places, items, heroes):
        random.shuffle(lst)
    return [
        f"ヒント1:元ネタの舞台は「{places[0]}」と「{places[1]}」",
        f"ヒント2:元ネタの小道具は「{items[0]}」と「{items[1]}」",
        f"ヒント3:元ネタの主人公は「{heroes[0]}」と「{heroes[1]}」",
    ]


# ---- ゲーム本体 ---------------------------------------------------------
class StoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("むかしばなしミックス")
        self.root.geometry("680x620")
        self.root.minsize(560, 520)

        self.rounds = 3
        self.round_no = 0
        self.total = 0
        self.a_name = ""
        self.b_name = ""
        self.hints = []
        self.used_hints = 0

        tk.Label(
            root, text="むかしばなしミックス", font=("Yu Gothic UI", 22, "bold")
        ).pack(pady=(15, 2))
        tk.Label(
            root,
            text="物語に混ざっている昔話を2つ選んでください",
            font=("Yu Gothic UI", 11),
        ).pack()

        self.round_label = tk.Label(root, font=("Yu Gothic UI", 13, "bold"))
        self.round_label.pack(pady=(14, 5))

        self.story_text = tk.Text(
            root,
            height=8,
            wrap="word",
            font=("Yu Gothic UI", 12),
            padx=10,
            pady=8,
            state="disabled",
        )
        self.story_text.pack(fill="x", padx=25)

        tk.Label(
            root, text="元ネタだと思う昔話を2つ選択", font=("Yu Gothic UI", 11, "bold")
        ).pack(pady=(12, 3))
        self.choices = tk.Listbox(
            root,
            selectmode=tk.MULTIPLE,
            height=len(NAMES),
            exportselection=False,
            font=("Yu Gothic UI", 11),
        )
        for name in NAMES:
            self.choices.insert(tk.END, name)
        self.choices.pack()

        self.status_label = tk.Label(
            root, text="", font=("Yu Gothic UI", 11), wraplength=620
        )
        self.status_label.pack(pady=8)

        buttons = tk.Frame(root)
        buttons.pack()
        self.answer_button = tk.Button(
            buttons, text="答え合わせ", width=13, command=self.check_answer
        )
        self.answer_button.pack(side="left", padx=4)
        self.hint_button = tk.Button(
            buttons, text="ヒントを見る", width=13, command=self.show_hint
        )
        self.hint_button.pack(side="left", padx=4)
        self.give_up_button = tk.Button(
            buttons, text="降参", width=13, command=self.give_up
        )
        self.give_up_button.pack(side="left", padx=4)
        self.next_button = tk.Button(
            buttons, text="次の問題", width=13, command=self.next_round, state="disabled"
        )
        self.next_button.pack(side="left", padx=4)

        self.next_round()

    def set_story(self, story):
        self.story_text.config(state="normal")
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert("1.0", story)
        self.story_text.config(state="disabled")

    def next_round(self):
        if self.round_no >= self.rounds:
            self.round_label.config(text=f"ゲーム終了　{self.total} / {self.rounds * 10}点")
            self.set_story("おつかれさまでした！")
            self.status_label.config(text="全問終了です。")
            for button in (self.answer_button, self.hint_button, self.give_up_button):
                button.config(state="disabled")
            self.next_button.config(state="disabled")
            self.choices.config(state="disabled")
            return

        self.round_no += 1
        self.a_name, self.b_name = random.sample(NAMES, 2)
        self.hints = make_hints(self.a_name, self.b_name)
        self.used_hints = 0
        self.round_label.config(text=f"第{self.round_no}問　（得点: {self.total}点）")
        self.set_story(make_story(self.a_name, self.b_name))
        self.choices.config(state="normal")
        self.choices.selection_clear(0, tk.END)
        self.status_label.config(text="昔話を2つ選んでください。")
        self.answer_button.config(state="normal")
        self.hint_button.config(state="normal")
        self.give_up_button.config(state="normal")
        self.next_button.config(state="disabled")

    def finish_round(self, message):
        self.status_label.config(text=message)
        self.answer_button.config(state="disabled")
        self.hint_button.config(state="disabled")
        self.give_up_button.config(state="disabled")
        self.next_button.config(
            state="normal", text="結果を見る" if self.round_no == self.rounds else "次の問題"
        )
        self.choices.config(state="disabled")

    def check_answer(self):
        selected = {self.choices.get(i) for i in self.choices.curselection()}
        if len(selected) != 2:
            self.status_label.config(text="昔話を2つ選択してください。")
            return
        if selected != {self.a_name, self.b_name}:
            self.status_label.config(text="ざんねん、ちがいます。もう一度選んでください。")
            return

        point = 10 - 3 * self.used_hints
        self.total += point
        self.finish_round(
            f"正解！ +{point}点　元ネタは「{self.a_name}」と「{self.b_name}」でした。"
        )

    def show_hint(self):
        if self.used_hints < len(self.hints):
            self.status_label.config(text=self.hints[self.used_hints])
            self.used_hints += 1
        else:
            self.status_label.config(text="ヒントはもうありません。")

    def give_up(self):
        self.finish_round(
            f"正解は「{self.a_name}」と「{self.b_name}」でした。 +0点"
        )


def main():
    root = tk.Tk()
    StoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()