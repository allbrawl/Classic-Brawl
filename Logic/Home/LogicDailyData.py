from datetime import datetime, timezone
from Logic.Home.LogicShopData import LogicShopData

class LogicDailyData:

    @staticmethod
    def encode(self):
        UTCNow = datetime.now(timezone.utc)

        self.writeVInt(UTCNow.year * 1000 + UTCNow.timetuple().tm_yday) # Current Year and Day
        self.writeVInt(UTCNow.hour * 3600 + UTCNow.minute * 60 + UTCNow.second) # Time left for the next day

        self.writeVInt(self.player.trophies) # Player Trophies
        self.writeVInt(self.player.high_trophies) # Player Highest Trophies
        self.writeVInt(0) # Player Daily High Trophies

        self.writeVInt(self.player.trophy_reward) # Trophy Road Rewards Collected
        self.writeVInt(self.player.exp_points) # Player Experience Points

        self.writeDataReference(28, self.player.profile_icon) # Player Profile Icon
        self.writeDataReference(43, self.player.name_color) # Player Name Color

        self.writeIntList([]) # Played Gamemodes

        self.writeVInt(len(self.player.selected_skins)) # Selected Characters Skins
        for x in self.player.selected_skins:
            self.writeDataReference(29, self.player.selected_skins[x])

        self.writeVInt(len(self.player.unlocked_skins)) # Unlocked Skins
        for x in self.player.unlocked_skins:
            self.writeDataReference(29, x)

        self.writeVInt(0)  # Unknown Array
        for x in range(0):
            self.writeDataReference(0, 0)

        self.writeVInt(0) # Leaderboard Default Region
        self.writeVInt(self.player.high_trophies) # Trophy Road Highest Icon Reached
        self.writeVInt(0) # Tokens used in Battles

        self.writeUInt8(0) # Token Limit Reached
        self.writeVInt(0) # Control Mode (Unused, 2017 feature)
        self.writeUInt8(0)

        self.writeVInt(self.player.token_doubler) # Token Doublers left
        self.writeVInt(99999) # Trophy Road Timer
        self.writeVInt(99999) # Power Play Timer
        self.writeVInt(99999) # Brawl Pass Timer

        self.writeVInt(0) # ForcedDrops::encode

        self.writeBoolean(False) # TimedOffer::encode 1?
        self.writeBoolean(False) # TimedOffer::encode 2?

        self.writeUInt8(8) # Shop Token Doubler State

        self.writeVInt(2) # Unknown
        self.writeVInt(2) # Unknown
        self.writeVInt(2) # Unknown

        self.writeVInt(0) # Name Change Cost
        self.writeVInt(0) # Name Change Timer

        LogicShopData.encodeShopOffers(self)

        self.writeVInt(0) # AdStatus::encode

        self.writeVInt(200) # Available Battle Tokens
        self.writeVInt(0) # Time till Tokens refill (20)

        self.writeIntList([]) # Tickets Purchased Index

        self.writeVInt(self.player.tickets) # Player Tickets Amount
        self.writeVInt(0) # Unknown

        self.writeDataReference(16, self.player.home_brawler) # Selected Character

        self.writeString(self.player.region) # Player Region
        self.writeString(self.player.content_creator) # Supported Content Creator

        self.writeVInt(0) # IntValueEntry::encode
        for x in range(0):
            self.writeInt(0)
            self.writeInt(0)

        self.writeVInt(0) # CooldownEntry::encode
        for x in range(0):
            self.writeVInt(0)
            self.writeDataReference(0, 0) # Item Locked
            self.writeVInt(0)

        self.writeVInt(0) # BrawlPassSeasonData::encode
        for x in range(0):
            pass

        self.writeVInt(0) # ProLeagueSeasonData::encode
        for x in range(0):
            self.writeVInt(0)
            self.writeVInt(0)

        self.writeBoolean(True) # LogicQuests::encode
        self.writeVInt(0) # Quests Count




