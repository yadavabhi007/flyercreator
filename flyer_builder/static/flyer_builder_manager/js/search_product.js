App.search_product = {
    search_and_select: false,

    init: function () {
        App.search_product.init_search_field();
    },

    init_search_field: function () {
        $('#search-product-form_description, #search-product-form_code').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13') {
                App.search_product.search_by_description();
            }
        });
    },

    open_search_product_modal: function (select) {
        App.search_product.search_and_select = select;
        $("#search-product-modal #search-product-result").empty();
        $('#search-product-form_description, #search-product-form_code').val("");
        $("#search-product-modal").modal("show");
    },
    

    search_by_code: function () {
        let params = {
            code: $("#search-product-form_code").val(),
            description: ""
        };
        $("#search-product-form_description").val("");
        App.search_product.search(params);
    },

    

    search_by_description: function () {
        let params = {
            code: "",
            description: $("#search-product-form_description").val()
        }
        $("#search-product-form_code").val("");
        App.search_product.search(params);
    },

    open_search_image_modal: function (select,type) {
        App.search_product.search_and_select = select;
        $("#search-product-modal #search-product-result").empty();
        $('#search-image-form_code').val("");
        if (type == 'header'){
            $("#search-image-modal").modal("show");
        }else{
            $("#search-image-modal-footer").modal("show");
            
        }
        
    },
    search_header_banner:function(clientID,projectID,pageID,header_bannerID,type){
        $.ajax({
            method: "GET",
            url: "/search-header-banner",
            data: {
                'clientID':clientID,
                'projectID':projectID,
                'pageID':pageID,
                'header_bannerID':header_bannerID,
                'tipo':type
            }
        })
            .done(function (data) {
                if (type == 'footer'){
                    $("#search-image-result-footer").html(data);
                }else{
                    $("#search-image-result").html(data);
                }
                
                if (App.search_product.search_and_select){
                    $("#search-product-result .search-result-edit-button").hide();
                } else {
                    $("#search-product-result .search-result-select-button").hide();
                }
            })
            .fail(function () {
                alert("Spiacenti, si è verificato un errore imprevisto nella ricerca");
            })
            .always(function () {
                App.hide_loader();
            });
    },
    search: function (params) {
        App.show_loader();
        $.ajax({
            method: "GET",
            url: "/products/search",
            data: params
        })
            .done(function (data) {
                $("#search-product-result").html(data);
                if (App.search_product.search_and_select){
                    $("#search-product-result .search-result-edit-button").hide();
                } else {
                    $("#search-product-result .search-result-select-button").hide();
                }
            })
            .fail(function () {
                alert("Spiacenti, si è verificato un errore imprevisto nella ricerca");
            })
            .always(function () {
                App.hide_loader();
            });
    }
}