frappe.pages['stock-maintenance-re'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Stock Maintenance Report',
        single_column: true
    });

    // Create Filter Section
    let filter_fields = [
        {fieldname: "warehouse", label: "Warehouse", fieldtype: "Link", options: 'Warehouse'},
        {fieldname: "rack", label: "Rack", fieldtype: "Link",options:'Rack'},
        {fieldname: "item_group", label: "Item Group", fieldtype: "Link", options: "Item Group"},
        {fieldname: "brand", label: "Brand", fieldtype: "Link", options: "Brand"},
        {fieldname: "year", label: "Year", fieldtype: "Link",options:'Year'},
        {fieldname: "subject", label: "Subject", fieldtype: "Link",options:'Subject'},
        {fieldname: "status", label: "Status", fieldtype: "Select", options: ["All", "Continue","SemiContinue","Discontinue"]},
        {fieldname: "season", label: "Season", fieldtype: "Link",options:'Item Segment'},
        {fieldname: "item", label: "Item", fieldtype: "Link", options: "Item"}
    ];

    // Initialize Filters
    filter_fields.forEach(function (field) {
        page.add_field({
            fieldname: field.fieldname,
            label: field.label,
            fieldtype: field.fieldtype,
            options: field.options || '',
            change: function() {
                update_dashboard();
            }
        });
    });

    let grid_container = $('<div></div>').appendTo(page.body);
    // Function to Fetch and Update Dashboard based on Filters
    function update_dashboard() {
        let filters = {
            warehouse: page.fields_dict.warehouse.get_value(),
            rack: page.fields_dict.rack.get_value(),
            item_group: page.fields_dict.item_group.get_value(),
            brand: page.fields_dict.brand.get_value(),
            year: page.fields_dict.year.get_value(),
            subject: page.fields_dict.subject.get_value(),
            status: page.fields_dict.status.get_value(),
            season: page.fields_dict.season.get_value(),
            item: page.fields_dict.item.get_value(),
        };
        console.log(filters)
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Stock Ledger Entry',
                filters: filters,
                fields: ['item_code', 'warehouse', 'brand', 'stock_qty'],
            },
            callback: function(r) {
                if (r.message) {
                    // Here, update your dashboard with the filtered data
                    display_report_data(r.message);
                }
            }
        });
    }

     function reset_filters() {
            filter_fields.forEach(function (field) {
                page.fields_dict[field.fieldname].set_value('');
            });
            update_dashboard();  // Refresh dashboard without filters
        }

        page.add_button('Reset Filters', reset_filters);

    function display_report_data(items) {
            // Create grid structure and display items
            items.forEach(function(item) {
                let item_div = $('<div class="item-container"></div>').css({
                    display: 'inline-block',
                    width: '150px',
                    padding: '10px',
                    textAlign: 'center',
                    border: '1px solid #ddd',
                    margin: '10px'
                }).appendTo(grid_container);

                // Item Image
                let img = $('<img>').attr('src', item.image || 'placeholder-image-url.png') // fallback to a placeholder image if no image is available
                                    .css({ width: '100px', height: '100px', objectFit: 'cover' })
                                    .appendTo(item_div);

                // Item Code / Name
                $('<div></div>').text(item.item_code || 'No Item Code')
                                .css({ fontWeight: 'bold', margin: '10px 0' })
                                .appendTo(item_div);

                // Item description or any other detail
                $('<div></div>').text(item.item_description || 'No description available')
                                .css({ fontSize: '12px', color: '#666' })
                                .appendTo(item_div);

                // Any other fields like quantity, warehouse, etc.
                $('<div></div>').text(`Stock Qty: ${item.stock_qty || 'N/A'}`)
                                .css({ fontSize: '12px', color: '#333' })
                                .appendTo(item_div);
            });
        }

        // Initial load of the dashboard
        update_dashboard();

    };
