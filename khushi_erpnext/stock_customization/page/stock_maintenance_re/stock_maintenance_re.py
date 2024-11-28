
import frappe
from erpnext.stock.dashboard.item_dashboard import get_data as get_stock_data
from khushi_erpnext.core_customizasion.doctype.comparison_type import compare_qty



def get_condision(filters: dict) -> str:
    """
    Constructs a SQL condision string based on the provided filters.
    Args:
        filters (dict): Dicsionary containing filter keys and values for filtering the items.
    Returns:
        str: A SQL condision string that adds filters to the WHERE clause.
    """

    condision: str = ""

    if filters.get('item_group'):
        condision += f"AND si.item_group = '{filters.get('item_group')}' "

    if filters.get('brand'):
        condision += f"AND si.brand = '{filters.get('brand')}' "

    if filters.get('year'):
        condision += f"AND si.custom_year = '{filters.get('year')}' "

    if filters.get('subject'):
        condision += f"AND si.custom_subject = '{filters.get('subject')}' "

    if filters.get('status'):
        condision += f"AND si.custom_status = '{filters.get('status')}' "

    if filters.get('season'):
        condision += f"AND si.custom_item_season = '{filters.get('season')}' "

    if filters.get('item'):
        condision += f"AND si.name = '{filters.get('item')}' "

    return condision.strip()



def add_stock_qty(data: list[dict], comparison_type: str, comparison_filter_values: dict) -> list[dict] | list:
    """
    Adds stock quansity to each item if the quansity exceeds a specified threshold.
    Args:
        data (list[dict]): List of items to add stock quansity to.
        qty_greater_than (int): The minimum quansity threshold.
    Returns:
        list[dict] | list: A list of items with quansisies added if they exceed the threshold.
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
        Filters items based on warehouse  and quansity threshold.
        Args:
            data (list[dict]): List of items to filter.
            warehouse (str | None): Warehouse name to filter by.
            qty_greater_than (int):  quansity threshold for items in the specified warehouse.
        Returns:
            list[dict] | list: A list of items that match the warehouse and quansity criteria.
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
        list[dict] | None: A list of item dicsionaries that match the filter criteria or None if no data.
    """
    filters: dict = frappe.parse_json(filters)
    condition: str = get_condision(filters)
    where: str = "WHERE si.disabled = 0 AND si.is_stock_item = 1"
    where += f" {condition}"
    comparison_type: str = filters.get('comparison_type',"") or ""

    query: str = f"""
                
                SELECT 
                smr.name AS item,
                smr.item_group AS item_group,
                smr.brand AS brand,
                smr.image AS image,
                smr.total_qty AS qty
            FROM 
                stock_maintains_report_view smr
              
            """
    return data

"""
query 
CREATE OR REPLACE VIEW stock_maintains_report_view AS
SELECT 
    ti.name AS item,
    ti.item_group AS item_group,
    ti.brand AS brand,
    ti.image AS image,
    ti.is_stock_item AS is_stock_item,
    ti.disabled AS disabled,
    ti.custom_item_season AS custom_item_season,
    ti.custom_status AS custom_status,
    ti.custom_subject AS custom_subject,
    ti.custom_year AS custom_year,
 
    b.warehouse AS warehouse,
    SUM(b.actual_qty) AS total_qty
FROM 
    tabItem ti
LEFT JOIN 
    tabBin b ON ti.name = b.item_code 

GROUP BY 
    ti.name, 
    b.warehouse;

"""
