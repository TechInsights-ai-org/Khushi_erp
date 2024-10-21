import frappe


def append_and_if_needed(condition: str) -> str:
    if condition:
        condition += "AND "
    return condition

def get_condition(filters: dict) -> str:
    condition: str = ""

    if filters.get('warehouse'):
        condition += f"warehouse = '{filters.get('warehouse')}' "

    if filters.get('rack'):
        condition = append_and_if_needed(condition)
        condition += f"rack = '{filters.get('rack')}' "

    if filters.get('item_group'):
        condition = append_and_if_needed(condition)
        condition += f"item_group = '{filters.get('item_group')}' "

    if filters.get('brand'):
        condition = append_and_if_needed(condition)
        condition += f"brand = '{filters.get('brand')}' "

    if filters.get('year'):
        condition = append_and_if_needed(condition)
        condition += f"year = '{filters.get('year')}' "

    if filters.get('subject'):
        condition = append_and_if_needed(condition)
        condition += f"subject = '{filters.get('subject')}' "

    if filters.get('status'):
        condition = append_and_if_needed(condition)
        condition += f"status = '{filters.get('status')}' "

    if filters.get('season'):
        condition = append_and_if_needed(condition)
        condition += f"season = '{filters.get('season')}' "

    if filters.get('item'):
        condition = append_and_if_needed(condition)
        condition += f"item = '{filters.get('item')}' "

    if condition:
        condition = f"WHERE {condition}"

    return condition.strip()





@frappe.whitelist()
def get_data(filters:str) -> list[dict] | None:
    filters: dict = frappe.parse_json(filters)
    condition: str = get_condition(filters)
    query: str = f""" SELECT * FROM `stock_maintaince_view` {condition} """
    item_data: list[dict] = frappe.db.sql(query, as_dict=True)
    print("-------------------------",item_data)
    return item_data if item_data else None