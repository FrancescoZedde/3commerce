
var s = '{{selected_rows}}';
var s = '{{selected_items_delete}}';


function open_actions_panel() {

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

    select_rows()
}



function select_rows() {
    console.log('ciao')
    var rows = document.getElementsByTagName("table")[0].rows;
    var rows_checked = document.getElementsByName("checkbox-item")
    console.log(rows_checked)
    var sku_list = []
    for (let i = 0; i < rows_checked.length; i++) {
        var is_checked = rows_checked[i].checked;
        console.log(is_checked)
        if (is_checked==true){
            var r = rows[i+1];
            
            
            var c = r.cells[2];
            var sku = c.innerHTML
            sku_list.push(sku)
        }
        //var cell = row.cells[3];
        //var value = cell.innerHTML;
        //print(value)
    }

    //s = sku_list
    var selected_items_hidden_inputs = document.getElementsByName("selected-items")
    selected_items_hidden_inputs.forEach(
        function(element) {
            element.value = sku_list;
            console.log(element.value)
        }
    )
    console.log('ciao')
    document.getElementById("selecteditems").value = sku_list;
    document.getElementById("selecteditemsdelete").value = sku_list;
    document.getElementById("selecteditemsadddefaulttemplate").value = sku_list;
    document.getElementById("selecteditemswoocommerce").value = sku_list;
    document.getElementById("selecteditemsebay").value = sku_list;


    console.log('document.getElementById("selecteditemsebay").value')
    console.log(document.getElementById("selecteditemsebay").value)
    //console.log(document.getElementById("selecteditemsdelete").value)
    //document.getElementById("selecteditemsdelete").value = sku_list;
    //console.log('selecteditemsdelete values.')
    //console.log(document.getElementById("selecteditemsdelete").value)
    //"{{selected_items}}" = sku_list
    //console.log("{{selected_items}}")
    
  }


  