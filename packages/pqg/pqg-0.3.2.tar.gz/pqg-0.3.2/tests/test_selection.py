from pqg.selection import Selection


class TestSelection:
  def test_empty_selection(self):
    selection = Selection([])
    assert selection.apply('customer') == ''

  def test_single_condition(self):
    selection = Selection([("'age'", '>=', 25, None)])
    assert selection.apply('customer') == "[(customer['age'] >= 25)]"

  def test_multiple_conditions_with_and(self):
    selection = Selection([("'age'", '>=', 25, '&'), ("'status'", '==', "'active'", None)])

    assert (
      selection.apply('customer') == "[(customer['age'] >= 25) & (customer['status'] == 'active')]"
    )

  def test_string_operations(self):
    selection = Selection(
      [("'name'", '.str.startswith', "'A'", '&'), ("'email'", '.str.startswith', "'test'", None)]
    )

    assert (
      selection.apply('customer')
      == "[(customer['name'].str.startswith('A')) & (customer['email'].str.startswith('test'))]"
    )

  def test_isin_operation(self):
    selection = Selection([("'status'", '.isin', ['active', 'pending'], None)])
    assert selection.apply('customer') == "[(customer['status'].isin(['active', 'pending']))]"
