# Copyright (c) 2024, TechInsights and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.caching import redis_cache


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns() -> list[dict]:
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date"},
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Qty to Deliver", "fieldname": "qty_to_deliver", "fieldtype": "float"},
        {"label": "Stock Balance", "fieldname": "stock_balance", "fieldtype": "float"},
        {"label": "Purchase Qty", "fieldname": "purchase_qty", "fieldtype": "float"}]


def get_condition(filters: dict) -> str:
    "Need to return condition based on the filter the give"
    pass


@redis_cache
def get_stock_balance(item_code: str, warehouse: str = None) -> float:
    cond: str = f"WHERE item_code = '{item_code}'"
    if warehouse:
        cond += f" warehouse = {warehouse}"
    stock_qty: float = frappe.db.sql(f"""SELECT SUM(actual_qty) AS "stock_qty" FROM `tabBin` {cond};""",
                                   pluck="stock_qty")[0]
    return stock_qty if stock_qty else 0

@redis_cache
def get_po_balance(item_code: str) -> float:
    poi_qty: float = frappe.db.sql(f"""SELECT sum(poi.qty) as "poi_qty"
                                    FROM `tabPurchase Order` AS po
                                             JOIN `tabPurchase Order Item` AS poi ON po.name = poi.parent
                                    WHERE po.status NOT IN ("To Bill", "Completed", "Cancelled", "Closed", "Delivered") 
                                    AND poi.item_code = '{item_code}';""",
                                   pluck="poi_qty")[0]
    return poi_qty if poi_qty else 0


def append_balance(func, data: list[list], *args):
    for row in data:
        row.append(func(row[4], *args) if args else func(row[4]))
    return data


def get_data(filters: dict) -> list[list]:
    cond: str = get_condition(filters)
    data = frappe.db.sql("""SELECT so.transaction_date as "Date",
                               so.name             as "Sales Order",
                               so.status           as "Status",
                               so.customer         as "Customer",
                               soi.item_code       as "Item Code",
                               soi.qty             as "Qty to Deliver"
                        FROM `tabSales Order` AS so
                                 JOIN `tabSales Order Item` AS soi ON so.name = soi.parent
                        WHERE so.status <> "Cancelled";""", as_list=True)
    data = append_balance(get_stock_balance, data, filters.get("warehouse", None))
    data = append_balance(get_po_balance, data)
    return data
