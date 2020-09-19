var input_file;
var reader = new FileReader();

$("#btn_upload").click(function (e) {
    e.preventDefault();
    $($("#input_file")[0]).trigger('click');
});

$("#btn_clear").click(function (e) {
    clear_canvas()
});

$('#input_file').change(function (ev) {
    ev.preventDefault();
    input_file = $('#input_file').prop('files')[0];
    reader.onload = function (event) {
        document.getElementById('image_raw').className = 'visible'
        $('#image_raw').attr('src', event.target.result);
    }
    reader.readAsDataURL(input_file);
    clear_canvas()
    $('.row-result').hide()
});


$('#btn_process').on('click', function (ev) {
    canvas = $('#drawing')[0]
    mask_b64 = canvas.toDataURL("image/png");
    form_data = new FormData();
    form_result = $('form')[0];

    $('.overlay').show()
    form_data.append('input_file', input_file);
    form_data.append('mask_b64', mask_b64);

    $.ajax({
        url: '/process',
        type: "post",
        contentType: "application/json",
        data: form_data,
        processData: false,
        contentType: false,
        crossDomain: true,
        cache: false,
        beforeSend: function () {
            $('.overlay').show()
            $('#div-result-1').html('')
            $('#div-result-2').html('')
            $('#div-result-3').html('')
            $('.row-result').hide()
        },
    }).done(function (jsondata, textStatus, jqXHR) {
        img_1 = jsondata['output_image_1']
        img_2 = jsondata['output_image_2']
        img_3 = jsondata['output_image_3']

        img_1 = window.location + '/' + img_1;
        img_2 = window.location + '/' + img_2;
        $('#div-result-1').append(`<img id='image_out_1' src="${img_1}" class="img_result" width=384 height=384>`)
        $('#div-result-2').append(`<img id='image_out_2' src="${img_2}" class="img_result" width=384 height=384>`)

        for (i = 0; i < img_3.length; i++) {
            img_path = window.location + '/' + img_3[i]
            $('#div-result-3').append(`<img id='image_out_3' src="${img_path}" class="img_result" width=384 height=384>`)
        }

        $('.overlay').hide()
        $('.row-result').css('display', 'flex')
    }).fail(function (jsondata, textStatus, jqXHR) {

        alert(jsondata['responseJSON'])
        $('.overlay').hide()
    });
})