from __future__ import annotations

import random
from functools import lru_cache
from typing import Dict, List, Tuple

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "change-this-for-production"

CARD_ORDER = ["A", "2", "3", "4", "5", "J", "Q", "K"]
FULL_DECK: Dict[str, int] = {card: 4 for card in CARD_ORDER}
BASE_VALUE = {"A": 0, "2": 2, "3": 3, "4": 4, "5": 5, "J": 5, "Q": 5, "K": 5}
TARGET = 16

COLOR_CLASS = {
    "A": "card-a",
    "2": "card-2",
    "3": "card-3",
    "4": "card-4",
    "5": "card-5",
    "J": "card-j",
    "Q": "card-q",
    "K": "card-k",
}


def fresh_state() -> dict:
    return {"hand": [], "remaining": FULL_DECK.copy(), "status": "Ready", "finished": False}


def get_state() -> dict:
    if "game" not in session:
        session["game"] = fresh_state()
    return session["game"]


def save_state(state: dict) -> None:
    session["game"] = state
    session.modified = True


def draw_random_card(remaining: Dict[str, int]) -> str | None:
    deck = [card for card, count in remaining.items() for _ in range(count)]
    if not deck:
        return None
    card = random.choice(deck)
    remaining[card] -= 1
    return card


def hand_base_and_aces(hand: List[str]) -> Tuple[int, int]:
    base = sum(BASE_VALUE[c] for c in hand if c != "A")
    aces = sum(1 for c in hand if c == "A")
    return base, aces


def best_total(base: int, aces: int) -> Tuple[int, bool, List[int]]:
    """Return best total, bust status, and all possible ace-adjusted totals."""
    totals = [base + aces + 5 * six_count for six_count in range(aces + 1)]
    safe = [t for t in totals if t <= TARGET]
    if safe:
        return max(safe), False, sorted(set(totals))
    return min(totals), True, sorted(set(totals))


def remaining_tuple(remaining: Dict[str, int]) -> Tuple[int, ...]:
    return tuple(int(remaining.get(card, 0)) for card in CARD_ORDER)


def tuple_to_remaining(counts: Tuple[int, ...]) -> Dict[str, int]:
    return {card: counts[i] for i, card in enumerate(CARD_ORDER)}


def new_base_aces(base: int, aces: int, card: str) -> Tuple[int, int]:
    if card == "A":
        return base, aces + 1
    return base + BASE_VALUE[card], aces


def decrement_count(counts: Tuple[int, ...], idx: int) -> Tuple[int, ...]:
    arr = list(counts)
    arr[idx] -= 1
    return tuple(arr)


@lru_cache(maxsize=None)
def optimal_value(base: int, aces: int, counts: Tuple[int, ...]) -> float:
    total, bust, _ = best_total(base, aces)
    if bust:
        return 0.0
    stand_value = float(total)
    cards_left = sum(counts)
    if cards_left == 0:
        return stand_value

    hit_value = 0.0
    for idx, card in enumerate(CARD_ORDER):
        count = counts[idx]
        if count <= 0:
            continue
        nb, na = new_base_aces(base, aces, card)
        next_counts = decrement_count(counts, idx)
        hit_value += (count / cards_left) * optimal_value(nb, na, next_counts)
    return max(stand_value, hit_value)


def hit_expected_value(base: int, aces: int, remaining: Dict[str, int]) -> float:
    counts = remaining_tuple(remaining)
    cards_left = sum(counts)
    if cards_left == 0:
        total, bust, _ = best_total(base, aces)
        return 0.0 if bust else float(total)

    ev = 0.0
    for idx, card in enumerate(CARD_ORDER):
        count = counts[idx]
        if count <= 0:
            continue
        nb, na = new_base_aces(base, aces, card)
        next_counts = decrement_count(counts, idx)
        ev += (count / cards_left) * optimal_value(nb, na, next_counts)
    return ev


