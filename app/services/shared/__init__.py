from app.model.entity import Context
from app.providers import Providers


class ServicesShared:
    def __init__(self, context: Context, providers: Providers) -> None:
        self.ctx = context
        self.pvd = providers

    def do_sth(self):
        res = self.pvd.user.get_user_by_name("SimplyLab")
        return None
