from oauthlib.uri_validate import query

import frappe
from hrms.hr.report.shift_attendance.shift_attendance import get_query


def build_qty_condition(filters: dict,condition: str, comparison_type: str) -> str:

    qty_from: int = filters.get('qty_from', 0)
    qty_to: int = filters.get('qty_to', 0)
    qty: int = filters.get('qty', 0)

    if comparison_type == 'Between':
        condition += f"AND smr.total_qty BETWEEN '{qty_from}' AND '{qty_to}' "

    elif comparison_type == 'Less than or Equal to':
        condition += f"AND smr.total_qty <= '{qty}' "

    elif comparison_type == 'Less than':
        condition += f"AND smr.total_qty < '{qty}' "

    elif comparison_type == 'Greater than or Equal to':
        condition += f"AND smr.total_qty >= '{qty}' "

    elif comparison_type == 'Greater than':
        condition += f"AND smr.total_qty > '{qty}' "

    elif comparison_type == 'Not Equals':
        condition += f"AND smr.total_qty != '{qty}' "

    elif comparison_type == 'Equals':
        condition += f"AND smr.total_qty = '{qty}' "

    return condition


def get_condition(filters: dict) -> str:
    """
    Constructs a SQL condition string based on the provided filters.
    Args:
        filters (dict): Dicsionary containing filter keys and values for filtering the items.
    Returns:
        str: A SQL condition string that adds filters to the WHERE clause.
    """

    condition: str = ""
    comparison_type: str | None = filters.get('comparison_type', None)

    if filters.get('item_group'):
        condition += f"AND smr.item_group = '{filters.get('item_group')}' "

    if filters.get('brand'):
        condition += f"AND smr.brand = '{filters.get('brand')}' "

    if filters.get('year'):
        condition += f"AND smr.custom_year = '{filters.get('year')}' "

    if filters.get('subject'):
        condition += f"AND smr.custom_subject = '{filters.get('subject')}' "

    if filters.get('status'):
        condition += f"AND smr.custom_status = '{filters.get('status')}' "

    if filters.get('season'):
        condition += f"AND smr.custom_item_season = '{filters.get('season')}' "

    if filters.get('item'):
        condition += f"AND smr.item = '{filters.get('item')}' "

    if filters.get('warehouse'):
        condition += f"AND smr.warehouse = '{filters.get('warehouse')}' "

    if comparison_type:
        condition = build_qty_condition(filters, condition, comparison_type)

    return condition.strip()

def get_query(filters: dict,where: str) -> str:
    warehouse: str| None = filters.get('warehouse',None)
    qty_field: str = "smr.total_qty AS qty" if warehouse else "SUM(smr.total_qty) AS qty"
    group_by: str = "" if warehouse else "GROUP BY smr.item"
    query: str = f"""
                SELECT 
                    smr.item AS item,
                    smr.item_group AS item_group,
                    smr.brand AS brand,
                    smr.image AS image,
                    {qty_field}
                FROM 
                    stock_maintains_report_view smr 
                {where}
                {group_by}
             """
    return query


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
    condition: str = get_condition(filters)
    where: str = f"WHERE smr.disabled = 0 AND smr.is_stock_item = 1 {condition}"
    query: str = get_query(filters,where)
    data: list[dict] = frappe.db.sql(query, as_dict=True)
    return data

