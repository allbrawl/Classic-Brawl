from Core.Networking.Server import Server
import json # meh

from Utils.Updater import Updater


def main():
    if json.loads(open("config.json", "r").read())["UpgradesEnabled"]: Updater() # Execute deadly weapons

    print(r"""
   ________                _         ____                      __
  / ____/ /___ ___________(_)____   / __ )_________ __      __/ /
 / /   / / __ `/ ___/ ___/ / ___/  / __  / ___/ __ `/ | /| / / / 
/ /___/ / /_/ (__  |__  ) / /__   / /_/ / /  / /_/ /| |/ |/ / /  
\____/_/\__,_/____/____/_/\___/  /_____/_/   \__,_/ |__/|__/_/   
                                                                 
    """)

    Server("0.0.0.0", 9339).start()


if __name__ == '__main__':
    main()
