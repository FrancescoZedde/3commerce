const modal_instagram = document.getElementById("modal-instagram");
const close_modal_0 = document.getElementsByClassName("close")[0];

close_modal_0.onclick = function() {
    modal_instagram.style.display = "none";
}
    
window.onclick = function(event) {
    if (event.target == modal_instagram) {
        modal_instagram.style.display = "none";
    }
}

function retrieve_button_id_and_show_modal(clicked_id){
    console.log(clicked_id);
    let open_instagram_modal = document.getElementById(clicked_id);
    modal_instagram.style.display = "block";
    let product_id = clicked_id.replace('open-instagram-modal-','');
    document.getElementById("ig-selected-item").value = product_id;
    console.log(document.getElementById("ig-selected-item").value);
}


function select_deselect_all_rows() {
    //var rows = document.getElementsByTagName("table")[0].rows;
    var rows_checked = document.getElementsByName("checkbox-item")
    let select_all_button = document.getElementById("select-all-button");
    let deselect_all_button = document.getElementById("deselect-all-button");

    let hidden = select_all_button.getAttribute("hidden");

    if (hidden) {
        select_all_button.removeAttribute("hidden");
        deselect_all_button.setAttribute("hidden", "hidden");
        rows_checked.forEach((checkbox) => {
            checkbox.checked = false;
        });
     } else {
        select_all_button.setAttribute("hidden", "hidden");
        deselect_all_button.removeAttribute("hidden");
        rows_checked.forEach((checkbox) => {
            checkbox.checked = true;
        });
     }

    //select_rows()
}