# 26S6G Blackjack 16 Lab (Qian Yi, Kar Roong, Tze Thal)

A Flask and Jinja web app for a simplified single-player blackjack investigation.

The player draws from a 32-card deck and tries to maximise final score without exceeding 16. There is no dealer. The app calculates the current total, one-hit bust odds, expected value of hitting, expected value of standing, and the mathematically recommended move.

## Game rules

The deck has 32 cards.

| Card | Copies | Value |
| --- | ---: | ---: |
| A | 4 | 1 or 6, whichever is more favourable |
| 2 | 4 | 2 |
| 3 | 4 | 3 |
| 4 | 4 | 4 |
| 5 | 4 | 5 |
| J | 4 | 5 |
| Q | 4 | 5 |
| K | 4 | 5 |

The target is 16. If the best possible total exceeds 16, the player busts and the payoff is 0. Otherwise, standing gives payoff equal to the current total.

## Mathematical model

The app uses exact drawing without replacement from the remaining deck.

Standing value

```text
EV(stand) = current total
```

Hitting value

```text
EV(hit) = sum over remaining card types of P(card) * V(new state)
```

Optimal recursive value

```text
V(state) = max(EV(stand), EV(hit))
```

This matches the research conclusion that the broad threshold is to hit below 12 and stand on 12 or above. The app still recomputes the exact value from the live remaining deck after every drawn or manually added card.

## Running locally
Install dependencies and run the app on browser `http://127.0.0.1:5000`

```bash
pip install -r requirements.txt
python app.py
```

## Files

```text
app.py                  Flask backend and probability engine
templates/index.html    Jinja page template
static/styles.css       Frontend styling
requirements.txt        Python dependencies
README.md               Project instructions
```