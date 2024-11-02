import datetime
from Logic.Player import Player
from DataBase.SQLiteManager import SQLiteManager

class Database:
    def __init__(self):
        self.players = SQLiteManager("DataBase/Files/players.sqlite", "PlayerTable")
        self.clubs = SQLiteManager("DataBase/Files/clubs.sqlite", "ClubTable")

        self.data = {
            "Name": "Brawler",
            "Registered": True,
            "Gems": Player.gems,
            "Trophies": Player.trophies,
            "Tickets": Player.tickets,
            "Resources": Player.resources,
            "TokenDoubler": 0,
            "HighestTrophies": 0,
            "TrophyRoadReward": 0,
            "ExperiencePoints": Player.exp_points,
            "ProfileIcon": 0,
            "NameColor": 0,
            "UnlockedBrawlers": Player.brawlers_unlocked,
            "BrawlersTrophies": Player.brawlers_trophies,
            "BrawlersHighestTrophies": Player.brawlers_high_trophies,
            "BrawlersLevel": Player.brawlers_level,
            "BrawlersPowerPoints": Player.brawlers_powerpoints,
            "UnlockedSkins": Player.unlocked_skins,
            "SelectedSkins": Player.selected_skins,
            "SelectedBrawler": 0,
            "Region": Player.region,
            "SupportedContentCreator": Player.content_creator,
            "AccountCreationDate": str(datetime.datetime.now())
        }

    def createPlayerAccount(self, playerID: list, token: str):
        self.players.createEntry(playerID, token, self.data)

    def loadPlayerAccount(self, token: str):
        return self.players.getEntry(token)

    def loadPlayerAccountByID(self, id: list):
        return self.players.getEntryFromID(id)

    def updatePlayerAccount(self, token: str, item, value):
        self.players.updateEntry(item, value, token)

    def deletePlayer(self, token):
        self.players.deleteEntry(token)

    def getAllPlayers(self) -> list:
        return self.players.getAllEntries()

    def loadAllPlayersSorted(self, item: str):
        return self.players.getAllEntriesSorted(item)

    def createClub(self, id, data):
        self.clubs.createEntry(id, data.get("Region", "RO"), data)

    def updateClub(self, id, item, value):
        self.clubs.updateEntry(item, value, id)

    def loadClub(self, id):
        return self.clubs.getEntry(id)

    def loadAllClubsSorted(self, element):
        return self.clubs.getAllEntriesSorted(element)

    def loadAllClubs(self) -> list:
        return self.clubs.getAllEntries()

    def deleteClub(self, id):
        self.clubs.deleteEntry(id)