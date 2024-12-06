from dataclasses import dataclass

from .arguments import Arguments


@dataclass
class QueryStructure:
  """
  A dataclass that encapsulates the configuration parameters controlling query generation.
  Contains settings for various query features like aggregation, projection, and merging.
  """

  groupby_aggregation_probability: float
  max_groupby_columns: int
  max_merges: int
  max_projection_columns: int
  max_selection_conditions: int
  projection_probability: float
  selection_probability: float

  @staticmethod
  def from_args(arguments: Arguments) -> 'QueryStructure':
    """
    Create a QueryStructure instance from command-line arguments.

    Args:
      arguments: Instance of Arguments containing parsed command-line parameters

    Returns:
      QueryStructure: Instance configured according to the provided arguments
    """
    return QueryStructure(
      groupby_aggregation_probability=arguments.groupby_aggregation_probability,
      max_groupby_columns=arguments.max_groupby_columns,
      max_merges=arguments.max_merges,
      max_projection_columns=arguments.max_projection_columns,
      max_selection_conditions=arguments.max_selection_conditions,
      projection_probability=arguments.projection_probability,
      selection_probability=arguments.selection_probability,
    )
