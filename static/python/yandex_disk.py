

disk = yadisk.YaDisk(token='AQAAAABAnEzFAAe8DKWJh_F-AEeRmOR1ZPKKXzc')


class Upload:
    def __init__(self, filename, path):
        try:
            disk.upload(filename, f"/Site-avatars/{path}")
            print(filename, path)
            print('ok')

        except:
            print('not ok')
