function delete_cache()
{
    window.location.href = "/manage/remove/" + $('#id_name').val();
}

function clear_form_data()
{
    $('#id_name').val('');
}