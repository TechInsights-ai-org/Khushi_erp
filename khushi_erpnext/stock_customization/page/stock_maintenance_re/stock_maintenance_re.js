frappe.pages['stock-maintenance-re'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Stock Maintenance Report',
        single_column: true
    });

    // Create Filter Section
    let filter_fields = [
        {fieldname: "warehouse", label: "Warehouse", fieldtype: "Link", options: 'Warehouse'},
        {fieldname: "item_group", label: "Item Group", fieldtype: "Link", options: "Item Group"},
        {fieldname: "brand", label: "Brand", fieldtype: "Link", options: "Brand"},
        {fieldname: "year", label: "Year", fieldtype: "Link", options: 'Year'},
        {fieldname: "subject", label: "Subject", fieldtype: "Link", options: 'Subject'},
        {fieldname: "status", label: "Status", fieldtype: "Select", options: ["","Continue", "SemiContinue", "Discontinue"]},
        {fieldname: "season", label: "Season", fieldtype: "Link", options: 'Item Segment'},
        {fieldname: "item", label: "Item", fieldtype: "Link", options: "Item"},
        {fieldname: "qty", label: "Qty Greater than", fieldtype: "Int", defualt:0}
    ];

    // Initialize Filters
    filter_fields.forEach(function (field) {
        page.add_field({
            fieldname: field.fieldname,
            label: field.label,
            fieldtype: field.fieldtype,
            options: field.options || '',
            change: function () {
                update_dashboard();
            }
        });
    });

    // Create the grid container
    let grid_container = $('<div></div>').css({
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',  // Dynamically adjust to fit the screen size
        gap: '20px',
        marginTop: '20px',
    }).appendTo(page.body);

    function update_dashboard() {
        let filters = {
            warehouse: page.fields_dict.warehouse.get_value(),
            item_group: page.fields_dict.item_group.get_value(),
            brand: page.fields_dict.brand.get_value(),
            year: page.fields_dict.year.get_value(),
            subject: page.fields_dict.subject.get_value(),
            status: page.fields_dict.status.get_value(),
            season: page.fields_dict.season.get_value(),
            item: page.fields_dict.item.get_value(),
            qty: page.fields_dict.qty.get_value()
        };
        frappe.call({
            method: "khushi_erpnext.stock_customization.page.stock_maintenance_re.stock_maintenance_re.get_data",
            args: {
                filters: filters,
            },
            callback: function (r) {
                grid_container.empty();
                display_report_data(r.message);

            }
        });
    }

    function reset_filters() {
        filter_fields.forEach(function (field) {
            page.fields_dict[field.fieldname].set_value('');
        });
        update_dashboard();
    }

    page.add_button('Reset Filters', reset_filters);

    function display_report_data(items) {
        if (!items || items.length === 0) {
        $('<div>No data found</div>')
            .css({
                textAlign: 'center',
                padding: '20px',
                color: '#666',
                fontSize: '16px',
                fontStyle: 'italic'
            })
            .appendTo(grid_container);
        return;
    }

        items.forEach(function (item) {
            let item_div = $('<div class="item-container"></div>').css({
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                padding: '15px',
                textAlign: 'center',
                border: '1px solid #ddd',
                borderRadius: '10px',
                background: 'linear-gradient(135deg, #e3f2fd, #fce4ec)',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                transition: 'transform 0.2s, box-shadow 0.2s',
                cursor: 'pointer',
                marginBottom: '20px'
            }).hover(
                function () {
                    // On hover, slightly enlarge the item and add a stronger shadow
                    $(this).css({
                        transform: 'scale(1.05)',
                        boxShadow: '0 6px 16px rgba(0, 0, 0, 0.2)'
                    });
                },
                function () {
                    // Reset the size and shadow when hover is removed
                    $(this).css({
                        transform: 'scale(1)',
                        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                    });
                }
            ).appendTo(grid_container);

            // Item Image
            let img = $('<img>').attr('src', item.image || 'placeholder-image-url.png')
                .css({
                    width: '160px',
                    height: '100px',
                    objectFit: 'cover',
                    borderRadius: '8px',
                    marginBottom: '10px'
                }).appendTo(item_div);

            // Item Code / Name
            $('<div></div>').text(`Item: ${item.item || 'No Item Code'}`)
                .css({
                    fontWeight: 'bold',
                    fontSize: '14px',
                    marginBottom: '8px',
                    color: '#333' // Darker text for contrast
                }).appendTo(item_div);

            // Item description
            $('<div></div>').text(`Item Group: ${item.item_group || 'N/A'}`)
                .css({
                    fontSize: '12px',
                    color: '#666',
                    marginBottom: '8px'
                }).appendTo(item_div);

            // Stock Quantity
            $('<div></div>').text(`Total Qty: ${item.qty || '0'}`)
                .css({
                    fontSize: '12px',
                    color: '#333'
                }).appendTo(item_div);
        });
    }
     update_dashboard();
}

