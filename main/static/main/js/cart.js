// Зчитування та відправка замовлення у cart.js
document.getElementById('checkout-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
    if (cartItems.length === 0) {
        alert('Ваш кошик порожній!');
        return;
    }

    const cityName = document.getElementById('selected-city-name').value || document.getElementById('city-input').value.trim();
    const warehouseName = document.getElementById('warehouse-select').value;

    if (!cityName || !warehouseName) {
        alert('Будь ласка, оберіть місто та відділення зі списку!');
        return;
    }

    const payload = {
        full_name: document.getElementById('full_name').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        address: `м. ${cityName}, ${warehouseName}`,
        items: cartItems.map(item => ({
            id: item.id,
            quantity: item.quantity
        }))
    };

    fetch('/create-order/', { // ваш URL для create_order
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Замовлення успішно створено!');
            localStorage.removeItem('cart');
            window.location.href = '/shop/';
        } else {
            alert('Помилка: ' + data.message);
        }
    })
    .catch(err => {
        console.error('Помилка при створенні замовлення:', err);
        alert('Помилка з\'єднання з сервером');
    });
});