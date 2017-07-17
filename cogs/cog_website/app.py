"""Partially based on the example of Kyoukai's GitHub repo README.md, solely for testing right now."""
import kyoukai

blueprint = kyoukai.Blueprint("blueprint")


class Site(kyoukai.Kyoukai):
    def __init__(self, bot, name: str="website_cog", ip: str="127.0.0.1", port: int=4444):
        super().__init__(name)
        self.register_blueprint(blueprint)

    @blueprint.route("/")
    async def index(ctx: kyoukai.HTTPRequestContext):
        return "Hi"


# Made for internal testing.
if __name__ == "__main__":
    # Port 22 confirmed in use on my Windows PC
    Site("placeholder").run()
