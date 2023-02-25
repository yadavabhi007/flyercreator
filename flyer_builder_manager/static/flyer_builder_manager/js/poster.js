App.poster = {
    project_id: null,
    current_product_id: null,

    init: function (project_id) {
        App.poster.project_id = project_id;
        App.poster.init_available_images_list();
    },

    init_available_images_list: function () {
        App.poster.init_image_dad();
        App.poster.init_available_images_dad();
    },

    init_image_dad: function(){
      $(".poster_name").droppable({
            accept: ".card",
            drop: function (event, ui) {
                  App.show_loader();
                  image_id = $(ui.draggable).data("image_id")
                  target = $(event.target).data("target");
                  App.poster.save_image_data_api(target, false, image_id).then(function (response) {
                      if (!response.status == "edited") {
                          alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
                      }
                      return App.poster.get_poster_partial();
                  }).then(function (html_page) {
                      $("#page-wrapper").html(html_page);
                      App.hide_loader();
                  }).catch(function (error_message) {
                      alert(error_message);
                      App.hide_loader();
                  });
            }
      });
    },
    init_available_images_dad: function () {
        $(".card").draggable({
            revert: "invalid",
            cursor: "crosshair",
        });
    },


    reload: function () {
        App.poster.get_poster_partial().then(function (html) {
            $("#page-wrapper").html(html);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
        });
    },

    // Project special cell functions
    add_image_to_cell: function (type) {
        App.search_product.open_search_image_modal(true,type);
    },

    select_image_to_add: function (image_id, special_cell_id, page_id, project_id, type) {
        $('#search-image-modal').modal('hide');
        $('#search-image-modal-footer').modal('hide');
        App.poster.import_image_to_cell(image_id, special_cell_id, page_id, project_id, type).then(function (response) {
            if (response.status == "imported") {
                return App.poster.get_poster_partial();
            }
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
        }).catch(function (error_message) {
            alert(error_message);
        });
    },
    import_image_to_cell: function (image_id,special_cell_id,page_id,project_id,type) {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "GET",
                url: "/project/import-image-to-cell",
                data: {
                    'specialCellID': special_cell_id,
                    'imageID': image_id,
                    'page_id':page_id,
                    'project_id':project_id,
                    'type':type
                }
            })
                .done(function (data) {
                    if(type == 'header'){
                        $('#header_banner').html('');
                        $('#header_banner').append(`<img class="header_banner" src="`+ data.url +`" alt="" style="width: 100%;height: 100%;">`)
                    }else{
                        $('#footer_banner').html('');
                        $('#footer_banner').append(`<img class="footer_banner" src="`+ data.url +`" alt="" style="width: 100%;height: 100%;">`)
                    }
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante l'importazione del prodotto da catalogo");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },
    get_poster_partial: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "GET",
                url: "/project/" + App.poster.project_id + "/poster/partial"
            })
                .done(function (data) {
                    $("#center").css("left", '226px');
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante il recupero delle informazioni sulla pagina");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },

    edit_page_style: function () {
        App.show_loader("#pageStyle .modal-content");
        $('#pageStyle').modal('show');
        App.hide_loader("#pageStyle .modal-content");
    },
    edit_page_banner: function () {
        document.getElementById("mySidenav").style.width = "240px";
        document.getElementById("mySidenav").style.overflow = "overlay";
        document.getElementById("center").style.left = "473px";
        $(".closebtn").show()
    },
    close_page_banner: function(){
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("mySidenav").style.overflow = "hidden";
        document.getElementById("center").style.left = "226px";
        $(".closebtn").hide()
    },

    save_page_style_data: function () {
        App.show_loader();
        App.poster.save_page_style_data_api().then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#pageStyle').modal('hide');
            return App.poster.get_poster_partial();
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
            App.hide_loader();
        });
    },

    save_page_style_data_api: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/projects/" + App.poster.project_id + "/poster/edit_style",
                data: {
                    header_per: $("#page_header_per").val(),
                    body_per: $("#page_body_per").val(),
                    footer_per: $("#page_footer_per").val(),
                }
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },


    save_header_image_data: function () {
        App.show_loader();
        var files = $('#headerImageFile')[0].files;
        App.poster.save_image_data_api("poster_header", files).then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#search-image-modal').modal('hide');
            return App.poster.get_poster_partial();
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
            App.hide_loader();
        });
    },

    save_footer_image_data: function () {
        App.show_loader();
        var files = $('#footerImageFile')[0].files;
        App.poster.save_image_data_api("poster_footer", files).then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#search-image-modal-footer').modal('hide');
            return App.poster.get_poster_partial();
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
            App.hide_loader();
        });
    },

    save_image_data_api: function (type, files, image_id=false) {
        return new Promise(function (resolve, reject) {
            var fd = new FormData();
            if (files){
            fd.append('file',files[0]);
            }
            else {
            fd.append("image_id", image_id)
            }
            fd.append("type", type)
            fd.append("apply_for", $("input[type='radio'][name='apply_for']:checked").val())
            $.ajax({
                method: "POST",
                url: "/projects/" + App.poster.project_id + "/poster/upload_image",
                data: fd,
                contentType: false,
                processData: false,
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },
}