import pathlib
from typing import List, Tuple

import pytest

from pqg.generator import GenerateOptions, Generator
from pqg.query_structure import QueryStructure
from pqg.schema import Schema

EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / 'examples'


def find_schema_files() -> List[Tuple[str, pathlib.Path]]:
  schema_files = []

  for example_dir in EXAMPLES_DIR.iterdir():
    if example_dir.is_dir():
      schema_file = example_dir / 'schema.json'
      if schema_file.exists():
        schema_files.append((example_dir.name, schema_file))

  return schema_files


@pytest.fixture(params=find_schema_files(), ids=lambda x: x[0])
def schema_fixture(request) -> Tuple[str, Schema]:
  example_name, schema_file = request.param
  return example_name, Schema.from_file(str(schema_file))


@pytest.fixture
def query_structure() -> QueryStructure:
  return QueryStructure(
    groupby_aggregation_probability=0.3,
    max_groupby_columns=3,
    max_merges=10,
    max_projection_columns=5,
    max_selection_conditions=10,
    projection_probability=0.7,
    selection_probability=0.7,
  )


def test_schema_query_generation_and_execution(
  schema_fixture: Tuple[str, Schema], query_structure: QueryStructure
):
  example_name, schema = schema_fixture

  generator = Generator(schema, query_structure)

  query_pool = generator.generate(GenerateOptions(num_queries=100))

  non_empty_results = 0

  for query, (result, error) in query_pool.items():
    assert (
      error is None
    ), f'Single-line query execution failed with error: {error}\nQuery: {str(query)}'

    assert result is not None, f'Single-line query produced None result\nQuery: {str(query)}'

    if not result.empty:
      non_empty_results += 1

    assert hasattr(result, 'empty'), f'Result is neither DataFrame nor Series: {type(result)}'

  min_non_empty_ratio = 0.3

  actual_ratio = non_empty_results / len(query_pool)

  assert actual_ratio >= min_non_empty_ratio, (
    f'Too few non-empty results in {example_name} schema. '
    f'Expected at least {min_non_empty_ratio:.1%}, got {actual_ratio:.1%}'
  )
