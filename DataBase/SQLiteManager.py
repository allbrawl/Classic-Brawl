import sqlite3
import json
import traceback
from Utils.Helpers import Helpers

class SQLiteManager:
	def __init__(self, databaseName: str, tableName: str):
		self.connection = sqlite3.connect(databaseName)
		self.tableName = tableName
		self.cursor = self.connection.cursor()
        
		self.primaryKeys = ("HighID", "LowID") if tableName == "ClubTable" else ("Authentication",)
		columns = "HighID INTEGER, LowID INTEGER, Region TEXT, Data JSON" if tableName == "ClubTable" else "HighID INTEGER, LowID INTEGER, Authentication TEXT, Data JSON"
		try:
			self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName.upper()} ({columns})")
		except sqlite3.OperationalError:
			print(f"{Helpers.red}Unable to initialize {tableName} table:\n{traceback.format_exc()}{Helpers.reset}")

	def createEntry(self, ids, key: str, data):
		try:
			if not isinstance(ids, tuple):
				ids = (ids,)
			values = (0, *ids, key, json.dumps(data))
			placeholders = ', '.join(['?'] * len(values))
			self.cursor.execute(f"INSERT INTO {self.tableName} VALUES ({placeholders})", values)
			self.connection.commit()
		except Exception:
			traceback.print_exc()

	def updateEntry(self, item, value, key: str):
		try:
			entry = self.getEntry(key)
			if not entry:
				raise sqlite3.Error(f"Entry with key {key} not found in {self.tableName}")
			if isinstance(item, list):
				for i, enuItem in enumerate(item):
					entry[enuItem] = value[i]
			else:
				entry[item] = value
			self.cursor.execute(f"UPDATE {self.tableName} SET Data = ? WHERE {self.primaryKeys[0]} = ?", (json.dumps(entry), key))
			self.connection.commit()
		except Exception:
			traceback.print_exc()

	def getEntry(self, key: str):
		try:
			query = f"SELECT Data FROM {self.tableName} WHERE {self.primaryKeys[0]} = ?"
			if len(self.primaryKeys) > 1:
				query += f" AND {self.primaryKeys[1]} = ?"
			self.cursor.execute(query, (key,))
			result = self.cursor.fetchone()
			return json.loads(result[0]) if result else None
		except Exception:
			traceback.print_exc()

	def getAllEntries(self) -> list:
		try:
			entries = []
			self.cursor.execute(f"SELECT * FROM {self.tableName}")
			fetched = self.cursor.fetchall()
			for entry in fetched:
				entries.append(json.loads(entry[3]))
			return entries
		except Exception:
			traceback.print_exc()

	def getAllEntriesSorted(self, item: str) -> list:
		try:
			return sorted(self.getAllEntries(), key=lambda x: x.get(item), reverse=True)
		except Exception:
			traceback.print_exc()

	def getEntryFromID(self, id: list):
		try:
			self.cursor.execute(f"SELECT Data FROM {self.tableName} WHERE HighID = ? AND LowID = ? LIMIT 1", (*id,))
			result = self.cursor.fetchone()
			return json.loads(result[0]) if result else None
		except Exception:
			traceback.print_exc()

	def deleteEntry(self, key: str):
		try:
			self.cursor.execute(f"DELETE FROM {self.tableName} WHERE {self.primaryKeys[0]} = ?", (key,))
			self.connection.commit()
		except Exception:
			traceback.print_exc()

	def closeConnection(self):
		try:
			self.connection.close()
		except Exception:
			print(f"[SQLiteManager::] Unable to close {self.tableName} connection:\n{traceback.format_exc()}")
