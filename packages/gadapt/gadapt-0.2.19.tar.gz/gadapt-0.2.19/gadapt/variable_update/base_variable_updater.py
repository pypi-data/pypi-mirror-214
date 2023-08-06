import gadapt.ga_model.definitions as definitions
class BaseVariableUpdater:

    """
    Base class for variable update
    """

    def update_variables(self, population):
        raise Exception(definitions.NOT_IMPLEMENTED)