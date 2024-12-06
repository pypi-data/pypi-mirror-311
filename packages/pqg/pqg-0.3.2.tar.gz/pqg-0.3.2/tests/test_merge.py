import pytest

from pqg.merge import Merge
from pqg.projection import Projection
from pqg.query import Query
from pqg.selection import Selection


@pytest.fixture
def simple_selection():
  return Selection([("'age'", '>=', 25, '&'), ("'status'", '==', "'active'", None)])


@pytest.fixture
def simple_projection():
  return Projection(['name', 'age', 'email'])


@pytest.fixture
def simple_merge(simple_selection):
  nested_query = Query('orders', [simple_selection], False, {'age', 'status'})
  return Merge(nested_query, "'customer_id'", "'customer_id'")


@pytest.fixture
def multi_column_projection():
  return Projection(['order_id', 'customer_id', 'total', 'status'])


class TestMerge:
  def test_simple_merge(self, simple_merge):
    expected = (
      ".merge(orders[(orders['age'] >= 25) & (orders['status'] == 'active')], "
      "left_on='customer_id', right_on='customer_id')"
    )

    assert simple_merge.apply('customer') == expected

  def test_merge_with_complex_right_query(self, simple_projection):
    nested_query = Query('orders', [simple_projection], False, {'name', 'age', 'email'})

    merge = Merge(nested_query, "'customer_id'", "'order_id'")

    expected = (
      ".merge(orders[['name', 'age', 'email']], " "left_on='customer_id', right_on='order_id')"
    )

    assert merge.apply('customer') == expected

  def test_merge_with_multiple_operations(self, simple_selection, simple_projection):
    nested_query = Query(
      'orders', [simple_selection, simple_projection], False, {'name', 'age', 'email', 'status'}
    )

    merge = Merge(nested_query, "'customer_id'", "'order_id'")

    expected = (
      ".merge(orders[(orders['age'] >= 25) & (orders['status'] == 'active')]"
      "[['name', 'age', 'email']], "
      "left_on='customer_id', right_on='order_id')"
    )

    assert merge.apply('customer') == expected

  def test_nested_merges(self, simple_selection):
    innermost_query = Query('items', [simple_selection], False, {'age', 'status'})

    inner_merge = Merge(innermost_query, "'order_id'", "'item_id'")

    middle_query = Query('orders', [inner_merge], False, {'order_id', 'item_id'})

    outer_merge = Merge(middle_query, "'customer_id'", "'order_id'")

    expected = (
      ".merge(orders.merge(items[(items['age'] >= 25) & "
      "(items['status'] == 'active')], "
      "left_on='order_id', right_on='item_id'), "
      "left_on='customer_id', right_on='order_id')"
    )

    assert outer_merge.apply('customer') == expected

  def test_merge_with_empty_right_query(self):
    right_query = Query('orders', [], False, set())
    merge = Merge(right_query, "'customer_id'", "'order_id'")
    expected = ".merge(orders, left_on='customer_id', right_on='order_id')"
    assert merge.apply('customer') == expected

  def test_merge_with_list_join_columns(self):
    right_query = Query('orders', [], False, set())

    merge = Merge(
      right_query, "['customer_id', 'region_id']", "['order_customer_id', 'order_region_id']"
    )

    expected = (
      '.merge(orders, '
      "left_on=['customer_id', 'region_id'], "
      "right_on=['order_customer_id', 'order_region_id'])"
    )

    assert merge.apply('customer') == expected

  def test_merge_chain(self, simple_projection, multi_column_projection):
    items_query = Query('items', [simple_projection], False, {'name', 'age', 'email'})

    orders_query = Query(
      'orders', [multi_column_projection], False, {'order_id', 'customer_id', 'total', 'status'}
    )

    first_merge = Merge(items_query, "'customer_id'", "'customer_id'")
    second_merge = Merge(orders_query, "'order_id'", "'order_id'")

    final_query = Query('customer', [first_merge, second_merge], False, {'customer_id', 'order_id'})

    expected = (
      'customer'
      ".merge(items[['name', 'age', 'email']], "
      "left_on='customer_id', right_on='customer_id')"
      ".merge(orders[['order_id', 'customer_id', 'total', 'status']], "
      "left_on='order_id', right_on='order_id')"
    )

    assert str(final_query) == expected

  def test_merge_with_quoted_column_names(self):
    right_query = Query('orders', [], False, set())

    merge = Merge(right_query, "'customer_id'", "'order_id'")

    expected = ".merge(orders, left_on='customer_id', right_on='order_id')"

    assert merge.apply('customer') == expected

  def test_merge_with_complex_selections(self):
    conditions = [
      ("'age'", '>=', 25, '&'),
      ("'status'", '.isin', "['active', 'pending']", '&'),
      ("'name'", '.str.startswith', "'A'", None),
    ]

    right_query = Query('orders', [Selection(conditions)], False, {'age', 'status', 'name'})

    merge = Merge(right_query, "'customer_id'", "'order_id'")

    expected = (
      ".merge(orders[(orders['age'] >= 25) & "
      "(orders['status'].isin(['active', 'pending'])) & "
      "(orders['name'].str.startswith('A'))], "
      "left_on='customer_id', right_on='order_id')"
    )

    assert merge.apply('customer') == expected

  def test_merge_complexity_inheritance(self):
    inner_query = Query('orders', [], False, set())

    middle_query = Query(
      'products', [Merge(inner_query, "'order_id'", "'order_id'")], False, {'order_id'}
    )

    outer_query = Query(
      'customer', [Merge(middle_query, "'product_id'", "'product_id'")], False, {'product_id'}
    )

    assert outer_query.complexity == 7

  def test_merge_entities_property(self):
    simple_query = Query('orders', [], False, set())

    simple_merge = Merge(simple_query, "'customer_id'", "'order_id'")

    assert simple_merge.entities == {'orders'}

    nested_ops_query = Query(
      'orders', [Selection([("'status'", '==', "'active'", None)])], False, {'status'}
    )
    nested_ops_merge = Merge(nested_ops_query, "'customer_id'", "'order_id'")

    assert nested_ops_merge.entities == {'orders'}

    items_query = Query('items', [], False, set())

    orders_query = Query(
      'orders', [Merge(items_query, "'order_id'", "'item_id'")], False, {'order_id', 'item_id'}
    )
    customer_merge = Merge(orders_query, "'customer_id'", "'order_id'")

    assert customer_merge.entities == {'orders', 'items'}

    nation_query = Query('nation', [], False, set())

    supplier_query = Query(
      'supplier', [Merge(nation_query, "'nation_id'", "'nation_id'")], False, {'nation_id'}
    )

    lineitem_query = Query(
      'lineitem', [Merge(supplier_query, "'supplier_id'", "'supplier_id'")], False, {'supplier_id'}
    )

    complex_merge = Merge(lineitem_query, "'order_id'", "'order_id'")

    assert complex_merge.entities == {'lineitem', 'supplier', 'nation'}
