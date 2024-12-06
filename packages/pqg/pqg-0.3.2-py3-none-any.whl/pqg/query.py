import typing as t

from .group_by_aggregation import GroupByAggregation
from .merge import Merge
from .operation import Operation
from .projection import Projection
from .selection import Selection


class Query:
  """
  Represents a complete database query with tracking for query complexity.

  A query consists of a target entity and a sequence of operations to be
  applied to that entity. Query complexity is determined primarily by the
  number of merge operations and their nesting depth.

  Attributes:
    entity (str): The name of the target entity.
    operations (List[Operation]): List of operations to apply.
    multi_line (bool): Whether to format output across multiple lines.
    columns (Set[str]): Columns available for operations.
  """

  def __init__(
    self,
    entity: str,
    operations: t.List[Operation],
    multi_line: bool,
    columns: t.Set[str],
  ):
    self.entity = entity
    self.operations = operations
    self.multi_line = multi_line
    self.columns = columns

  def __str__(self) -> str:
    return (
      self.format_multi_line()[0]
      if self.multi_line
      else f'{self.entity}{''.join(op.apply(self.entity) for op in self.operations)}'
    )

  def __hash__(self) -> int:
    """Hash based on complexity and string representation."""
    return hash((self.complexity, str(self)))

  def __eq__(self, other: object) -> bool:
    """Equality comparison based on complexity and string representation."""
    if not isinstance(other, Query):
      return NotImplemented
    return (self.complexity, str(self)) == (other.complexity, str(other))

  def __lt__(self, other: object) -> bool:
    """Less than comparison based on complexity and string representation."""
    if not isinstance(other, Query):
      return NotImplemented
    return (self.complexity, str(self)) < (other.complexity, str(other))

  @property
  def complexity(self) -> int:
    """
    Calculate query complexity based on all operations and their details.

    Complexity is determined by:
    1. Base complexity: Total number of operations
    2. Merge complexity:
     - Each merge adds weight of 3 (more complex than other operations)
     - Additional complexity from nested queries
    3. Selection complexity: Number of conditions in each selection
    4. Projection complexity: Number of columns being projected
    5. GroupBy complexity: Number of grouping columns plus weight of aggregation

    Returns:
      int: Complexity score for the query
    """

    def get_merge_complexity(op: Operation) -> int:
      return (
        3 + sum(get_operation_complexity(nested_op) for nested_op in op.right.operations)
        if isinstance(op, Merge)
        else 0
      )

    def get_operation_complexity(op: Operation) -> int:
      if isinstance(op, Selection):
        return 1 + len(op.conditions)
      elif isinstance(op, Projection):
        return 1 + len(op.columns)
      elif isinstance(op, GroupByAggregation):
        return 2 + len(op.group_by_columns)
      elif isinstance(op, Merge):
        return get_merge_complexity(op)
      raise ValueError('Unsupported operation type')

    base_complexity = len(self.operations)

    operation_complexity = sum(get_operation_complexity(op) for op in self.operations)

    return base_complexity + operation_complexity

  @property
  def merge_count(self) -> int:
    """
    Count the total number of merge operations in the query, including nested merges.

    Returns:
      int: Total number of merge operations
    """
    return sum(
      1 + sum(1 for nested_op in op.right.operations if isinstance(nested_op, Merge))
      if isinstance(op, Merge)
      else 0
      for op in self.operations
    )

  @property
  def merge_entities(self) -> t.Set[str]:
    """
    Get the set of all entities involved in this query, including
    the base entity and all merged entities.

    This property maintains a complete picture of table dependencies by tracking:
    1. The base entity of the query
    2. All entities that have been merged directly into this query
    3. All entities that have been merged into sub-queries (nested merges)

    The tracking helps prevent:
    - Circular dependencies (e.g., orders → customers → orders)
    - Redundant joins (e.g., merging the same table multiple times)
    - Invalid join paths

    Returns:
      Set[str]:
        A set of entity names (table names) that are part of this query's join graph.
        Includes both the base entity and all merged entities.
    """
    merged = {self.entity}

    for op in self.operations:
      if isinstance(op, Merge):
        merged.update(op.entities)

    return merged

  def format_multi_line(self, start_counter: int = 1) -> t.Tuple[str, int]:
    """
    Format the query across multiple lines for better readability.

    Transforms the query into a sequence of DataFrame operations where each
    operation is assigned to a numbered DataFrame variable (df1, df2, etc.).
    Handles nested operations by recursively formatting sub-queries and
    maintaining proper DataFrame references.

    Args:
      start_counter (int): Initial counter value for DataFrame numbering. Defaults to 1.

    Returns:
      Tuple[str, int]: A tuple containing:
          - The formatted multi-line query string
          - The final counter value after processing all operations

    Example:
      For a query with multiple operations, might return:
      ("df1 = customer[customer['age'] >= 25]\n"
       "df2 = df1.merge(orders, left_on='id', right_on='customer_id')",
       3)
    """
    lines, df_counter, current_df = [], start_counter, self.entity

    for op in self.operations:
      if isinstance(op, (Selection, Projection, GroupByAggregation)):
        lines.append(f'df{df_counter} = {current_df}{op.apply(current_df)}')
        current_df = f'df{df_counter}'
        df_counter += 1
      elif isinstance(op, Merge):
        right_statements, right_final_counter = op.right.format_multi_line(df_counter)

        if right_statements:
          lines.extend(right_statements.split('\n'))

        right_df = f'df{right_final_counter-1}'

        lines.append(
          f'df{right_final_counter} = {current_df}.merge({right_df}, '
          f'left_on={op.left_on}, right_on={op.right_on})'
        )

        current_df, df_counter = f'df{right_final_counter}', right_final_counter + 1

    return '\n'.join(lines), df_counter
