$(document).ready(function () {

    function sorting(e){
        search_value = $('#search-val').text()
        category_value = $('#cat-val').text()

        $.ajax({
            method: 'GET',
            url: $('#sorting-form').attr('action'),
            data: {
                'sorting': $(this).val(),
                'search_value': search_value,
                'category_value': category_value,
                },
            dataType: 'json',
            success: function (response) {
                console.log(response)
                $('#list-table').html(response['html']);

            },
        })
    }

    $('#id_sorting').change(sorting);
})