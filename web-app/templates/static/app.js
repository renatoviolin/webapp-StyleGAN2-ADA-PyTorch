var URL = 'http://192.168.100.50:8000'

$(document).on('change', '#style_image', function () {
    value = $('#style_image').find(":selected").val();
    $('#style_preview').attr('src', `${URL}/images/${value}`)
})

$(document).on('change', '#source_image', function () {
    value = $('#source_image').find(":selected").val();
    $('#source_preview').attr('src', `${URL}/images/${value}`)
})

$(document).ready(function () {
    $('#source_image').trigger('change')
    $('#style_image').trigger('change')

    $('#btn-process-style').on('click', function () {
        var form_data = new FormData();
        form_data.append('source_image', $('#source_image').find(":selected").val())
        form_data.append('style_image', $('#style_image').find(":selected").val())
        form_data.append('z_start', $('#z_start').val())
        form_data.append('z_end', $('#z_end').val())
        $.ajax({
            url: URL + '/api/process_style',
            type: "post",
            data: form_data,
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            cache: false,
            beforeSend: function () {
                $(".overlay").show()
            },
        }).done(function (jsondata, textStatus, jqXHR) {
            img_path = jsondata['image']
            start = $('#z_start').val()
            end = $('#z_end').val()
            $('#label_vector').html(`Replaced axis from Latent Vector: [${start}...${end}]`)
            $('#img_result').attr('src', `${URL}/images/generated/${img_path}`)
            $(".overlay").hide()
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $(".overlay").hide()
        });

    })

    $('#btn-process-generate').on('click', function () {
        var form_data = new FormData();
        form_data.append('seed', $('#seed').val())
        $.ajax({
            url: URL + '/api/process_generate',
            type: "post",
            data: form_data,
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            cache: false,
            beforeSend: function () {
                $(".overlay").show()
            },
        }).done(function (jsondata, textStatus, jqXHR) {
            img_path = jsondata['image']
            $('#img_result').attr('src', `${URL}/images/generated/${img_path}`)
            $(".overlay").hide()
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $(".overlay").hide()
        });

    })




    // $('#btn-process').on('click', function () {
    //     var form_data = new FormData();
    //     files = $('#input_file').prop('files')
    //     for (i = 0; i < files.length; i++)
    //         form_data.append('file', $('#input_file').prop('files')[i]);

    //     form_data.append('z_style', $('#style_target').find(":selected").val())
    //     form_data.append('z_start', $('#z_start').val())
    //     form_data.append('z_end', $('#z_end').val())
    //     $.ajax({
    //         url: URL + '/api/process',
    //         type: "post",
    //         data: form_data,
    //         enctype: 'multipart/form-data',
    //         contentType: false,
    //         processData: false,
    //         cache: false,
    //         beforeSend: function () {
    //             $(".overlay").show()
    //         },
    //     }).done(function (jsondata, textStatus, jqXHR) {

    //         console.log(jsondata)
    //         $(".overlay").hide()

    //     }).fail(function (jsondata, textStatus, jqXHR) {
    //         console.log(jsondata)
    //         $(".overlay").hide()
    //     });

    // })

})