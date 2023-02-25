App.page = {
    project_id: null,
    cell_selected: null,
    page_number: null,
    current_product_id: null,
    current_source_cell_id: null,
    current_destination_cell_id: null,
    current_source_product_id: null,

    init: function (project_id, page_number) {
        App.page.page_number = page_number;
        App.page.project_id = project_id;
        App.page.init_cells();
        // App.page.init_dad();
        App.page.init_available_products_list();
        // alert("page init!");
        // $("#edit-project-product_ref_block_id").select2();
        App.page.init_available_images_list();
        App.page.init_edit_product_block_select();
    },

    init_edit_product_block_select: function () {
        $('#edit-project-product_ref_block_id').on('change', function () {
            let image_url = $('#edit-project-product_ref_block_id option[value="' + this.value + '"]').data("url");
            if (image_url) {
                $("#edit-project-product_block_image").attr("src", image_url);
                $("#edit-project-product_block_image").show();
            } else {
                $("#edit-project-product_block_image").hide();
            }
        });
    },

    init_available_products_list: function () {
        App.page.init_dad();
        App.page.init_available_products();
    },

    init_available_products: function () {
        $(".product-available-box").hover(function () {
            $(this).find(".product-available-box-over-layer").show();
        },
            function () {
                $(this).find(".product-available-box-over-layer").hide();
            });
    },

    init_available_products_dad: function () {
        $(".product-available-box").draggable({
            revert: "invalid",
            zIndex: 5,
            appendTo: 'body',
            helper: 'clone',
            handle: ".drag-indicator",
        });
        $(".proj_pg_prod_avail").droppable({
            accept: ".page_cell",
            classes: {
                "ui-droppable-hover": "highlight"
            },
            drop: function (event, ui) {
                App.page.current_source_cell_id = $(ui.draggable).data("cell-id");
                App.page.current_destination_cell_id = 0;
                App.page.current_source_product_id = 0;
                App.page.swap_cells();
            }
        });
    },

    init_dad: function () {
        $(".page_cell").draggable({
            revert: "invalid",
            handle: ".drag-indicator",
            zIndex: 5,
            helper: 'clone',
            appendTo: 'body',
        });
        $(".page_cell").droppable({
            accept: ".page_cell, .product-available-box",
            drop: function (event, ui) {
                App.page.current_source_cell_id = $(ui.draggable).data("cell-id");
                App.page.current_destination_cell_id = $(event.target).data("cell-id");
                App.page.current_source_product_id = $(ui.draggable).data("product-id");
                App.page.swap_cells();
            }
        });
        App.page.init_available_products_dad();
    },

    init_available_images_list: function () {
        App.page.init_header_image_dad();
        App.page.init_available_header_images_dad();
        App.page.init_footer_image_dad();
        App.page.init_available_footer_images_dad();
        App.page.init_full_image_dad();
        App.page.init_available_full_images_dad();
        App.page.init_half_image_dad();
        App.page.init_available_half_images_dad();
    },

    init_header_image_dad: function(){
      $(".page_name_header").droppable({
            accept: ".card_header",
            drop: function (event, ui) {
                  App.show_loader();
                  image_id = $(ui.draggable).data("image_id")
                  target = $(event.target).data("target");
                  App.page.save_image_data_api(target, false, image_id).then(function (response) {
                      if (!response.status == "edited") {
                          alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
                      }
                      return App.page.get_page_partial();
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
    init_available_header_images_dad: function () {
        $(".card_header").draggable({
            revert: "invalid",
            cursor: "crosshair",
        });
    },

    init_footer_image_dad: function(){
        $(".page_name_footer").droppable({
              accept: ".card_footer",
              drop: function (event, ui) {
                    App.show_loader();
                    image_id = $(ui.draggable).data("image_id")
                    target = $(event.target).data("target");
                    App.page.save_image_data_api(target, false, image_id).then(function (response) {
                        if (!response.status == "edited") {
                            alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
                        }
                        return App.page.get_page_partial();
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
      init_available_footer_images_dad: function () {
          $(".card_footer").draggable({
              revert: "invalid",
              cursor: "crosshair",
          });
      },

      init_full_image_dad: function(){
        $(".page_name_full_page").droppable({
              accept: ".card_full_page",
              drop: function (event, ui) {
                    App.show_loader();
                    image_id = $(ui.draggable).data("image_id")
                    target = $(event.target).data("target");
                    App.page.save_image_data_api(target, false, image_id).then(function (response) {
                        if (!response.status == "edited") {
                            alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
                        }
                        return App.page.get_page_partial();
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
      init_available_full_images_dad: function () {
          $(".card_full_page").draggable({
              revert: "invalid",
              cursor: "crosshair",
          });
      },

      init_half_image_dad: function(){
        $(".page_name_half_page").droppable({
              accept: ".card_half_page",
              drop: function (event, ui) {
                    App.show_loader();
                    image_id = $(ui.draggable).data("image_id")
                    target = $(event.target).data("target");
                    App.page.save_image_data_api(target, false, image_id).then(function (response) {
                        if (!response.status == "edited") {
                            alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
                        }
                        return App.page.get_page_partial();
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
      init_available_half_images_dad: function () {
          $(".card_half_page").draggable({
              revert: "invalid",
              cursor: "crosshair",
          });
      },

    reload: function () {
        App.page.get_page_partial().then(function (html) {
            $("#page-wrapper").html(html);
            return App.page.get_available_products_partial();
        }).then(function (html) {
            $("#available-products-list").html(html);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
        });
    },

    swap_cells: function () {
        App.show_loader();
        App.page.swap_cells_api().then(function (response) {
            return App.page.get_page_partial();
        }).then(function (html) {
            $("#page-wrapper").html(html);
            return App.page.get_available_products_partial();
        }).then(function (html) {
            $("#available-products-list").html(html);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
        });
    },

    move_cell_product_to_available_products: function (cell_id) {
        App.page.current_source_cell_id = cell_id;
        App.page.current_destination_cell_id = 0;
        App.page.current_source_product_id = 0;
        App.page.swap_cells();
    },

    swap_cells_api: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/project/swap-cells",
                data: {
                    source_cell_id: App.page.current_source_cell_id,
                    destination_cell_id: App.page.current_destination_cell_id,
                    source_product_id: (App.page.current_source_product_id == undefined ? 0 : App.page.current_source_product_id)
                }
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante lo spostamento del prodotto");
                });
        });
    },
    // Project cell functions
    add_product_to_cell: function (cell_id) {
        App.page.cell_selected = cell_id;
        App.search_product.open_search_product_modal(true);
    },
    
    
    select_product_to_add: function (catalog_product_id) {
        $('#search-product-modal').modal('hide');
        App.page.import_catalog_product_to_cell(catalog_product_id).then(function (response) {
            if (response.status == "imported") {
                return App.page.get_page_partial();
            }
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
        }).catch(function (error_message) {
            alert(error_message);
        });
    },
    
    
    import_catalog_product_to_cell: function (catalog_product_id) {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/project/import-catalog-product-to-cell",
                data: {
                    cell_id: App.page.cell_selected,
                    catalog_product_id: catalog_product_id
                }
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante l'importazione del prodotto da catalogo");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },

    // Project special cell functions
    add_image_to_cell: function (banner_id,type) {
        App.page.cell_selected = banner_id;
        App.search_product.open_search_image_modal(true,type);
    },

    select_image_to_add: function (image_id, special_cell_id, page_id, project_id, type) {
        $('#search-image-modal').modal('hide');
        $('#search-image-modal-footer').modal('hide');
        App.page.import_image_to_cell(image_id, special_cell_id, page_id, project_id, type).then(function (response) {
            if (response.status == "imported") {
                return App.page.get_page_partial();
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
                    
                    // resolve(data);
                    
                    

                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante l'importazione del prodotto da catalogo");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },
    get_page_partial: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "GET",
                url: "/project/" + App.project.project_id + "/page/" + App.page.page_number + "/partial"
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

    get_available_products_partial: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "GET",
                url: "/project/" + App.project.project_id + "/available-products/partial"
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante il recupero delle informazioni sui prodotti disponibili");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },

    init_cells: function () {
        $("#page-wrapper .page_cell").hover(function () {
            $(this).find(".page-cell-content-over-layer, .empty-cell-dropdown-layout-container").show();
        },
            function () {
                $(this).find(".page-cell-content-over-layer, .empty-cell-dropdown-layout-container").hide();
            });
    },

    delete_project_product_api: function (product_id) {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/projects/" + App.page.project_id + "/products/" + product_id + "/delete"
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante l'eliminazione del prodotto");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },


    delete_project_page_api: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/delete"
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante l'eliminazione della pagina");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },

    // show_send_to_agency_modal: function () {
    //     $("#send-to-agency-modal").modal("show");
    // },

    send_to_agency: function (delete_products) {
        $("#send-to-agency-modal").modal("hide");
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/send-to-agency";
    },

    show_delete_project_page_modal: function () {
        $("#delete-page-modal").modal("show");
    },

    delete_project_page: function (delete_products) {
        $("#delete-page-modal").modal("hide");
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/delete?delete_products=" + delete_products;
    },

    show_clear_project_page_modal: function () {
        $("#clear-page-modal").modal("show");
    },

    clear_project_page: function (delete_products) {
        $("#clear-page-modal").modal("hide");
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/clear?delete_products=" + delete_products;
    },

    show_switch_project_page_modal: function () {
        $("#switch-page-modal").modal("show");
    },

    switch_project_page: function (delete_products) {
        $("#switch-page-modal").modal("hide");
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/switch?with=" + $("#switch-page-select").val();
    },

    change_page_template: function (template_id) {
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/change-template/" + template_id;
    },

    merge_split_cells: function (cell_id, operation) {
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/cells/" + cell_id + "/merge-split/" + operation;
    },

    delete_project_product: function (product_id) {
        App.show_loader();
        App.page.delete_project_product_api(product_id).then(function (response) {
            return App.page.get_page_partial();
        }).then(function (html) {
            $("#page-wrapper").html(html);
            return App.page.get_available_products_partial();
        }).then(function (html) {
            $("#available-products-list").html(html);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
        });
    },
    edit_cell_style: function () {
        App.show_loader("#cell_style .modal-content");
        $('#cell_style').modal('show');
        App.hide_loader("#cell_style .modal-content");
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

    edit_product: function (product_id) {
        App.page.current_product_id = product_id;
        App.show_loader("#edit-project-product-modal .modal-content");
        $('#edit-project-product-modal').modal('show');
        App.page.load_product_data_api(product_id).then(function (product_data) {
            $("#edit-project-product_price").val(product_data.price);
            $("#edit-project-product_description1").val(product_data.description1);
            $("#edit-project-product_description2").val(product_data.description2);
            $("#edit-project-product_description3").val(product_data.description3);
            $("#edit-project-product_description4").val(product_data.description4);
            $("#edit-project-product_loyalty").prop("checked", product_data.loyalty);
            $("#edit-project-product_focus").prop("checked", product_data.focus);
            $("#edit-project-product_stopper").prop("checked", product_data.stopper);
            $("#edit-project-product_poster").prop("checked", product_data.poster);
            $("#edit-project-product_ref_block_id").val(product_data.ref_block_id);
            if (product_data.block_image_url) {
                $("#edit-project-product_block_image").attr("src", product_data.block_image_url);
                $("#edit-project-product_block_image").show();
            } else {
                $("#edit-project-product_block_image").hide();
            }
            $("#edit-project-product_note").val(product_data.note);
            $("#edit-project-product_price_without_discount").val(product_data.price_without_discount);
            $("#edit-project-product_tag_code").val(product_data.tag_code);
            $("#edit-project-product_discount_percentage").val(product_data.discount_percentage);
            $("#edit-project-product_pieces_number").val(product_data.pieces_number);
            $("#edit-project-product_max_purchasable_pieces").val(product_data.max_purchasable_pieces);
            $("#edit-project-product_points").val(product_data.points);
            App.hide_loader("#edit-project-product-modal .modal-content");
        }).catch(function (error_message) {
            alert(error_message);
        });
    },

    edit_product_style: function (product_id) {
        App.page.current_product_id = product_id;
        App.show_loader("#editcolorModal .modal-content");
        $('#editcolorModal').modal('show');
        App.page.load_product_style_data_api(product_id).then(function (product_data) {
            $("#priceColor").val(product_data.price_color);
            $("#describoneColor").val(product_data.description1_color);
            $("#describtwoColor").val(product_data.description2_color);
            $("#describthreeColor").val(product_data.description3_color);
            $("#describfourColor").val(product_data.description4_color);
            $("#price_style_"+product_data.price_style).prop("checked", true);
            $("#description1_style_"+product_data.description1_style).prop("checked", true);
            $("#description2_style_"+product_data.description2_style).prop("checked", true);
            $("#description3_style_"+product_data.description3_style).prop("checked", true);
            $("#description4_style_"+product_data.description4_style).prop("checked", true);
            $("#price_int_font").val(product_data.price_integer_font);
            $("#price_int_font_size").val(product_data.price_integer_font_size);
            $("#price_float_font").val(product_data.price_float_font);
            $("#price_float_font_size").val(product_data.price_float_font_size);
            $("#description1_font").val(product_data.description1_font);
            $("#description1_font_size").val(product_data.description1_font_size);
            $("#description_font").val(product_data.description_font);
            $("#description_font_size").val(product_data.description_font_size);
            App.hide_loader("#editcolorModal .modal-content");
        }).catch(function (error_message) {
            alert(error_message);
        });
    },

    load_product_data_api: function (product_id) {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "GET",
                url: "/projects/" + App.page.project_id + "/products/" + product_id
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante il caricamento dei dati del prodotto");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },

    load_product_style_data_api: function (product_id) {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "GET",
                url: "/projects/" + App.page.project_id + "/products/" + product_id +"/style"
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante il caricamento dei dati del prodotto");
                })
                .always(function () {
                    // App.hide_loader();
                });
        });
    },

    save_product_data: function () {
        App.show_loader();
        App.page.save_product_data_api().then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#edit-project-product-modal').modal('hide');
            return App.page.get_page_partial();
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
            App.hide_loader();
        });
    },

    save_product_data_api: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/projects/" + App.page.project_id + "/products/" + App.page.current_product_id + "/edit",
                data: {
                    price: $("#edit-project-product_price").val(),
                    description1: $("#edit-project-product_description1").val(),
                    description2: $("#edit-project-product_description2").val(),
                    description3: $("#edit-project-product_description3").val(),
                    description4: $("#edit-project-product_description4").val(),
                    loyalty: $("#edit-project-product_loyalty").prop("checked"),
                    focus: $("#edit-project-product_focus").prop("checked"),
                    stopper: $("#edit-project-product_stopper").prop("checked"),
                    poster: $("#edit-project-product_poster").prop("checked"),
                    // ref_block_id: $("#edit-project-product_ref_block_id").val(),
                    note: $("#edit-project-product_note").val(),
                    price_without_discount: $("#edit-project-product_price_without_discount").val(),
                    tag_code: $("#edit-project-product_tag_code").val(),
                    discount_percentage: $("#edit-project-product_discount_percentage").val(),
                    pieces_number: $("#edit-project-product_pieces_number").val(),
                    max_purchasable_pieces: $("#edit-project-product_max_purchasable_pieces").val(),
                    points: $("#edit-project-product_points").val(),
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

    save_product_style_data: function () {
        App.show_loader();
        App.page.save_product_style_data_api().then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#editcolorModal').modal('hide');
            return App.page.get_page_partial();
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
            App.hide_loader();
        });
    },

    save_product_style_data_api: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/projects/" + App.page.project_id + "/products/" + App.page.current_product_id + "/edit_style",
                data: {
                    price_color: $("#priceColor").val(),
                    description1_color: $("#describoneColor").val(),
                    description2_color: $("#describtwoColor").val(),
                    description3_color: $("#describthreeColor").val(),
                    description4_color: $("#describfourColor").val(),
                    price_style: $("input[type='radio'][name='price_style']:checked").val(),
                    description1_style: $("input[type='radio'][name='description1_style']:checked").val(),
                    description2_style: $("input[type='radio'][name='description2_style']:checked").val(),
                    description3_style: $("input[type='radio'][name='description3_style']:checked").val(),
                    description4_style: $("input[type='radio'][name='description4_style']:checked").val(),
                    price_int_font:$("#price_int_font").val(),
                    price_int_font_size:$("#price_int_font_size").val(),
                    price_float_font:$("#price_float_font").val(),
                    price_float_font_size:$("#price_float_font_size").val(),
                    description1_font:$("#description1_font").val(),
                    description1_font_size:$("#description1_font_size").val(),
                    description_font:$("#description_font").val(),
                    description_font_size:$("#description_font_size").val(),
                    apply_for: $("input[type='radio'][name='exampleRadios']:checked").val(),
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

    save_cell_style_data: function () {
        App.show_loader();
        App.page.save_cell_style_data_api().then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#cell_style').modal('hide');
            return App.page.get_page_partial();
        }).then(function (html_page) {
            $("#page-wrapper").html(html_page);
            App.hide_loader();
        }).catch(function (error_message) {
            alert(error_message);
            App.hide_loader();
        });
    },

    save_cell_style_data_api: function () {
        return new Promise(function (resolve, reject) {
            $.ajax({
                method: "POST",
                url: "/projects/" + App.page.project_id + "/page/" + App.page.page_number + "/edit_cell_style",
                data: {
                    border_width: $("#border_width").val(),
                    border_color: $("#border_color").val(),
                    border_style: $("input[type='radio'][name='borderstyle']:checked").val(),
                    apply_for: $("input[type='radio'][name='apply_for']:checked").val(),
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

    save_page_style_data: function () {
        App.show_loader();
        App.page.save_page_style_data_api().then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#pageStyle').modal('hide');
            return App.page.get_page_partial();
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
                url: "/projects/" + App.page.project_id + "/page/" + App.page.page_number + "/edit_page_style",
                data: {
                    header_per: $("#page_header_per").val(),
                    body_per: $("#page_body_per").val(),
                    footer_per: $("#page_footer_per").val(),
                    apply_for: $("input[type='radio'][name='apply_for']:checked").val(),
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
        App.page.save_image_data_api("header", files).then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#search-image-modal').modal('hide');
            return App.page.get_page_partial();
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
        App.page.save_image_data_api("footer", files).then(function (response) {
            if (!response.status == "edited") {
                alert("Spiacenti si è verificato un errore imprevisto nel salvataggio delle informazioni del prodotto")
            }
            $('#search-image-modal-footer').modal('hide');
            return App.page.get_page_partial();
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
                url: "/projects/" + App.page.project_id + "/page/" + App.page.page_number + "/upload_image",
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



    new_project_page: function (position) {
        App.show_loader();
        window.location = "/projects/" + App.page.project_id + "/pages/new?start=" + App.page.page_number + "&position=" + position;
    },

    update_page_name: function () {
        $.ajax({
            method: "POST",
            url: "/projects/" + App.page.project_id + "/pages/" + App.page.page_number + "/change-name",
            data: {
                name: $("#page-name").val()
            }
        })
            .done(function (data) {
                $("#page_nav_name_label_" + App.page.page_number).html($("#page-name").val());
            })
            .fail(function () {
            })
            .always(function () {
            });
    },
}