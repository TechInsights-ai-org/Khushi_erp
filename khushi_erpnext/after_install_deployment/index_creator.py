import frappe


def create_indexes_if_not_exists(index_data):
    """
    Check if the index exists for each table-column combination in the provided list of dicts.
    If the index does not exist, create it.

    :param index_data: List of dictionaries, where each dictionary contains:
                        'table_name' - The table where the index needs to be created.
                        'index_name' - The name of the index.
                        'column_name' - The column on which the index should be created.
    """

    for data in index_data:
        table_name = data.get('table_name')
        index_name = data.get('index_name')
        column_name = data.get('column_name')

        index_exists = frappe.db.sql("""
            SELECT COUNT(*) 
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
              AND table_name = %s
              AND index_name = %s
        """, (table_name, index_name))[0][0]


        if index_exists == 0:
            try:
                frappe.db.sql("""
                    CREATE INDEX `{}` ON `{}`(`{}`)
                """.format(index_name, table_name, column_name))
                frappe.db.commit()
                print(f"Index `{index_name}` created successfully on `{table_name}` ({column_name})!")
            except Exception as e:
                frappe.log_error(f"`{table_name}`","Index Creation Error {str(e)}")
                print(f"Failed to create index `{index_name}`: {str(e)}")
        else:
            print(f"Index `{index_name}` already exists on table `{table_name}`.")
