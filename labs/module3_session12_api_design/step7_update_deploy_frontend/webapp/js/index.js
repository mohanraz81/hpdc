var productsList = [], myCart = [], curProd = {}, cartList = []

$(document).ready(function () {
    $('.copyright').append('<span>&copy;Archeplay ' + new Date().getFullYear() + '</span>')
    // if (sessionStorage.getItem('mycart')) {
    //     myCart = JSON.parse(window.atob(sessionStorage.getItem('mycart')))
    //     $('#my-cart-count').html(myCart.length)
    // }
    if (sessionStorage.getItem('prodList')) {
        productsList = JSON.parse(window.atob(sessionStorage.getItem('prodList')))
    }
    var url_string = window.location.href;
    var url = new URL(url_string);
    var product_id = url.searchParams.get("product_id");
    var mycart = url.searchParams.get('view-cart')
    if (product_id) {
        document.title = "Product - "+product_id
        manageProductAPI({
            API: getproductbyid.API,
            type: getproductbyid.type,
            body: {
                user: user,
                id: product_id
            }
        })
        if(sessionStorage.getItem('cart-added')){
            manageProductAPI({
                API: getcart.API,
                type: getcart.type,
                body: {
                    user: user
                }
            })
        }
    }
    else if (mycart) {
        document.title = "My Cart - "+user
        manageProductAPI({
            API: getcart.API,
            type: getcart.type,
            display: true,
            body: {
                user: user
            }
        })
    }
    else {
        document.title = "Archeplay - Products"
        manageProductAPI({
            API: dumpproduct.API,
            type: dumpproduct.type
        })
        if(sessionStorage.getItem('cart-added')){
            manageProductAPI({
                API: getcart.API,
                type: getcart.type,
                body: {
                    user: user
                }
            })
        }
    }
})


// TOAST DISPLAY FUNCTION
function showToast(key, message) {
    $('.toast-body').html(message);
    $('.toast').removeClass('toast-error');
    $('.toast').removeClass('toast-success');
    $('.toast').toast('show');
    $('.toast').css('display', 'block');
    if (key == "success") {
        $('.toast').addClass('toast-success');
    }
    else if (key == "error") {
        $('.toast').addClass('toast-error');
    }
}

//API STATUS CHECK
function apiStatusCheck(response, asyncFunction) {
    if (response.status == 200 || response.Status == 200) {
        asyncFunction(true)
    }
    else {
        $('.loader-div').attr('hidden', true)
        showToast('error', response.errorMessage)
        asyncFunction(false)
        return;
    }
}

function manageProductAPI(apidata) {
    $('.loader-div').removeAttr('hidden')
    $.ajax({
        type: apidata.type,
        url: apidata.API,
        cors: false,
        contentType: "application/json",
        data: apidata.hasOwnProperty('body') == true ? JSON.stringify(apidata.body) : "",
        success: function (result) {
            apiStatusCheck(result, function (success) {
                if (success) {
                    if (apidata.API.indexOf('dumpproduct') != -1) {
                        manageProductAPI({
                            API: getallproduct.API,
                            type: getallproduct.type,
                            display: true
                        })
                    }
                    else if (apidata.API.indexOf('getallproduct') != -1) {
                        productsList = result.response.Items
                        sessionStorage.setItem('prodList', window.btoa(JSON.stringify(productsList)))
                        if (apidata.hasOwnProperty('display')) {
                            displayProducts()
                        }
                    }
                    else if (apidata.API.indexOf('addtocart') != -1) {
                        myCart.push(apidata.body.id)
                        sessionStorage.setItem("mycart", window.btoa(JSON.stringify(myCart)))
                        // $('#my-cart-count').html(myCart.length)
                        showToast('success', 'Item added to cart successfully')
                        sessionStorage.setItem('cart-added',"yes")
                        setTimeout(function () {
                            window.open('index.html?view-cart=true&user=swaminathan', "_self")
                        }, 500)
                    }
                    else if (apidata.API.indexOf('getproductbyid') != -1) {
                        curProd = result.response.Item
                        displayActiveProduct()
                    }
                    else if (apidata.API.indexOf('getcart') != -1) {
                        cartList = result.data
                        $('#my-cart-count').html(cartList.length)
                        if (apidata.hasOwnProperty('display')) {
                            displayMyCart()
                        }
                    }
                }
            })
        },
        error: function (err) {
            $('.loader-div').attr('hidden', true)
            showToast('error','Some internal error please try after some time.')
        }
    })
}

