frappe.pages['device-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Router Stats',
        single_column: true
    });

    // Render main HTML template
    page.main.html(frappe.render_template("device_dashboard", {}));

    // Populate the router dropdown on page load
    frappe.call({
        method: 'your_app_name.your_module_name.get_routers',  // Replace with your method
        callback: function(r) {
            let routers = r.message;
            let $select = $('#router-select');
            $select.empty();
            $select.append('<option value="">Select a router</option>');
            routers.forEach(function(router) {
                $select.append(`<option value="${router.name}">${router.device_name}</option>`);
            });
        }
    });

    // On router selection, fetch the data for the selected router
    $('#router-select').on('change', function() {
        let selectedRouterId = $(this).val();
        if (selectedRouterId) {
            fetchRouterData(selectedRouterId);
        }
    });

    // Function to fetch router data
    function fetchRouterData(routerId) {
        frappe.call({
            method: 'billing_system.billing_system.page.device_dashboard.device_dashboard',
            args: { device_id: routerId },
            callback: function(r) {
                let data = r.message;
                // Populate fields in the dashboard with fetched data
                updateDashboard(data);
            }
        });
    }

    // Function to update the dashboard
    function updateDashboard(data) {
        // Update the fields with the received data
        $('#activeUsers').text(data.activeUsers || '0');
        $('#cpuLoad').text(data.cpuLoad ? data.cpuLoad + '%' : '0%');
        $('#income').text('Rp ' + (data.income || '0'));
        $('#memory').text(data.memory ? data.memory + ' MB' : 'Loading...');
        $('#hdd').text(data.hdd ? data.hdd + ' MB' : 'Loading...');
        $('#health').text(data.health || 'Loading...');
        $('#uptime').text(data.uptime || 'Loading...');
        $('#model').text(data.model || 'Loading...');
        $('#routerOS').text(data.routerOS || 'Loading...');
        $('#appLog').text(data.appLog || 'No logs available');
        $('#hotspotLog').text(data.hotspotLog || 'No logs available');
    }

    // Real-time event listener for webhook data
    frappe.realtime.on('mikrotik_data', function(data) {
        // When mikrotik_data is received, update the dashboard
        updateDashboard(data);
    });
};
