import frappe
from frappe import _dict
from frappe.utils import get_date_str, nowdate
from erpnext.stock.dashboard.item_dashboard import get_data
from erpnext.stock.report.stock_balance.stock_balance import execute


def get_rack_balance(filters: dict) -> tuple[list[dict], str]:
    to_date_str: str = get_date_str(nowdate())
    company: str = filters.get("company", frappe.defaults.get_user_default('Company'))
    item_code: str = filters.get("item_code", "")
    warehouse: str = filters.get("warehouse", "")
    filters = _dict({'company': company, 'from_date': '2000-01-1', 'to_date': to_date_str,
                     'item_code': item_code, 'warehouse': warehouse,
                     'valuation_field_type': 'Currency', 'rack': [],
                     'show_dimension_wise_stock': 1})
    _, rack_balance = execute(filters)
    return rack_balance, "bal_qty"


def get_warehouse_balance(filters: dict) -> tuple[list[dict], str]:
    warehouse_balance: list[dict] = get_data(item_code=filters.get("item_code", ""))
    return warehouse_balance, "actual_qty"


def get_outward_dropdown_list(doctype: str, txt: str, filters: dict) -> list[list[str]]:
    dropdown_list: list[list[str]] = []
    balance_dict: list[dict] = []
    doc_key: str = doctype.lower()
    balance_key: str = ""
    if doctype == "Warehouse":
        balance_dict, balance_key = get_warehouse_balance(filters)
    elif doctype == "Rack":
        balance_dict, balance_key = get_rack_balance(filters)
    if not balance_dict:
        return []
    lower_search_txt: str = txt.lower()
    for value in balance_dict:
        doc_record: str | None = value.get(doc_key, "")
        if not doc_record:
            continue
        doc: "Document" = frappe.get_doc(doctype, doc_record)
        if doc.disabled:
            continue
        actual_balance = value.get(balance_key)
        if not actual_balance:
            continue
        if lower_search_txt in doc_record.lower() or not lower_search_txt:
            dropdown_list.append([doc_record, f"Actual balance: {actual_balance}"])
    return dropdown_list


def get_condition(txt: str, searchfield: str, cond_list: None | list = None) -> str:
    if not cond_list:
        cond_list: list = []
    if txt:
        cond_list.append(f"{searchfield} LIKE \"%{txt}%\"")
    cond: str = "WHERE disabled = 0 AND " + " AND ".join(cond_list) if cond_list else "WHERE disabled = 0"
    return cond


def get_inward_dropdown_list(doctype: str, txt: str, searchfield: str, filters: dict) -> list[list[str]]:
    cond_list: list = []
    warehouse: str = filters.get("warehouse", "")
    if doctype == "Rack" and warehouse:
        cond_list.append(f" warehouse='{warehouse}' ")
    cond: str = get_condition(txt, searchfield, cond_list)
    return frappe.db.sql(f"""SELECT name From `tab{doctype}` {cond}""")


@frappe.whitelist()
def stock_dropdown_filter(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict)-> list[list[str]]:
    dropdown_type: str = filters.get("dropdown_type", "")
    item_code: str = filters.get("item_code", "")
    cond: str = get_condition(txt, searchfield)
    if not dropdown_type:
        return frappe.db.sql(f"""SELECT name From `tab{doctype}` {cond}""")
    if not item_code and dropdown_type == "outward":
        return []
    dropdown_value: list = []
    if dropdown_type == "inward":
        dropdown_value = get_inward_dropdown_list(doctype, txt, searchfield, filters)
    elif dropdown_type == "outward":
        dropdown_value = get_outward_dropdown_list(doctype, txt, filters)
    return dropdown_value


