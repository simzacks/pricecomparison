
$( document ).ready(function() {
    $("#item_div").hide();
});

function search_callback(results){
    $.each(results, function(i, item){
        $('<tr>').append(
            $('<td>').text(item.pk),
            $('<td>').text(item.fields.itemname),
            $('<td>').text(item.fields.quantity),
            $('<td>').text(item.fields.unitqty),
            $('<td>').text(item.fields.minprice),
            $('<td>').text(item.fields.maxprice),
            $('<td>').html(item.fields.details),
            $('<td>').html('<a href="#" onclick="return add_to_basket(' + item.pk + ')">הוסיף לסל</a>')).appendTo($("#item_table tbody"))});


//    $("#item_details").jPut({jsonData:results, name: "tbody_template"});
    $("#item_div").show();
}

function search_form(form){
    $("#item_table tbody").empty();
    search_term = $("#search_term").val();
    csrf_token = $("[name='csrfmiddlewaretoken']").val();
    data = {"search_term": search_term, 'csrfmiddlewaretoken': csrf_token}
    $.post("/compare_prices/search", data, search_callback, "json");
    return false;
}

function add_to_callback(results){
    $.each(results, function(i, item){
        $("#store"+i).html(item.fields.chainname +"<br>"+item.fields.city+"<br>"+item.fields.storename+"<br>"+item.fields.numitems + " פריטים");
        $("#price"+i).html(item.fields.totalprice);

    });
}

function add_to_basket(itemcode){
    csrf_token = $("[name='csrfmiddlewaretoken']").val();
    data = {"itemcode": itemcode, 'csrfmiddlewaretoken': csrf_token};
    $.post("/compare_prices/addtobasket", data, add_to_callback, "json");
    return false;
}


function getbasket_callback(results){
    stores = results.stores;
    items = results.items;
    prices = results.prices;
    alert(stores);
    alert(items);
    alert(prices)
    tr = $('<tr>');
    numstores = 0;
    chainstorestoreids = [];
    tr.append(
        $('<th>').text("קוד פריט"),
        $('<th>').text("פריט"),
        $('<th>').text("כמות"));
    $.each(stores, function(i, store){
        tr.append($('<th>').html(store.fields.chainname + "<br>" + store.fields.city + "<br"> + store.fields.storename));
        numstores += 1;
        chainstoreids.push(store.fields.chainstoreid);
    });
    tr.appendTo($("#basket_head"));
    body_tr = $('<tr>');
    $.each(items, function(i, item){
        body_tr.append(
            $('<td>').text(item.fields.itemcode),
            $('<td>').text(item.fields.itemname),
            $('<td>').text(item.fields.qty));
        $.each(chainstoreids, function(i, chainstoreid){
            body_tr.append($('<td id=' + chainstoreid + ">"));
        });
        body_tr.appendTo($("basket_body"));
    });
    $.each(prices, function(i, price){
        $("#" + price.pk).val(price.fields.itemprice);
    });
}

function get_basket(){
    $.get("/compare_prices/getbasket", {}, getbasket_callback, "json");
    return false;
}
