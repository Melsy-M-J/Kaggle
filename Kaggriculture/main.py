from kaggle_environments import make


def agent(obs):
    # Get our own farm information
    player = obs["player"]
    farm = obs["farms"][player]

    # Farmer coordinates are [x, y], but tiles are indexed [y][x]
    x, y = farm["farmer"]
    tile = farm["tiles"][y][x]

    # Get our stored seeds and harvested wheat
    private = obs["private"]
    wheat_seeds = private["seeds"].get("WHEAT", 0)
    wheat_in_shed = private["shed"].get("WHEAT", 0)

    # Market orders are separate from the farmer's physical action
    market = []

    # Sell harvested wheat stored in the shed
    if wheat_in_shed > 0:
        market.append(["SELL", "WHEAT", wheat_in_shed])

    # Buy a seed only when the current tile is empty
    if tile is None and wheat_seeds == 0 and farm["money"] >= 10:
        market.append(["BUY_SEED", "WHEAT", 1])

        
    # Decide what the farmer should do
    action = ["PASS"]

    inventory = private["inventories"][0]
    x, y = farm["farmer"]

    # The shed is at the center of the board.
    # These four positions are next to it.
    shed_adjacent = (
        (x, y) in [(4, 4), (5, 4), (4, 5), (5, 5)]
    )

    # Deposit harvested goods before doing anything else.
    if inventory and shed_adjacent:
        action = ["DROP"]

    elif tile is None:
        if wheat_seeds > 0:
            action = ["PLANT", "WHEAT"]

    elif isinstance(tile, dict) and tile.get("kind") == "WEED":
        action = ["DIG"]

    elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
        if tile.get("crop") == "WHEAT":
            age = obs["day"] - tile["planted_day"]

            if not tile["watered_today"]:
                action = ["WATER"]

            elif age >= 4:
                action = ["HARVEST"]


    # if tile is None:
    #     if wheat_seeds > 0:
    #         action = ["PLANT", "WHEAT"]

    # elif isinstance(tile, dict) and tile.get("kind") == "WEED":
    #     action = ["DIG"]

    # elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
    #     if tile.get("crop") == "WHEAT":
    #         age = obs["day"] - tile["planted_day"]

    #         # Water first so the crop can reach its best yield
    #         if not tile["watered_today"]:
    #             action = ["WATER"]

    #         # Harvest after four days, once watered that day
    #         elif age >= 4:
    #             action = ["HARVEST"]

    return {
        "farmer": action,
        "hands": [],
        "market": market
    }
