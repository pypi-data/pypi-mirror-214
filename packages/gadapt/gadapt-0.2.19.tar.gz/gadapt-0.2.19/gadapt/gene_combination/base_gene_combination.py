from ast import Tuple
from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.gene import Gene
import gadapt.ga_model.definitions as definitions

class BaseGeneCombination:

    """
    Base class for gene combination
    """

    def combine(self, mother_gene: Gene, father_gene: Gene):
        raise Exception(definitions.NOT_IMPLEMENTED)