
from kaggle_environments import make
from main import agent

env = make(
    "kaggriculture",
    configuration={"episodeSteps": 720}
)

env.run([agent, "random"])

final = env.steps[-1]

for i, player in enumerate(final):
    print(f"\nPlayer {i}")
    print("Reward:", player.reward)
    print("Status:", player.status)

    obs = player.observation
    if obs and "farms" in obs:
        print("Money:", obs["farms"][i].get("money"))

        if i == 0:
            print("Shed inventory:", obs["private"].get("shed"))
            print("Farmer inventory:", obs["private"].get("inventories"))
