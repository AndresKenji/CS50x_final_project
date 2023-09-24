

function showForm(form_name){
    document.getElementById('add-food').style.display = 'none';
    document.getElementById('edit-food').style.display = 'none';
    document.getElementById('add-menu').style.display = 'none';
    document.getElementById('edit-menu').style.display = 'none';

    document.getElementById(form_name).style.display = 'block';

}
