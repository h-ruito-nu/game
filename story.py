"""昔話を組み合わせた物語とヒントを作る処理。"""

import random

from tales import TALES


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
    """ヒントを段階的に返す（後ろほど答えに近い）。"""
    a, b = TALES[a_name], TALES[b_name]
    values = [[a["place"], b["place"]], [a["item"], b["item"]], [a["hero"], b["hero"]]]
    for pair in values:
        random.shuffle(pair)
    return [
        f"ヒント1:元ネタの舞台は「{values[0][0]}」と「{values[0][1]}」",
        f"ヒント2:元ネタの小道具は「{values[1][0]}」と「{values[1][1]}」",
        f"ヒント3:元ネタの主人公は「{values[2][0]}」と「{values[2][1]}」",
    ]
