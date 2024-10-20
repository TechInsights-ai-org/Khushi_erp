import frappe


def get_condition(filters:dict):
    return ""

def get_data(filters:dict):
    # condition: str = get_condition(filters)
    query = """
        SELECT * FROM tabItem  
    """
    item_data = frappe.db.sql(query, as_dict=True)
    return item_data