


function filter_results(){
  console.log('test')
  let element = document.getElementById("filters-tab");
  let hidden = element.getAttribute("hidden");

  if (hidden) {
     element.removeAttribute("hidden");
     //button.innerText = "Hide filters tab";
  } else {
     element.setAttribute("hidden", "hidden");
     //button.innerText = "Show filters tab";
  }
}


function search_results_select_rows() {
    var rows = document.getElementsByTagName("table")[0].rows;
    var rows_checked = document.getElementsByName("checkbox-item")
    console.log(rows_checked)
    var sku_list = []
    for (let i = 0; i < rows_checked.length; i++) {
        var is_checked = rows_checked[i].checked;
        console.log(is_checked)
        if (is_checked==true){
            var r = rows[i+1];
            
            var c = r.cells[1];
            var sku = c.innerHTML
            sku_list.push(sku)
        }
        //var cell = row.cells[3];
        //var value = cell.innerHTML;
        //print(value)
      }

    //s = sku_list
    console.log(sku_list)
    document.getElementById("selecteditems").value = sku_list;
    document.getElementById("selecteditems-2").value = sku_list;
    
    //"{{selected_items}}" = sku_list
    //console.log("{{selected_items}}")
  }
