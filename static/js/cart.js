$(".update-cart").click((e) => {
  product_id = $(e.target).data("product");
  action = $(e.target).data("action");
  product_price = parseFloat($(e.target).data("price"));
  console.log("User: ", user);
  if (user == "AnonymousUser") {
    addCookieItem(product_id, action, product_price);
  } else {
    updateUserOrder(product_id, action, product_price);
  }
});

function addCookieItem(product_id, action, product_price) {
  console.log("Unauthenticated user...");
  if (action == "add") {
    if (cart[product_id] == undefined) {
      console.log("creating cookie");
      cart[product_id] = { "quantity": 1 };
    } else {
      console.log("increasing cookie");
      cart[product_id]["quantity"] += 1;
    }
    cart_number += 1

  } else if (action == "remove") {
    if (cart[product_id] == undefined) {
    } else {
      cart[product_id]["quantity"] -= 1;
    }
    if (cart[product_id]["quantity"] <= 0) {
      console.log("item should be deleted");
      delete cart[product_id];
    }
    cart_number -= 1
  }
  console.log('cart: ', cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ';domain;path=/'
  document.cookie = 'cart_number=' + JSON.stringify(cart_number) + ';domain;path=/';
  changeHTML(product_id, action, product_price, cart_number)
}

async function updateUserOrder(product_id, action, product_price) {
  console.log("user authenticated, sending data..");
  var url = "/update-item/";
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      product_id: product_id,
      action: action,
    }),
  });
  let data = await response.json();
  console.log("data: ", data);
  changeHTML(product_id, action, product_price, data)
}

function changeHTML(product_id, action, product_price, total_cart_items){
  total_items = document.querySelectorAll('.total_cart_items');
  for (i=0; i<total_items.length; i++){
    total_items[i].textContent = total_cart_items
  }

  quantity_tag = document.getElementById('quantity:'+product_id.toString())
  total_price_tag = document.getElementById('total_price:'+product_id.toString())
  total_amount_tag = document.getElementById('total_amount') 

  if (quantity_tag != undefined){
    quantity = parseInt(quantity_tag.innerHTML)
    total_price_list = (total_price_tag.textContent.trim()).split(" ")
    total_price = parseFloat(total_price_list[0])
    total_amount_list = (total_amount_tag.textContent.trim()).split(" ")
    total_amount = parseFloat(total_amount_list[0])
    if (action == 'add'){
      quantity += 1
      total_price += product_price
      total_amount += product_price
    } else if (action == 'remove'){
      quantity -= 1
      total_price -= product_price
      total_amount -= product_price
    }
    if (quantity <= 0) {
      location.reload()
    }
    quantity_tag.innerHTML = quantity;
    total_price_tag.textContent = total_price.toFixed(2)+" "+total_price_list[1];
    total_amount_tag.textContent = total_amount.toFixed(2)+" "+total_amount_list[1]
  }
}