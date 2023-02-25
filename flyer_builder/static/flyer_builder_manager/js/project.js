App.project = {
    project_id: null,
    generating_polling_interval: null,

    init: function(project_id, pdf_generation_in_progress){
        App.project.project_id = project_id;
        if (pdf_generation_in_progress)
        {
            $("#generate-pdf-link").hide();
            $("#download-pdf-link").hide();
            $("#generating-pdf-link").show();
            App.show_loader("#center");
            App.project.set_generating_polling();
        }
    },

    generate_pdf: function(){
        App.show_loader();
        App.project.save_pages_image()
    },
    generate_stopper_pdf: function(){
        App.show_loader();
        App.project.save_stopper_pages_image()
    },
    generate_poster_pdf: function(){
        App.show_loader();
        App.project.save_poster_pages_image()
    },

    set_generating_polling: function(pdf_type){
        App.project.generating_polling_interval = setInterval(App.project.check_pdf_generation, 10000 ,pdf_type);
    },

    check_pdf_generation: function(pdf_type){
        if (pdf_type=='page'){
            url="/projects/" + App.page.project_id + "/page/pdf-generating-status"
        }
        else if (pdf_type=="stopper"){
            url= "/projects/" + App.stopper.project_id + "/stopper/pdf-generating-status"

        }
        else if(pdf_type == "poster"){
            url= "/projects/" + App.poster.project_id + "/poster/pdf-generating-status"

        }

        $.ajax({
            method: "GET",
            url: url
        })
            .done(function (response) {
                if (response.status == "generated")
                {
                    clearInterval(App.project.generating_polling_interval);
                    $("#generating-pdf-link").hide();
                    $("#generate-pdf-link").show();
                    $("#pdf-generated-datetime").html(response.pdf_generation_time);
                    $("#download-pdf-link").attr("href", response.pdf_url);
                    $("#download-pdf-link").show();
                    App.hide_loader("#center");
                }
            })
            .fail(function () {
                
            });
    },

    save_pages_image: function (){
      $("#all-page").css("display", "block")
      AImgConvas=[];
      pages = []
      var numPage=1;
      $(".page-wrapper").each(function() {
          numPage++;
      });
      var indexImg=1;
      $(".page-wrapper").each(function() {
         html2canvas($(this).get(0)).then(canvas => {
            var image = new Image();
            image.src = canvas.toDataURL("image/jpeg");
            image.id = "img_convert";
            AImgConvas.push(image.src);
            pages.push($(this).data("page"));
            indexImg++;
            if(numPage==indexImg){
              var canvas_json = JSON.stringify(AImgConvas);
              page_json = JSON.stringify(pages)
              var form_data = new FormData();
              form_data.append('pages', page_json);
              form_data.append('photos', canvas_json);
              $.ajax({
                method: 'POST',
                dataType: 'text',
                cache: false,
                contentType: false,
                processData: false,
                url: '/projects/'+App.page.project_id+'/save_page',
                data: form_data,
                success: function(output) {
                  App.project.generate_pdf_api('page').then(function (response) {
                      $("#generate-pdf-link").hide();
                      $("#download-pdf-link").hide();
                      $("#generating-pdf-link").show();
                      App.project.set_generating_polling("page");
                      App.hide_loader();
                      App.show_loader("#center");
                  })
                  .catch(function (error_message) {
                      alert(error_message);
                  });
                }
              });
            }
         });
      });
      $("#all-page").css("display", "none")
      return;
    },

    save_stopper_pages_image: function (){
        AImgConvas=[];
        pages = []
        var numPage=1;
        $(".page-wrapper").each(function() {
            numPage++;
        });
        var indexImg=1;
        $(".page-wrapper").each(function() {
           html2canvas($(this).get(0)).then(canvas => {
              var image = new Image();
              image.src = canvas.toDataURL("image/jpeg");
              image.id = "img_convert";
              AImgConvas.push(image.src);
            //   pages.push($(this).data("page"));
              indexImg++;
              if(numPage==indexImg){
                var canvas_json = JSON.stringify(AImgConvas);
                page_json = JSON.stringify(pages)
                var form_data = new FormData();
                //form_data.append('pages', page_json);
                form_data.append('photos', canvas_json);
                $.ajax({
                  method: 'POST',
                  dataType: 'text',
                  cache: false,
                  contentType: false,
                  processData: false,
                  url: '/projects/'+App.stopper.project_id+'/save_stopper',
                  data: form_data,
                  success: function(output) {
                    App.project.generate_pdf_api('stopper').then(function (response) {
                        $("#generate-pdf-link").hide();
                        $("#download-pdf-link").hide();
                        $("#generating-pdf-link").show();
                        App.project.set_generating_polling('stopper');
                        App.hide_loader();
                        App.show_loader("#center");
                    })
                    .catch(function (error_message) {
                        alert(error_message);
                    });
                  }
                });
              }
           });
        });
        $("#all-page").css("display", "none")
        return;
      },

      save_poster_pages_image: function (){
        AImgConvas=[];
        pages = []
        var numPage=1;
        $(".page-wrapper").each(function() {
            numPage++;
        });
        var indexImg=1;
        $(".page-wrapper").each(function() {
           html2canvas($(this).get(0)).then(canvas => {
              var image = new Image();
              image.src = canvas.toDataURL("image/jpeg");
              image.id = "img_convert";
              AImgConvas.push(image.src);
            //   pages.push($(this).data("page"));
              indexImg++;
              if(numPage==indexImg){
                var canvas_json = JSON.stringify(AImgConvas);
                page_json = JSON.stringify(pages)
                var form_data = new FormData();
                //form_data.append('pages', page_json);
                form_data.append('photos', canvas_json);
                $.ajax({
                  method: 'POST',
                  dataType: 'text',
                  cache: false,
                  contentType: false,
                  processData: false,
                  url: '/projects/'+App.poster.project_id+'/save_poster',
                  data: form_data,
                  success: function(output) {
                    App.project.generate_pdf_api('poster').then(function (response) {
                        $("#generate-pdf-link").hide();
                        $("#download-pdf-link").hide();
                        $("#generating-pdf-link").show();
                        App.project.set_generating_polling("poster");
                        App.hide_loader();
                        App.show_loader("#center");
                    })
                    .catch(function (error_message) {
                        alert(error_message);
                    });
                  }
                });
              }
           });
        });
        $("#all-page").css("display", "none")
        return;
      },



    generate_pdf_api: function (type) {
        return new Promise(function (resolve, reject) {
            if (type == "page"){
                url = "/projects/" + App.page.project_id + "/generate-pdf"
            }
            else if(type == "stopper"){
                url = "/projects/" + App.stopper.project_id + "/generate-pdf"
            }
            else if(type == "poster"){
                url = "/projects/" + App.poster.project_id + "/generate-pdf"
            }
            $.ajax({
                method: "POST",
                url: url,
                data:{"type":type}
            })
                .done(function (data) {
                    resolve(data);
                })
                .fail(function () {
                    reject("Spiacenti, si è verificato un errore imprevisto durante la generazione del PDF");
                });
        });
    },

    show_update_products_data_by_excel_modal: function () {
        $("#update-products-data-by-excel-modal").modal("show");
    },

    update_products_data_by_excel: function(){
        if (!document.getElementById("update-products-data-by-excel-form_excel").checkValidity()) {
            document.getElementById("update-products-data-by-excel-form_excel").reportValidity();
            return;
        }

        App.show_loader();
        $("#update-products-data-by-excel-form").submit();
    
    },

    show_excel_import_report_modal: function () {
        $("#excel-import-report-modal").modal("show");
    },
}