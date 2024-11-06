import frappe

def compare_qty(actual_qty: int, comparison_type: str, filter_constraint_values: dict) -> bool:
    """
    Compares the actual_qty against filter_constraint_values based on comparison_type.
    :param actual_qty: The actual quantity to be compared.
    :param comparison_type: The type of comparison to apply ("Greater than", "Between", etc.).
    :param filter_constraint_values: A dictionary holding one or two values for comparison.
        Example: {'value': 10} or {'value_from': 5, 'value_to': 15} for "Between".
    :return: True if the actual_qty meets the comparison condition, otherwise False.
    """

    if comparison_type == "Greater than" and actual_qty > filter_constraint_values.get('value'):
        return True
    elif comparison_type == "Greater than or Equal to" and actual_qty >= filter_constraint_values.get('value'):
        return True
    elif comparison_type == "Less than" and actual_qty < filter_constraint_values.get('value'):
        return True
    elif comparison_type == "Less than or Equal to" and actual_qty <= filter_constraint_values.get('value'):
        return True
    elif comparison_type == "Equals" and actual_qty == filter_constraint_values.get('value'):
        return True
    elif comparison_type == "Not Equals" and actual_qty != filter_constraint_values.get('value'):
        return True
    elif comparison_type == "Between":
        value_from = filter_constraint_values.get('value_from')
        value_to = filter_constraint_values.get('value_to')
        if value_from is not None and value_to is not None and value_from <= actual_qty <= value_to:
            return True
    return False