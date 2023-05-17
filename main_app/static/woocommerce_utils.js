function control_actions_panel() {
    console.log('control_actions_panel')
    let open_panel_button = document.getElementById("open-actions-panel-button");
    let close_panel_button = document.getElementById("close-actions-panel-button");
    let panel = document.getElementById("actions-panel");
    
    let hidden = panel.getAttribute("hidden");

    if (hidden) {
      panel.removeAttribute("hidden");
      close_panel_button.removeAttribute("hidden");
      open_panel_button.setAttribute("hidden", "hidden");
      
   } else {
      panel.setAttribute("hidden", "hidden");
      close_panel_button.setAttribute("hidden", "hidden");
      open_panel_button.removeAttribute("hidden");
      
   }
}

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