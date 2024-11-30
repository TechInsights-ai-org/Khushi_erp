import frappe

def create_stock_maintains_report_view():
    query = """
            CREATE OR REPLACE
            ALGORITHM = UNDEFINED VIEW `stock_maintains_report_view` AS
            select
                `ti`.`name` AS `item`,
                `ti`.`item_group` AS `item_group`,
                `ti`.`brand` AS `brand`,
                `ti`.`image` AS `image`,
                `ti`.`is_stock_item` AS `is_stock_item`,
                `ti`.`disabled` AS `disabled`,
                `ti`.`custom_item_season` AS `custom_item_season`,
                `ti`.`custom_status` AS `custom_status`,
                `ti`.`custom_subject` AS `custom_subject`,
                `ti`.`custom_year` AS `custom_year`,
                `b`.`warehouse` AS `warehouse`,
                IFNULL(sum(`b`.`actual_qty`),0) AS `total_qty`
            from
                (`tabItem` `ti`
            left join `tabBin` `b` on
                (`ti`.`name` = `b`.`item_code`))
            group by
                `ti`.`name`,
                `b`.`warehouse`;
            """

    frappe.db.sql(query)
    frappe.db.commit()
    print("----------------- View Created for Stock Maintains Report ------------------------ ")



def execute():
    create_stock_maintains_report_view()
