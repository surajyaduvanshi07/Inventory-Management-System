let selectedProductId = null;

window.onload = function () {
    loadProducts();
};

async function loadProducts() {

    const response = await fetch("/products");
    const products = await response.json();

    const tableBody = document.getElementById("productTableBody");
    const productCount = document.getElementById("productCount");
    const emptyState = document.getElementById("emptyState");

    tableBody.innerHTML = "";

    productCount.innerText = `${products.length} Products`;

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

        product_id: Number(document.getElementById("productId").value),

        product_name: document.getElementById("productName").value,

        product_price: Number(document.getElementById("productPrice").value),

        product_category: document.getElementById("productCategory").value

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

async function deleteProduct(id) {

    if (!confirm("Delete this Product?")) {

        return;

    }

    const response = await fetch(`/products/${id}`, {

        method: "DELETE"

    });

    const result = await response.json();

    alert(result.message || result.detail);

    loadProducts();

}
async function searchProduct() {

    const id = document.getElementById("searchId").value;

    if (id === "") {

        alert("Enter Product ID");

        return;

    }

    const response = await fetch(`/products/${id}`);

    if (!response.ok) {

        alert("Product Not Found");

        return;

    }

    const product = await response.json();

    selectedProductId = product.product_id;

    document.getElementById("productId").value = product.product_id;
    document.getElementById("productName").value = product.product_name;
    document.getElementById("productPrice").value = product.product_price;
    document.getElementById("productCategory").value = product.product_category;

}

async function editProduct(id) {

    const response = await fetch(`/products/${id}`);

    if (!response.ok) {

        alert("Product Not Found");

        return;

    }

    const product = await response.json();

    selectedProductId = product.product_id;

    document.getElementById("productId").value = product.product_id;
    document.getElementById("productName").value = product.product_name;
    document.getElementById("productPrice").value = product.product_price;
    document.getElementById("productCategory").value = product.product_category;

}

async function updateProduct() {

    if (selectedProductId === null) {

        alert("Search or Edit a Product First");

        return;

    }

    const product = {

        product_name: document.getElementById("productName").value,

        product_price: Number(document.getElementById("productPrice").value),

        product_category: document.getElementById("productCategory").value

    };

    const response = await fetch(`/products/${selectedProductId}`, {

        method: "PUT",

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

function clearForm() {

    selectedProductId = null;

    document.getElementById("productForm").reset();

    document.getElementById("searchId").value = "";

}