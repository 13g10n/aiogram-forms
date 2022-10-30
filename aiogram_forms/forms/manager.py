from ..core.manager import EntityManager


class FormsManager(EntityManager):

    async def show(self, name: str):
        entity = self.dispatcher._registry[name]
        await entity.show(self.event, self.data['state'])
