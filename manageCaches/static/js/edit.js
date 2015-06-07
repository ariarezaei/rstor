function delete_cache()
{
    window.location.href = "/rapidstor/manage/remove/" + $('#id_name').val();
}

function clear_form_data()
{
    $('#id_name').val('');
}