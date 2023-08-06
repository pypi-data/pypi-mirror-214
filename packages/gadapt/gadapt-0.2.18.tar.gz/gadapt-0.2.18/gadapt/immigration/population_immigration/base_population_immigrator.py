import gadapt.ga_model.definitions as definitions
class BasePopulationImmigrator:

    """
    Base class for population immigration
    """

    def immigrate(self, population):
        raise Exception(definitions.NOT_IMPLEMENTED)