class Registry:
    TYPES = {}
    _AUDIO = ['.aif', '.cda', '.mid', '.midi',
              '.mp3', '.mpa', '.ogg', '.wav', '.wma']
    _PACKAGES = ['.deb', '.pkg', '.rpm']
    _COMPRESSED = ['.gz', '.rar', '.z', '.zip', '.7z', '.arj']
    _DISK_IMG = ['.dmg', '.iso', '.toast']
    _IMAGES = ['.ai', '.bmp', '.gif', '.ico', '.jpg']

    def load():
        for ext in Registry._AUDIO:
            Registry.TYPES[ext] = 'Audio'
        for ext in Registry._PACKAGES:
            Registry.TYPES[ext] = 'Package'
        for ext in Registry._COMPRESSED:
            Registry.TYPES[ext] = 'Compressed'
        for ext in Registry._DISK_IMG:
            Registry.TYPES[ext] = 'Disk Image'
        for ext in Registry._IMAGES:
            Registry.TYPES[ext] = 'Image'
