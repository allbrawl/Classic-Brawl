import requests, sys, time, os, hashlib
from ByteStream.Writer import Writer
from ByteStream.Reader import Reader

class Updater:
    """A class dedicated to updating your Classic Brawl server to the latest version with ease."""

    def __init__(self, shouldStartUpdating: bool = True):
        """Initializes the Updater class and starts the update check sequence."""
        if shouldStartUpdating: self.checkForUpdates()

    def writeUpdateFile(self, fileVersion: int, repoVersion: str, files: list):
        """Writes the data for the update file that the upgrader uses.

        Parameters:
            fileVersion (int): The version of the file that the reader will use
            repoVersion (str): The version of the repository (each update will have a version number)
            files (list): A list of the files location that were updated
        """
        byteStream = Writer(None)
        byteStream.writeInt(fileVersion, 1)
        byteStream.writeString(repoVersion)

        byteStream.writeInt(len(files), 2)
        for file in files:
            byteStream.writeString(file)

        with open("Logic/version.cb", "wb+") as classicFile:
            classicFile.seek(0)
            classicFile.write(byteStream.buffer)
            classicFile.flush()
            classicFile.close()

        print("Update file has been written successfully!")

    def readUpdateFileFromGitHub(self):
        updateFile = requests.get("https://raw.githubusercontent.com/PhoenixFire6934/Classic-Brawl/master/Logic/version.cb")
        headerData = {}

        if updateFile.status_code == 200:
            reader = Reader(updateFile.content)
            headerData["fV"] = reader.readInt(1) # File Version
            headerData["rV"] = reader.readString() # Repository Version

            headerData["fC"] = reader.readInt(2) # Files Count
            headerData["f"] = []
            for x in range(headerData["fC"]):
                headerData["f"].append(reader.readString())
        else:
            print(f"Unable to retrieve update file from GitHub! Request Status Code: {updateFile.status_code}")

        return headerData

    def readUpdateFile(self, debugOutput: bool = False):
        """Reads the update file written and compares it with the one in the Classic Brawl repository.

        Parameters:
            debugOutput (bool): Whether to output the header as a print in the console. False by default.
        """
        headerData = {}
        with open("Logic/version.cb", "rb") as classicFile:
            classicFile.seek(0)
            reader = Reader(classicFile.read())
            headerData["fV"] = reader.readInt(1)  # File Version
            headerData["rV"] = reader.readString()  # Repository Version

            headerData["fC"] = reader.readInt(2)  # Files Count
            headerData["f"] = []
            for x in range(headerData["fC"]):
                headerData["f"].append(reader.readString())

            classicFile.close()

        return headerData

    def formatSize(self, fileSize: int):
        """Formats the file size to a readable string (B, KB)"""
        if fileSize < 1024: return f"{fileSize} B"
        elif fileSize < 1024 * 1024: return f"{fileSize / 1024:.2f} KB"

        return f"{fileSize} B"

    def getRecommendedChunkSize(self, fileSize: int):
        """Return a suitable chunk size based on the file size to improve efficiency and download speeds."""
        if fileSize < 1024 * 1024:
            return 4096  # 4 KB
        elif fileSize < 5 * 1024 * 1024:
            return 8192  # 8 KB
        else:
            return 16384  # 16 KB

    def getHash(self, filePath: str):
        """Helper function to calculate the hashFile of a file"""
        hashFile = hashlib.new("sha256")

        with open(filePath, 'rb') as f:
            while chunk := f.read(8192):
                hashFile.update(chunk)

        return hashFile.hexdigest()

    def downloadFiles(self, files: list):
        """Downloads a list of files from the Classic Brawl repository.

        Parameters:
            files (list): A list containing strings leading to the directory of the updated file
        """
        print("Files to download: " + str(len(files)))
        coolSpinningAnimation = ['|', '/', '-', '\\'] # ASCII Characters
        downloadedBytes: bytes = b""
        fileHash = hashlib.sha256()
        localHash = hashlib.sha256().hexdigest()

        for file in files:
            retrieved = requests.get("https://raw.githubusercontent.com/PhoenixFire6934/Classic-Brawl/master/" + file, stream=True) # stream=True splits into chunks in case of "big" files
            fileName = os.path.basename(file)
            if retrieved.status_code != 200:
                print(f"Unable to download {fileName}. Continuing..")
                continue

            destination: str = file
            fileSize: int = int(retrieved.headers.get("Content-Length", 0))
            if os.path.exists(destination): localHash = self.getHash(destination)
            formattedSize: str = self.formatSize(fileSize)

            with open(destination, mode="w", encoding="utf-8") as updated: # Open the file in write mode
                updated.seek(0)
                spinnerLast = time.time()

                for chunk in retrieved.iter_content(chunk_size = self.getRecommendedChunkSize(fileSize)):
                    if not chunk: continue
                    fileHash.update(chunk)
                    downloadedBytes += chunk

                    # Show progress with the cool-looking spinner
                    if time.time() - spinnerLast:
                        sys.stdout.write(f"\rDownloading {fileName}... {coolSpinningAnimation[len(downloadedBytes) % len(coolSpinningAnimation)]} "
                                         f"({self.formatSize(len(downloadedBytes))}/{formattedSize})")
                        sys.stdout.flush() # ensure its written
                        spinnerLast = time.time()

                if fileHash and localHash == fileHash.hexdigest():
                    sys.stdout.write(f"File {fileName} is already up-to-date")
                else:
                    updated.write(downloadedBytes.decode('utf-8'))
                    updated.flush()
                    sys.stdout.write(f"\rDownloading {fileName}.. Done!\n")

                if not os.path.exists("Logic/Hashes/"): os.makedirs("Logic/Hashes/")
                file = open(f"Logic/Hashes/{fileName}.hash", "w+")
                file.seek(0)
                file.write(fileHash.hexdigest())
                file.flush()
                file.close()

                localHash = hashlib.sha256().hexdigest() # change back (im losing track of what im doing...)
                updated.close()
                downloadedBytes = b""
                sys.stdout.flush() # same story

    def checkForUpdates(self):
        """Checks for updates and upgrades if needed."""
        try:
            print("Checking for updates...\nYou can disable this feature by changing 'UpgradesEnabled' from true to false in config.json\n")
            localFile: dict = self.readUpdateFile()
            gitHubFile: dict = self.readUpdateFileFromGitHub()
            if gitHubFile == {}: raise Exception("GitHub update data is null/empty. Are you sure you're connected to the Internet?")

            if localFile.get("rV") == gitHubFile.get("rV"): # Compare versions
                print("Your server is up-to-date with the latest version of Classic Brawl! Continuing startup sequence...")
            else:
                shouldUpdate: bool = "yes" in input(f"An update is available (Remote: {gitHubFile.get('rV')}, Local: {localFile['rV']})! (WARNING: This will update your changes to a file that is in the update file!) Would you like to update? (yes or no)? ").lower()
                if shouldUpdate: self.downloadFiles(gitHubFile.get('f'))
                self.writeUpdateFile(gitHubFile.get("fV"), gitHubFile.get("rV"), gitHubFile.get("f")) # Update to the newest version from git
                print("Update has been completed. Your Classic Brawl server is up-to-date!\nContinuing startup sequence..")

        except Exception as e:
            print(f"Unable to perform an update. Error: {e}\nContinuing startup sequence...")