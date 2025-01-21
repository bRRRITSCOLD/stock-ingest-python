import dotenv

class Environment:
    config: dict[str, str | None]    

    def load(self):
        self.config = dotenv.dotenv_values(".env")

    @property
    def POLYGON_API_KEY(self):
        return self.config.get('POLYGON_API_KEY')

env = Environment()
