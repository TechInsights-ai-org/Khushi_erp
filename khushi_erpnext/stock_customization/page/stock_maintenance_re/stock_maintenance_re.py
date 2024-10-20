import frappe


def get_condition(filters:dict):
    return ""

@frappe.whitelist()
def get_data(filters):
    print(filters,"----------------------------------------------------------")
    # condition: str = get_condition(filters)
    query = """
        SELECT * FROM tabItem  WHERE custom_image_template IS NOT NULL
    """
    item_data = frappe.db.sql(query, as_dict=True)
    return item_data