function displayProducts() {
    $('#prd-blk').empty()
    $.each(productsList, function (index, item) {
        var eachProd = $('<div class="p-3 col-xl-3 col-md-4 col-sm-6 col-xs-12 shadow-sm border d-flex flex-column justify-content-between each-prod pointer" details="' + window.btoa(JSON.stringify(item)) + '"></div>')

        // var imgSrc = "./images/" + item.image

        var prodImgCartBlk = ''

        if (myCart.indexOf(item.id) == -1) {
            prodImgCartBlk = $('<div class="row m-0"><div class="flex-row mb-2 prod-img col-12 p-1"><div class="w-100"><img alt=' + item.id + ' src="./images/' + item.image + '"/></div></div></div>')

            // <div class="col-2 p-0"><div class="bg-primary text-white p-2 d-flex align-items-center justify-content-center to-cart" details=' + window.btoa(JSON.stringify(item)) + '><span class="material-icons">add_shopping_cart</span></div></div>
        }
        else {
            prodImgCartBlk = $('<div class="row m-0"><div class="flex-row mb-2 prod-img col-12 p-1"><div class="w-100"><img alt=' + item.id + ' src="./images/' + item.image + '"/></div></div></div>')
        }

        var prodDesc = $('<div class="row m-0 align-items-center"><div class="d-flex flex-column col-12 p-1"><div class="flex-row mb-1"><div class="prod-title"><p>' + item.title + '</p></div></div><div class="flex-row mb-1"><div class="prod-id"><p>' + item.description + '</p></div></div><div class="flex-row mb-1"><div class="prod-price"><p>₹' + item.Price + '</p></div></div></div></div>')
        $(eachProd).append(prodImgCartBlk).append(prodDesc)

        $('#prd-blk').append(eachProd)
    })
    $('#prod-sec').removeAttr('hidden')
    $('.loader-div').attr('hidden', true)
}

$(document).on('click', '.each-prod', function () {
    var prodDetails = JSON.parse(window.atob($(this).attr('details')))
    window.open("index.html?product_id=" + prodDetails.id, "_self")
})

function displayActiveProduct() {
    $('#cur-prod-blk').empty()
    $('.prod-id').html(curProd.title)
    var row = $('<div class="row m-0 flex-wrap"></div>')
    var left = $('<div class="col-md-4 col-xs-12 p-4 shadow-sm border"><div class="w-100 prod-img" style="height:300px"><img alt=' + curProd.id + ' src="./images/' + curProd.image + '"/></div></div>')
    var right = $('<div class="col-md-8 col-xs-12 shadow-sm border p-0"></div>')

    var addToCart = ''

    if (myCart.indexOf(curProd.id) == -1) {
        addToCart = '<div class="bg-primary d-flex p-3 pl-5 pr-5 text-white to-cart pointer"><span class="material-icons">add_shopping_cart</span><span>Add to Cart</span></div>'
    }
    else {
        addToCart = '<div class="bg-success d-flex p-3 pl-5 pr-5 text-white"><span class="material-icons">done</span><span>Added to Cart</span></div>'
    }

    var prodDetails = $('<div class="d-flex flex-column"><div class="bg-light border-bottom p-2 d-flex align-items-center" style="height:50px"><p class="font-weight-bold h4 m-0">' + curProd.title + '</p></div><div class="p-2 d-flex flex-column justify-content-between" style="height:300px"><div><div class="mb-1"><p>' + curProd.description + '</p></div><div class="mb-1"><p>₹' + curProd.Price + '</p></div></div><div class="d-flex">' + addToCart + '</div></div></div>')

    $('#cur-prod-blk').append(row.append(left).append(right.append(prodDetails)))
    $('#cur-prod-sec').removeAttr('hidden')
    $('.loader-div').attr('hidden', true)
}

//Add to Cart
$(document).on('click', '.to-cart', function () {
    manageProductAPI({
        API: addtocart.API,
        type: addtocart.type,
        body: {
            user: user,
            id: curProd.id
        }
    })
})

//My Cart Trigger
$(document).on('click', '#my-cart', function () {
    window.open('index.html?view-cart=true&user=swaminathan', "_self")
})

//Display My Cart
function displayMyCart() {
    $('#mycart-blk').empty()
    var row = $('<div class="row m-0"></div>')
    $.each(cartList, function (index, item) {
        for (var i = 0; i < productsList.length; i++) {
            if (productsList[i].id == item.productid) {
                var eachCart = $('<div class="col-11 p-0 row m-0"></div>')
                var left = $('<div class="col-md-3 col-xs-12 p-4 shadow-sm border"><div class="w-100 prod-img" style="height:200px"><img alt=' + productsList[i].id + ' src="./images/' + productsList[i].image + '"/></div></div>')

                var right = $('<div class="col-md-9 col-xs-12 shadow-sm border p-0"></div>')

                var prodDetails = $('<div class="d-flex flex-column"><div class="bg-light border-bottom p-2 d-flex align-items-center" style="height:50px"><p class="font-weight-bold h4 m-0">' + productsList[i].title + '</p></div><div class="p-2 d-flex flex-column justify-content-between" style="height:200px"><div><div class="mb-1"><p>' + productsList[i].description + '</p></div><div class="mb-1"><p>₹' + productsList[i].Price + '</p></div></div><div class="d-flex"></div></div></div>')

                $(row).append(eachCart.append(left).append(right.append(prodDetails)))
            }
        }
    })

    $('#mycart-blk').append(row)
    $('#my-cart-sec').removeAttr('hidden')
    $('.loader-div').attr('hidden', true)
}

$(document).on('click','.to-home',function(){
    window.open('index.html','_self')
})