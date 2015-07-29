
$( document ).ready(function() {
    $("#item_div").hide();
    $("#basket_div").hide();
    get_summary();
//    $("#item_table").DataTable();
//    $("#basket_table").DataTable();

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
            $('<td>').html('<input type="number" step="1" min="1" width="4" id="qty' + item.pk +'"> <a href="#" onclick="return add_to_basket(\'' + item.pk + '\',$(\'#qty' + item.pk + '\').val())">הוסיף לסל</a>')).appendTo($("#item_table tbody"))});


    $("#basket_div").hide();
//    $("#item_table").DataTable();
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
    for (i = 0; i < 3; i++) { 
        $("#store"+i).html("");
        $("#price"+i).html("");
    }
    $.each(results, function(i, item){
        $("#store"+i).html(item.fields.chainname +"<br>"+item.fields.city+"<br>"+item.fields.storename+"<br>"+item.fields.numitems + " פריטים");
        $("#price"+i).html(item.fields.totalprice);

    });
}

function get_summary(){
    $.get("/compare_prices/getsummary", {}, add_to_callback, "json");
    return false;
}

function add_to_basket(itemcode, qty){
    csrf_token = $("[name='csrfmiddlewaretoken']").val();
    data = {"itemcode": itemcode, "qty": qty, 'csrfmiddlewaretoken': csrf_token};
    $.post("/compare_prices/addtobasket", data, add_to_callback, "json");
    return false;
}



function getbasket_callback(results){
    stores = JSON.parse(results.stores);
    items = JSON.parse(results.items);
    prices = JSON.parse(results.prices);
    totals = JSON.parse(results.totals);
    $("#basket_head").html("");
    $("#basket_body").html("");
    tr = $('<tr>');
    tr_total = $('<tr>');
    numstores = 0;
    chainstoreids = [];
    tr.append(
        $('<th>').text("קוד פריט"),
        $('<th>').text("פריט"),
        $('<th>').text("כמות"));
    tr_total.append(
        $('<th>').text(""),
        $('<th>').text(""),
        $('<th>').text("סה\"כ"));
    $.each(stores, function(i, store){
        tr.append($('<th>').html('<a href="#" onclick="return get_basket(' + store.pk + ')">' +  store.fields.chainname + "<br>" + store.fields.city + "<br>" + store.fields.storename + '</a>'));
        numstores += 1;
        chainstoreids.push(store.pk);
        tr_total.append($('<th id="' + store.pk +'">'));

    });
    tr.appendTo($("#basket_head"));
    $.each(items, function(i, item){
        body_tr = $('<tr>');
        body_tr.append(
            $('<td>').text(item.fields.itemcode),
            $('<td>').text(item.fields.itemname),
            $('<td>').text(item.fields.qty));
        $.each(chainstoreids, function(i, chainstoreid){
            body_tr.append($('<td id=' + chainstoreid + item.fields.itemcode + ">"));
        });
        body_tr.appendTo($("#basket_body"));
    });
    tr_total.appendTo($("#basket_body"));
    $.each(prices, function(i, price){
        $("#" + price.pk).text(price.fields.itemprice);
    });
    $.each(totals, function(i, total){
        $("#" + total.pk).text(total.fields.totalprice);
    });
    $("#item_div").hide();
    $("#basket_div").show();
 //   $("#basket_table").DataTable();

}

function get_basket(storeid){
    if (storeid == undefined){
        data = {};
    }
    else {
        data = {"chainstoreid": storeid};
    }
    $.get("/compare_prices/getbasket", data, getbasket_callback, "json");
    return false;
}

function clear_basket(){
    $.get("/compare_prices/clearbasket", {}, add_to_callback, "json");
    $("#item_div").hide();
    $("#basket_div").hide();
    return false;
    }
