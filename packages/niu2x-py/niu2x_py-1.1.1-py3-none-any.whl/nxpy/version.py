class Version:
    def __init__(self, major, minor, patch):
        self.major_ = major
        self.minor_ = minor
        self.patch_ = patch

    def __str__(self):
        return f'{self.major_}.{self.minor_}.{self.patch_}'


version = Version(1, 1, 1)
