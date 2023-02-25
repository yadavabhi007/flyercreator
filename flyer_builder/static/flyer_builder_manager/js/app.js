App = {
    project_initializing_polling_intervals: {},

    set_project_initializing_polling: function (project_id) {
        App.project_initializing_polling_intervals[project_id] = setInterval(function(){ App.check_project_initialization(project_id); }, 10000);
    },

    check_project_initialization: function (project_id) {
        $.ajax({
            method: "GET",
            url: "/projects/" + project_id + "/initialization-status"
        })
            .done(function (response) {
                if (response.status == "initialization_completed") {
                    clearInterval(App.project_initializing_polling_intervals[project_id]);
                    $("#project_" + project_id).removeClass();
                    $("#initializing_project_label_" + project_id).hide();
                    $("#edit_button_" + project_id).show();
                    $("#delete_button_" + project_id).show();
                }
                else if (response.status == "excel_import_failed"){
                    window.location.reload();
                }
            })
            .fail(function () {
            });
    },

    show_loader: function (el = false) {
        if (el) {
            $(el).LoadingOverlay("show", {
                imageColor: "#343a40"
            });
        } else {
            $.LoadingOverlay("show", {
                imageColor: "#343a40"
            });
        }
    },

    hide_loader: function (el = false) {
        if (el) {
            $(el).LoadingOverlay("hide");
        } else {
            $.LoadingOverlay("hide");
        }
    },

    create_excel_project: function () {
        if (!document.getElementById("excel-project-name").checkValidity()) {
            document.getElementById("excel-project-name").reportValidity();
            return;
        }
        if (!document.getElementById("excel-project-file").checkValidity()) {
            document.getElementById("excel-project-file").reportValidity();
            return;
        }

        App.show_loader();
        $("#create-excel-project-form").submit();
    },

    zoom: function (zoom_type) {
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/zoom?type=" + zoom_type;
    },
}