from src.win007.modules.games_fetcher.basketball_odds_fetcher.game_info_and_all_odds_sequence import GameInfoAndAllOddsSequence

bids = {
        265: "macau_slot",  # Macao Slot
        26: "will_hill",  # WH
        214: "bet365",  # Bet365
        17: "pinnacle",  # Pinnacle
        # 432: "hkjc",  # HKJC
        82:  "vcbet", # VcBet
        3: "interwetten" # Interwetten
    }
odds_fetcher = GameInfoAndAllOddsSequence(bids)
print(odds_fetcher.get_odds(235974))