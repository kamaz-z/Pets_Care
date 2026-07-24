const CART_KEY = 'petcare_cart';

function getCart() {
    try {
        return JSON.parse(localStorage.getItem(CART_KEY)) || [];
    } catch (e) {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function updateCartCountHeader() {
    const countElement = document.getElementById('cart-count');n 
    if (!countElement) return;
    const cart = getCart();
    countElement.innerText = cart.reduce((sum, item) => sum + item.quantity, 0);
}

/* ---------- Сторінка магазину ---------- */

function changeQuantity(button, step) {
    const card = button.closest('.product-card');
    const qtyElement = card.querySelector('.qty-number');
    let qty = parseInt(qtyElement.innerText) || 1;

    if (step === 1) {
        const max = parseInt(button.getAttribute('data-max')) || 999;
        if (qty < max) {
            qty += 1;
        } else {
            alert('На складі немає більше цього товару!');
        }
    } else if (step === -1 && qty > 1) {
        qty -= 1;
    }

    qtyElement.innerText = qty;
}

function addToCart(button) {
    const card = button.closest('.product-card');
    const id = button.getAttribute('data-id');
    const name = button.getAttribute('data-name');
    const price = parseFloat(button.getAttribute('data-price')) || 0;
    const img = button.getAttribute('data-img') || '';

    if (!id) {
        alert('Помилка: не знайдено ID товару');
        return;
    }

    const qtyElement = card.querySelector('.qty-number');
    const selectedQuantity = parseInt(qtyElement ? qtyElement.innerText : 1) || 1;

    const cart = getCart();
    const existing = cart.find(item => String(item.id) === String(id));

    if (existing) {
        existing.quantity += selectedQuantity;
    } else {
        cart.push({ id: String(id), name, price, img, quantity: selectedQuantity });
    }

    saveCart(cart);
    if (qtyElement) qtyElement.innerText = 1;
    updateCartCountHeader();
}

/* ---------- Сторінка кошика ---------- */

function renderCart() {
    const container = document.getElementById('cart-items');
    const totalElement = document.getElementById('total-price');
    const form = document.getElementById('checkout-form');
    if (!container || !totalElement) return;

    const cart = getCart();
    container.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="cart-empty">
                <div class="cart-empty-icon">🛒</div>
                <p>Ваш кошик порожній</p>
                <a href="/shop/" class="btn-link">До покупок</a>
            </div>`;
        totalElement.innerText = '0 грн';
        if (form) form.style.display = 'none';
        return;
    }

    if (form) form.style.display = 'block';

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const el = document.createElement('div');
        el.className = 'cart-item';
        el.innerHTML = `
            <div class="cart-item-img">${item.img ? `<img src="${item.img}" alt="${item.name}">` : '🛒'}</div>
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <p>${item.price} грн / шт.</p>
            </div>
            <div class="quantity-controls">
                <button type="button" onclick="updateCartQuantity('${item.id}', -1)">-</button>
                <span>${item.quantity}</span>
                <button type="button" onclick="updateCartQuantity('${item.id}', 1)">+</button>
            </div>
            <div class="cart-item-total">
                <strong>${itemTotal} грн</strong>
                <button type="button" onclick="removeFromCart('${item.id}')" class="delete-btn" title="Видалити">✕</button>
            </div>
        `;
        container.appendChild(el);
    });

    totalElement.innerText = total + ' грн';
}

function updateCartQuantity(id, step) {
    let cart = getCart();
    const item = cart.find(i => String(i.id) === String(id));
    if (!item) return;

    item.quantity += step;
    if (item.quantity <= 0) {
        cart = cart.filter(i => String(i.id) !== String(id));
    }
    saveCart(cart);
    renderCart();
    updateCartCountHeader();
}

function removeFromCart(id) {
    const cart = getCart().filter(item => String(item.id) !== String(id));
    saveCart(cart);
    renderCart();
    updateCartCountHeader();
}

function submitOrder(event) {
    event.preventDefault();

    const cart = getCart();
    if (cart.length === 0) {
        alert('Ваш кошик порожній!');
        return;
    }

    const orderData = {
        full_name: document.getElementById('full_name').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        address: document.getElementById('address').value.trim(),
        items: cart.map(item => ({ id: item.id, quantity: item.quantity })),
    };

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const submitBtn = event.target.querySelector('.btn-checkout');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Оформлюємо...';
    }

    fetch('/create-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(orderData),
    })
        .then(response => response.json().then(data => ({ ok: response.ok, data })))
        .then(({ ok, data }) => {
            if (ok && data.status === 'success') {
                alert('Дякуємо! Ваше замовлення успішно оформлено.');
                localStorage.removeItem(CART_KEY);
                window.location.href = '/';
            } else {
                alert('Помилка: ' + (data.message || 'Не вдалося оформити замовлення'));
            }
        })
        .catch(error => {
            console.error('Order error:', error);
            alert('Сталася помилка при відправці замовлення.');
        })
        .finally(() => {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerText = 'Оформити замовлення';
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    updateCartCountHeader();
    renderCart();
});