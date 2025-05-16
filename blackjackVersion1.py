
import tkinter as tk
from tkinter import messagebox
import random

# Значения карт
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
    "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
}

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack 21")

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.player_label = tk.Label(self.root, text="Player: []", font=("Helvetica", 14))
        self.player_label.pack(pady=10)

        self.dealer_label = tk.Label(self.root, text="Dealer: []", font=("Helvetica", 14))
        self.dealer_label.pack(pady=10)

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand)
        self.stand_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.reset_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=20)

    def draw_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def hand_value(self, hand):
        value = sum(card_values[card] for card in hand)
        aces = hand.count("A")
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def update_display(self):
        self.player_label.config(text=f"Player: {self.player_hand} ({self.hand_value(self.player_hand)})")
        dealer_display = ["?"] + self.dealer_hand[1:] if not self.stand_pressed else self.dealer_hand
        self.dealer_label.config(
            text=f"Dealer: {dealer_display} ({self.hand_value(self.dealer_hand) if self.stand_pressed else '?'})"
        )

    def new_game(self):
        self.deck = list(card_values.keys()) * 4
        random.shuffle(self.deck)
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.stand_pressed = False
        self.update_display()
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

    def hit(self):
        self.player_hand.append(self.draw_card())
        self.update_display()
        if self.hand_value(self.player_hand) > 21:
            messagebox.showinfo("Result", "You busted! Dealer wins.")
            self.hit_button.config(state="disabled")
            self.stand_button.config(state="disabled")

    def stand(self):
        self.stand_pressed = True
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())
        self.update_display()
        player_score = self.hand_value(self.player_hand)
        dealer_score = self.hand_value(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            result = "You win!"
        elif player_score < dealer_score:
            result = "Dealer wins."
        else:
            result = "It's a tie."

        messagebox.showinfo("Result", result)
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()


