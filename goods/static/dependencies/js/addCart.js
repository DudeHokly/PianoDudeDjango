document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart-btn").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.dataset.productId;

            fetch("{% url 'catalog:add_to_cart' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                body: `product_id=${productId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Товар добавлен в корзину!");
                } else {
                    alert("Ошибка добавления.");
                }
            });
        });
    });
});