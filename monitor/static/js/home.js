function edit_modal(e)
{
    $('#edit-modal').show();
    e.stopPropagation();
}

function close_modal()
{
    $('#edit-modal').hide();
}


function load_edit()
{
    window.location.href = "/rapidstor/manage/edit/" + $('#cache-name').val();
}
