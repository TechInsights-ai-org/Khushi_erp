from khushi_erpnext.after_install_deployment.stock_maintains_report_view import execute as stock_maintains_report_view_executor
from khushi_erpnext.after_install_deployment.index_data import index_data
from khushi_erpnext.after_install_deployment.index_creator import create_indexes_if_not_exists




def execute():
    stock_maintains_report_view_executor()
    create_indexes_if_not_exists(index_data)