if(document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else{
    ready()
}

// Menu Functionality
function ready() {

    var removeCartItems = document.getElementsByClassName('btn-danger')
    
    for (var i = 0; i < removeCartItems.length; i++){
        var button = removeCartItems.item(i)
        button.addEventListener('click', removeCartItem)
    }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for(var i=0; i < quantityInputs.length; i++){
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged)
    }

    var addToCart = document.getElementsByClassName('shop-item-button')
    for(var i = 0; i < addToCart.length; i++){
        var button = addToCart[i]
        button.addEventListener('click', addItemToCartClick)
    }

    document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClick)
}

function purchaseClick() {
    alert('Thank you for your purchase')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    while(cartItems.hasChildNodes()){
        cartItems.removeChild(cartItems.firstChild)
    }
    updateCartTotal()
}

function addItemToCartClick(){
    var shopItem = event.target.parentElement.parentElement
    var title = shopItem.getElementsByClassName('shop-item-title')[0].innerText
    var price = shopItem.getElementsByClassName('shop-item-price')[0].innerText
    // var imageSrc = shopItem.getElementsByClassName('shop-item-image')[0].src

    addItemToCart(title, price)
    updateCartTotal()
}

function addItemToCart(title, price){
    var cartRow = document.createElement('div')
    cartRow.classList.add('cart-row')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    var cartItemNames = cartItems.getElementsByClassName('cart-item-title')
    for(var i=0; i < cartItemNames.length; i++){
        if(cartItemNames[i].innerText == title){
            alert('This item is already added to the cart')
            return
        }
    }
    var cartRowContents = `
                <div class="cart-item cart-column">
                    <span class="cart-item-title">${title}</span>
                </div>
                <span class="cart-price cart-column">${price}</span>
                <div class="cart-quantity cart-column">
                    <input class="cart-quantity-input" type="number" value="1">
                    <button class="btn btn-danger" type="button">REMOVE</button>
                </div>`
                cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem)
    cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged)
}

function removeCartItem(){
    event.target.parentElement.parentElement.remove()
    updateCartTotal()
}

function quantityChanged(event){
    var input = event.target
    if (isNaN(input.value) || input.value <= 0){
        input.value = 1
    }
    updateCartTotal()
}

function updateCartTotal(){
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i=0; i<cartRows.length; i++){
        var cartRow = cartRows[i]
        
        var price = parseFloat(cartRow.getElementsByClassName('cart-price')[0].innerText.replace('$', ''))
        var quantity = cartRow.getElementsByClassName('cart-quantity-input')[0].value
        
        total = total + (price * quantity)
    }

    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
}