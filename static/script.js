// Product Form
const form = document.getElementById("productForm");

// Product Table
const table = document.getElementById("productTable");


// ------------------------
// Load All Products
// ------------------------

async function loadProducts() {

    const response = await fetch("/products");

    const products = await response.json();

    table.innerHTML = "";

    products.forEach(product => {

        table.innerHTML += `
        <tr>

            <td>${product.product_id}</td>
            <td>${product.product_name}</td>
            <td>₹${product.product_price}</td>
            <td>${product.product_category}</td>

            <td>
                <button
                    class="delete-btn"
                    onclick="deleteProduct(${product.product_id})">

                    Delete

                </button>
            </td>

        </tr>
        `;

    });

}


// ------------------------
// Add Product
// ------------------------

form.addEventListener("submit", async function(event){

    event.preventDefault();

    const product = {

        product_id: Number(document.getElementById("product_id").value),

        product_name: document.getElementById("product_name").value,

        product_price: Number(document.getElementById("product_price").value),

        product_category: document.getElementById("product_category").value

    };

    const response = await fetch("/products",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify(product)

    });

    const result = await response.json();

    alert(result.message || result.detail);

    form.reset();

    loadProducts();

});



// ------------------------
// Delete Product
// ------------------------

async function deleteProduct(id){

    const confirmDelete = confirm("Are you sure?");

    if(!confirmDelete){

        return;

    }

    const response = await fetch(`/products/${id}`,{

        method:"DELETE"

    });

    const result = await response.json();

    alert(result.message || result.detail);

    loadProducts();

}



// ------------------------
// Page Load
// ------------------------

loadProducts();