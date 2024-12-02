import frappe


def create_soiq_view():
    query = """
           CREATE OR REPLACE
            ALGORITHM = UNDEFINED VIEW `veuSales Order Item Quantity` AS
            SELECT so.transaction_date, so.name, so.status, so.customer, soi.item_code, soi.qty, so.company FROM `tabSales Order` AS so
            JOIN `tabSales Order Item` AS soi ON so.name = soi.parent;
            """
    frappe.db.sql(query)
    frappe.db.commit()
    print("----------------- View Created for Sales Order Item Quantity ------------------------ ")


def create_poiq_view():
    query = """
           CREATE OR REPLACE
            ALGORITHM = UNDEFINED VIEW `veuPurchase Order Item Quantity` AS 
            SELECT CASE WHEN po.is_subcontracted = 1 THEN COALESCE(poi.fg_item_qty, 0) ELSE COALESCE(poi.qty, 0) END as "poi_qty",
                  CASE WHEN po.is_subcontracted = 1 THEN poi.fg_item ELSE poi.item_code END as "item_code"
            FROM `tabPurchase Order` AS po
                 JOIN `tabPurchase Order Item` AS poi ON po.name = poi.parent
            WHERE po.status NOT IN ("To Bill", "Completed", "Cancelled", "Closed", "Delivered");
            """
    frappe.db.sql(query)
    frappe.db.commit()
    print("----------------- View Created for Purchase Order Item Quantity ------------------------ ")


def create_scirq_view():
    query = """
           CREATE OR REPLACE
            ALGORITHM = UNDEFINED VIEW `veuSubcontracting Item Quantity to Receive` AS
            SELECT scoi.qty - scoi.received_qty as "subcontract_qty", scoi.item_code
            FROM `tabSubcontracting Order` AS sco
                     JOIN `tabSubcontracting Order Item` AS scoi ON sco.name = scoi.parent
            WHERE sco.status NOT IN ("Completed", "Cancelled", "Closed");
            """
    frappe.db.sql(query)
    frappe.db.commit()
    print("----------------- View Created for Subcontracting Item Receive Quantity ------------------------ ")



def execute():
    create_soiq_view()
    create_poiq_view()
    create_scirq_view()
