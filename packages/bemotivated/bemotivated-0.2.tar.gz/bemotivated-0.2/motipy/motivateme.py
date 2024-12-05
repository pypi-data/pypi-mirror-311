import random

motivational_sentences = [
    "Believe in yourself and all that you are.",
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Your time is limited, so don't waste it living someone else's life.",
    "Hardships often prepare ordinary people for an extraordinary destiny.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Don’t watch the clock; do what it does. Keep going.",
    "You are never too old to set another goal or to dream a new dream.",
    "Success usually comes to those who are too busy to be looking for it.",
    "The way to get started is to quit talking and begin doing.",
    "Dream big and dare to fail.",
    "What you get by achieving your goals is not as important as what you become by achieving your goals.",
    "Act as if what you do makes a difference. It does.",
    "The only way to do great work is to love what you do.",
    "You miss 100% of the shots you don’t take.",
    "Keep your face always toward the sunshine—and shadows will fall behind you.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Failure is simply the opportunity to begin again, this time more intelligently.",
    "If you want to lift yourself up, lift up someone else.",
    "The only person you are destined to become is the person you decide to be."
]

def give_me_energy():
    print(random.choice(motivational_sentences))