def one_hit_stats(base: int, aces: int, remaining: Dict[str, int]) -> dict:
    cards_left = sum(remaining.values())
    rows = []
    bust_prob = 0.0
    safe_prob = 0.0
    one_hit_ev = 0.0

    if cards_left == 0:
        return {"rows": [], "bust_prob": 0.0, "safe_prob": 1.0, "one_hit_ev": 0.0}

    for card in CARD_ORDER:
        count = remaining.get(card, 0)
        if count <= 0:
            continue
        prob = count / cards_left
        nb, na = new_base_aces(base, aces, card)
        total, bust, totals = best_total(nb, na)
        payoff = 0 if bust else total
        one_hit_ev += prob * payoff
        if bust:
            bust_prob += prob
        else:
            safe_prob += prob
        rows.append(
            {
                "card": card,
                "count": count,
                "prob": prob,
                "new_total": total,
                "bust": bust,
                "payoff": payoff,
                "totals": totals,
                "corner": corner_value(card, total),
                "color_class": COLOR_CLASS[card],
            }
        )
    return {"rows": rows, "bust_prob": bust_prob, "safe_prob": safe_prob, "one_hit_ev": one_hit_ev}


def corner_value(card: str, current_total: int | None = None) -> str:
    if card == "A":
        return "1/6"
    if card in {"J", "Q", "K"}:
        return "5"
    return card


def card_view(card: str) -> dict:
    return {
        "label": card,
        "corner": corner_value(card),
        "color_class": COLOR_CLASS[card],
    }


def build_context(state: dict) -> dict:
    hand = state["hand"]
    remaining = state["remaining"]
    base, aces = hand_base_and_aces(hand)
    total, bust, possible_totals = best_total(base, aces)
    stand_ev = 0.0 if bust else float(total)
    hit_ev = 0.0 if bust or sum(remaining.values()) == 0 else hit_expected_value(base, aces, remaining)
    stats = one_hit_stats(base, aces, remaining)
    recommendation = "Hit" if (not bust and hit_ev > stand_ev) else "Stand"

    if bust:
        state["finished"] = True
        state["status"] = "Bust. Final payoff is 0."

    threshold_text = "Hit below 12, stand on 12 or above"
    if total >= 12 and not bust:
        threshold_text = "Stand on 12 or above"
    elif total <= 11 and len(hand) > 0:
        threshold_text = "Hit below 12"

    return {
        "hand": [card_view(c) for c in hand],
        "raw_hand": hand,
        "remaining": remaining,
        "total": total,
        "possible_totals": possible_totals,
        "bust": bust,
        "status": state.get("status", "Ready"),
        "finished": state.get("finished", False),
        "stand_ev": stand_ev,
        "hit_ev": hit_ev,
        "hit_edge": hit_ev - stand_ev,
        "recommendation": recommendation,
        "stats": stats,
        "cards_left": sum(remaining.values()),
        "target": TARGET,
        "threshold_text": threshold_text,
        "card_options": [card_view(c) for c in CARD_ORDER],
        "deck_rows": [
            {"card": card, "count": remaining.get(card, 0), "corner": corner_value(card), "color_class": COLOR_CLASS[card]}
            for card in CARD_ORDER
        ],
    }


@app.route("/", methods=["GET", "POST"])
def index():
    state = get_state()

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "reset":
            state = fresh_state()

        elif action == "deal":
            state = fresh_state()
            for _ in range(2):
                card = draw_random_card(state["remaining"])
                if card:
                    state["hand"].append(card)
            state["status"] = "Two face-up cards dealt."

        elif action == "hit" and not state.get("finished", False):
            card = draw_random_card(state["remaining"])
            if card:
                state["hand"].append(card)
                state["status"] = f"You drew {card}."
            else:
                state["status"] = "Deck is empty."

        elif action == "stand" and state["hand"]:
            base, aces = hand_base_and_aces(state["hand"])
            total, bust, _ = best_total(base, aces)
            state["finished"] = True
            state["status"] = "Bust. Final payoff is 0." if bust else f"You stood on {total}. Final payoff is {total}."

        elif action == "add_card" and not state.get("finished", False):
            card = request.form.get("card")
            if card in CARD_ORDER and state["remaining"].get(card, 0) > 0:
                state["remaining"][card] -= 1
                state["hand"].append(card)
                state["status"] = f"Manually added {card}."

        save_state(state)
        return redirect(url_for("index"))

    context = build_context(state)
    save_state(state)
    return render_template("index.html", **context)


@app.template_filter("pct")
def pct(value: float) -> str:
    return f"{100 * value:.2f}%"


@app.template_filter("ev")
def ev(value: float) -> str:
    return f"{value:.3f}"


if __name__ == "__main__":
    app.run(debug=True)
