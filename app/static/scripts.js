const hideMenuOptions = () => {
    document.getElementById('add-food').style.display = 'none';
    document.getElementById('edit-food').style.display = 'none';
    document.getElementById('add-menu').style.display = 'none';
    document.getElementById('edit-menu').style.display = 'none';
};

const showForm = (form_name) => {
    hideMenuOptions();
    document.getElementById(form_name).style.display = 'block';
};