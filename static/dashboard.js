let selectedProductId = null;

window.onload = function () {

    loadProducts();

};



async function loadProducts() {

    const response = await fetch("/products");

    if (!response.ok) {

        if (response.status === 401) {

            window.location.href = "/";

        }

        return;

    }

    const products = await response.json();

    const tableBody = document.getElementById("productTableBody");

    const emptyState = document.getElementById("emptyState");

    tableBody.innerHTML = "";

    if (products.length === 0) {

        emptyState.style.display = "block";

        return;

    }

    emptyState.style.display = "none";

    products.forEach(product => {

        tableBody.innerHTML += `

        <tr>

            <td>${product.product_id}</td>

            <td>${product.product_name}</td>

            <td>₹${product.product_price}</td>

            <td>${product.product_category}</td>

            <td>

                <button

                    class="btn btn-secondary"

                    onclick="editProduct(${product.product_id})">

                    Edit

                </button>

            </td>

            <td>

                <button

                    class="btn btn-danger"

                    onclick="deleteProduct(${product.product_id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

}



async function addProduct() {

    const product = {

        product_id: Number(

            document.getElementById("productId").value

        ),

        product_name:

            document.getElementById("productName").value,

        product_price: Number(

            document.getElementById("productPrice").value

        ),

        product_category:

            document.getElementById("productCategory").value

    };



    const response = await fetch("/products", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(product)

    });

    const result = await response.json();

    alert(result.message || result.detail);

    clearForm();

    loadProducts();

}

async function searchProduct() {

    const id = document.getElementById("searchId").value;

    if (id === "") {

        alert("Please Enter Product ID");

        return;

    }

    const response = await fetch(`/products/${id}`);

    const result = await response.json();

    if (!response.ok) {

        alert(result.detail);

        return;

    }

    selectedProductId = result.product_id;

    document.getElementById("productId").value = result.product_id;

    document.getElementById("productName").value = result.product_name;

    document.getElementById("productPrice").value = result.product_price;

    document.getElementById("productCategory").value = result.product_category;

}



async function editProduct(id) {

    const response = await fetch(`/products/${id}`);

    const result = await response.json();

    if (!response.ok) {

        alert(result.detail);

        return;

    }

    selectedProductId = result.product_id;

    document.getElementById("productId").value = result.product_id;

    document.getElementById("productName").value = result.product_name;

    document.getElementById("productPrice").value = result.product_price;

    document.getElementById("productCategory").value = result.product_category;

}



async function updateProduct() {

    if (selectedProductId === null) {

        alert("Please Search or Edit a Product First");

        return;

    }

    const product = {

        product_name: document.getElementById("productName").value,

        product_price: Number(

            document.getElementById("productPrice").value

        ),

        product_category: document.getElementById("productCategory").value

    };

    const response = await fetch(

        `/products/${selectedProductId}`,

        {

            method: "PUT",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(product)

        }

    );

    const result = await response.json();

    alert(result.message || result.detail);

    clearForm();

    loadProducts();

}
async function deleteProduct(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this product?"
    );

    if (!confirmDelete) {

        return;

    }

    const response = await fetch(`/products/${id}`, {

        method: "DELETE"

    });

    const result = await response.json();

    alert(result.message || result.detail);

    loadProducts();

}



async function logout() {

    const response = await fetch("/logout");

    if (response.redirected) {

        window.location.href = response.url;

    }

    else {

        window.location.href = "/";

    }

}



function clearForm() {

    selectedProductId = null;

    document.getElementById("productId").value = "";

    document.getElementById("productName").value = "";

    document.getElementById("productPrice").value = "";

    document.getElementById("productCategory").value = "";

    document.getElementById("searchId").value = "";

}



window.addEventListener("keydown", function(event){

    if(event.key === "Enter"){

        event.preventDefault();

    }

});