import time
import random

def play_coin_betting_game():
    print("Welcome to the Coin Betting Game!")
    initial_bankroll = 25.0
    
    # Game settings
    num_computers = int(input("Enter number of computer opponents: "))
    time_limit = float(input("Enter time limit in seconds: "))
    profit_target = float(input("Enter profit target (dollars above the initial $25): "))
    
    p = 0.6  
    q = 1 - p
    b = 1.0 
    # Full Kelly fraction
    kelly_fraction = (b * p - q) / b
    
    # Initialize players
    players = {
        "You": {"bankroll": initial_bankroll, "active": True}
    }
    for i in range(num_computers):
        players[f"Computer {i+1}"] = {"bankroll": initial_bankroll, "active": True}
    
    print("\nStarting game...\n")
    start_time = time.time()
    
    # Main game loop
    while time.time() - start_time < time_limit and any(p["active"] for p in players.values()):
        for name, data in players.items():
            # Check time limit
            if time.time() - start_time >= time_limit:
                break
            # Skip inactive players
            if not data["active"]:
                continue
            # Check profit target
            if data["bankroll"] >= initial_bankroll + profit_target:
                data["active"] = False
                continue
            
            print(f"{name}'s turn (Bankroll: ${data['bankroll']:.2f})")
            
            # Determine bet
            if name == "You":
                while True:
                    try:
                        bet = float(input(f"  Enter bet amount (up to ${data['bankroll']:.2f}): "))
                        if 0 < bet <= data["bankroll"]:
                            break
                        else:
                            print("  Invalid bet. Try again.")
                    except ValueError:
                        print("  Please enter a number.")
            else:
                bet = round(data["bankroll"] * kelly_fraction, 2)
                bet = max(min(bet, data["bankroll"]), 0.01)
                print(f"  {name} (Kelly) bets ${bet:.2f}")
            
            # Flip the biased coin
            flip = "heads" if random.random() < 0.6 else "tails"
            print(f"  Coin result: {flip}")
            if flip == "heads":
                data["bankroll"] += bet
                print(f"  {name} wins ${bet:.2f}!")
            else:
                data["bankroll"] -= bet
                print(f"  {name} loses ${bet:.2f}!")
            
            # Check for bankruptcy or reaching target
            if data["bankroll"] <= 0:
                data["active"] = False
                print(f"  {name} is bankrupt and out.")
            elif data["bankroll"] >= initial_bankroll + profit_target:
                data["active"] = False
                print(f"  {name} reached the profit limit and stops betting.")
            
            print()
    
    # Game over, show results
    print("Time's up or all players done!\nFinal results:")
    for name, data in players.items():
        profit = data["bankroll"] - initial_bankroll
        kept = min(profit, profit_target) if profit > 0 else profit
        print(f"  {name}: Bankroll = ${data['bankroll']:.2f}, Profit kept = ${kept:.2f}")
    print("\nThanks for playing!")

if __name__ == "__main__":
    play_coin_betting_game()
