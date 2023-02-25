App.edit_product = {

    init: function () {
        App.edit_product.init_catagory_select();
        App.edit_product.init_file_input();
    },

    init_catagory_select: function () {
        $('#edit-product-form_category').change(function () {
            App.show_loader()
            let category_id = $(this).val();
            $.ajax({
                method: "GET",
                url: "/products/subcategory-select-options",
                data: {
                    category_id: category_id
                }
            })
                .done(function (data) {
                    $("#edit-product-form_subcategory").html(data);
                })
                .fail(function () {
                    alert("Spiacenti, si è verificato un errore imprevisto durante il recupero delle sottocategorie");
                })
                .always(function () {
                    App.hide_loader();
                });
        });
    },

    init_file_input: function () {
        var imagesPreview = function (input, placeToInsertImagePreview) {

            if (input.files) {
                var filesAmount = input.files.length;

                for (i = 0; i < filesAmount; i++) {
                    var reader = new FileReader();
                    reader.filename = input.files[i].name;

                    reader.onload = function (event) {
                        let el = '<div class="col-auto"><div class="card mr-3 mb-3" style="width: 150px;"><img src="' + event.target.result + '" class="card-img-top"><div class="card-body"><p class="card-text">' + event.target.filename + '</p></div></div></div>'
                        $(placeToInsertImagePreview).append(el);
                        a = event;
                    }

                    reader.readAsDataURL(input.files[i]);
                }
            }

        };

        $('#edit-product-form_images').on('change', function () {
            imagesPreview(this, 'div.images-upload-gallery');
        });
    }

}