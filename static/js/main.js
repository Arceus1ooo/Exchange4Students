/*function searchProducts() {
    var input = document.getElementById('searchBar').value;
    input = input.toLowerCase();
    var list = document.getElementsByClassName('products');
      
    for (var i = 0; i < list.length; i++) 
    { 
        if (list[i].innerHTML.toLowerCase().includes(input)) 
        {
            list[i].style.display="";
        }
        else {
            list[i].style.display="none";                 
        }
    }
}*/
// ^ used for search testing

function dropDown()
{
    var list = document.getElementById("productList");
    // .innerHTML and .value work in next line
    //document.getElementById("choice").innerHTML = list.options[list.selectedIndex].text;
    console.log(list.options[list.selectedIndex].text);
    return list.options[list.selectedIndex].text;
}

function display(event)
{
    var keynum = event.keyCode;
    if (keynum == 13) //presses enter
    {
        console.log(document.getElementById("choice").value);
        return document.getElementById("choice").value;
    }
}