
import frappe
from erpnext.stock.dashboard.item_dashboard import get_data as get_stock_data
from khushi_erpnext.core_customization.doctype.comparison_type import compare_qty



def get_condition(filters: dict) -> str:
    """
    Constructs a SQL condition string based on the provided filters.
    Args:
        filters (dict): Dictionary containing filter keys and values for filtering the items.
    Returns:
        str: A SQL condition string that adds filters to the WHERE clause.
    """

    condition: str = ""

    if filters.get('item_group'):
        condition += f"AND ti.item_group = '{filters.get('item_group')}' "

    if filters.get('brand'):
        condition += f"AND ti.brand = '{filters.get('brand')}' "

    if filters.get('year'):
        condition += f"AND ti.custom_year = '{filters.get('year')}' "

    if filters.get('subject'):
        condition += f"AND ti.custom_subject = '{filters.get('subject')}' "

    if filters.get('status'):
        condition += f"AND ti.custom_status = '{filters.get('status')}' "

    if filters.get('season'):
        condition += f"AND ti.custom_item_season = '{filters.get('season')}' "

    if filters.get('item'):
        condition += f"AND ti.name = '{filters.get('item')}' "

    return condition.strip()



def add_stock_qty(data: list[dict], comparison_type: str, comparison_filter_values: dict) -> list[dict] | list:
    """
    Adds stock quantity to each item if the quantity exceeds a specified threshold.
    Args:
        data (list[dict]): List of items to add stock quantity to.
        qty_greater_than (int): The minimum quantity threshold.
    Returns:
        list[dict] | list: A list of items with quantities added if they exceed the threshold.
    """

    result: list = []
    for item_code in data:
        stock_data: list[dict] = get_stock_data(item_code.get('item'))
        qty: int = 0
        for stock in stock_data:
            qty += stock.get('actual_qty')
        item_code['qty'] = qty
        if comparison_type:
            if compare_qty(actual_qty=qty,comparison_type=comparison_type,filter_constraint_values=comparison_filter_values):
                result.append(item_code)
        else:
            result.append(item_code)
    return result


def get_warehouse_based_qty(data:list[dict], warehouse: str|None ,comparison_type: str, comparison_filter_values: dict) -> list[dict] | list:
    """
        Filters items based on warehouse  and quantity threshold.
        Args:
            data (list[dict]): List of items to filter.
            warehouse (str | None): Warehouse name to filter by.
            qty_greater_than (int):  quantity threshold for items in the specified warehouse.
        Returns:
            list[dict] | list: A list of items that match the warehouse and quantity criteria.
    """
    result:list = []
    for item_code in data:
        stock_data = get_stock_data(item_code.get('item'))
        for stock in stock_data:
            stock_dict = {}
            stock_dict['qty'] = stock.get('actual_qty')
            stock_dict['warehouse'] = stock.get('warehouse')
            stock_dict['item'] = item_code.get('item')
            stock_dict['image'] = item_code.get('image')
            stock_dict['item_group'] = item_code.get('item_group')
            result.append(stock_dict)

    warehouse_data: list = []
    for data in result:
        if data.get('warehouse') == warehouse:
            if comparison_type:
                if compare_qty(actual_qty=data.get('qty'),comparison_type=comparison_type,filter_constraint_values=comparison_filter_values):
                    warehouse_data.append(data)
            else:
                warehouse_data.append(data)
    return warehouse_data


@frappe.whitelist()
def get_data(filters:str) -> list[dict] | None:
    """
    Retrieves item data based on specified filters.
    Args:
        filters (str): JSON string containing filter criteria for retrieving item data.
    Returns:
        list[dict] | None: A list of item dictionaries that match the filter criteria or None if no data.
    """
    filters: dict = frappe.parse_json(filters)
    condition: str = get_condition(filters)
    where: str = "WHERE ti.disabled = 0 AND ti.is_stock_item = 1"
    comparison_type: str = filters.get('comparison_type',"") or ""
    comparison_filter_values:dict = {"value":filters.get("qty"),"value_from":filters.get("qty_from"),"value_to":filters.get("qty_to")}
    if condition:
        where += f" {condition}"

    query: str = f"""
            SELECT 
                ti.name as item,
                ti.item_group as item_group,
                ti.brand as brand,
                ti.image as image
            FROM 
                tabItem ti 
            {where}
            """

    data = frappe.db.sql(query, as_dict=True)
    if data and not filters.get('warehouse'):
        data = add_stock_qty(data,comparison_type,comparison_filter_values)
    if data and filters.get('warehouse'):
        data = get_warehouse_based_qty(data,filters.get('warehouse'),comparison_type,comparison_filter_values)
    return data

