from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(days=1)

# Admin credentials
ADMIN_USERNAME = "osamo_444"
ADMIN_PASSWORD = "kovalev311010"  # Change this in production

# Sample data for products
products = [
    {
        "id": 1,
        "name": "Nike Air Force 1",
        "category": "обувь",
        "size": "42",
        "condition": "Новое",
        "price": "12,000 ₽",
        "description": "Оригинальные Nike Air Force 1, белый цвет, размер 42. Состояние новое, в коробке.",
        "images": ["https://via.placeholder.com/300x200?text=Nike+AF1", "https://via.placeholder.com/300x200?text=Nike+AF1+Side"]
    },
    {
        "id": 2,
        "name": "Adidas Hoodie",
        "category": "одежда",
        "size": "L",
        "condition": "БУ",
        "price": "4,500 ₽",
        "description": "Черный худи Adidas, размер L. Состояние отличное, почти как новое.",
        "images": ["https://via.placeholder.com/300x200?text=Adidas+Hoodie", "https://via.placeholder.com/300x200?text=Adidas+Back"]
    },
    {
        "id": 3,
        "name": "Apple Watch Series 7",
        "category": "другое",
        "size": "Универсальный",
        "condition": "Новое",
        "price": "25,000 ₽",
        "description": "Apple Watch Series 7, 45mm, серебристый цвет. Полностью функционален.",
        "images": ["https://via.placeholder.com/300x200?text=Apple+Watch", "https://via.placeholder.com/300x200?text=Watch+Side"]
    }
]

# Base HTML template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if title %}{{ title }}{% else %}Магазин вещей{% endif %}</title>
    <style>
        :root {
            --primary-color: #0a0a0a;
            --secondary-color: #121212;
            --accent-color: #1e1e1e;
            --text-color: #f5f5f5;
            --button-color: #ff6b6b;
            --button-hover: #ff5252;
            --highlight-color: #ffd166;
            --success-color: #06d6a0;
            --border-color: #2d2d2d;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--primary-color);
            color: var(--text-color);
            line-height: 1.6;
            background-image: radial-gradient(circle at 10% 20%, rgba(255, 107, 107, 0.05) 0%, transparent 20%),
                              radial-gradient(circle at 90% 80%, rgba(6, 214, 160, 0.05) 0%, transparent 20%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background-color: var(--secondary-color);
            padding: 15px 0;
            border-bottom: 2px solid var(--accent-color);
            z-index: 100;
            text-align: center;
        }

        .header-buttons {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .btn {
            background: linear-gradient(90deg, #ff6b6b, #ff8e53, #ff6b6b);
            background-size: 200% auto;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.4s;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
            position: relative;
            overflow: hidden;
            animation: gradientShift 3s ease infinite;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
            animation: gradientShift 2s ease infinite;
        }

        .btn:active {
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
            background-size: 200% auto;
        }

        .btn-secondary:hover {
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 60%);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .btn:hover::before {
            opacity: 1;
        }

        .btn:active {
            transform: translateY(0);
        }

        .filters {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 25px;
            justify-content: space-between;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .filters::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #ffd166, #06d6a0);
            border-radius: 3px 3px 0 0;
        }

        .filter-group {
            flex: 1;
            min-width: 200px;
            position: relative;
            padding: 15px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            transition: all 0.3s;
        }

        .filter-group:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateY(-2px);
        }

        .filter-group h3 {
            margin-bottom: 12px;
            font-size: 16px;
            color: #ffffff;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .filter-group h3::before {
            content: '🔍';
            font-size: 14px;
            color: #06d6a0;
        }

        select {
            width: 100%;
            padding: 14px 16px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            font-size: 16px;
            transition: all 0.3s;
            cursor: pointer;
            backdrop-filter: blur(5px);
        }

        select:hover {
            border-color: #ffd166;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 0 2px rgba(253, 209, 102, 0.1);
        }

        select:focus {
            outline: none;
            border-color: #06d6a0;
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 0 2px rgba(6, 214, 160, 0.2);
        }

        .products-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 20px;
        }

        .product-card {
            background-color: var(--secondary-color);
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.3s;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        .product-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .product-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }

        .product-info {
            padding: 15px;
        }

        .product-name {
            font-size: 18px;
            margin-bottom: 10px;
            font-weight: bold;
            color: #ffffff;
        }

        .product-price {
            font-size: 16px;
            color: var(--success-color);
            font-weight: bold;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            overflow: auto;
        }

        .modal-content {
            background-color: var(--secondary-color);
            margin: 5% auto;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }

        .close:hover {
            color: white;
        }

        .product-images {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .product-image-large {
            width: 100%;
            max-height: 300px;
            object-fit: contain;
            border-radius: 5px;
        }

        .product-image-thumb {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 5px;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.3s;
        }

        .product-image-thumb:hover {
            border: 2px solid var(--button-color);
            transform: scale(1.05);
        }

        .important-info {
            background-color: var(--accent-color);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .important-info h2 {
            color: #ffffff;
            font-size: 32px;
            margin-bottom: 15px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        @keyframes attentionPulse {
            0% { transform: scale(1); text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); }
            50% { transform: scale(1.02); text-shadow: 0 4px 8px rgba(255, 107, 107, 0.5); }
            100% { transform: scale(1); text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); }
        }

        .important-info p {
            margin-bottom: 15px;
        }

        .expandable {
            background-color: var(--primary-color);
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s;
            border-left: 3px solid var(--button-color);
        }

        .expandable:hover {
            background-color: #111122;
            transform: translateX(5px);
        }

        .expandable-content {
            display: none;
            padding-top: 15px;
            margin-top: 15px;
            border-top: 1px solid var(--accent-color);
            animation: fadeIn 0.3s ease-in-out;
        }

        .expandable.active .expandable-content {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .admin-panel {
            background-color: var(--secondary-color);
            padding: 20px;
            border-radius: 10px;
        }

        .admin-actions {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .product-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }

        .product-item {
            background-color: var(--primary-color);
            padding: 15px;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .product-actions {
            display: flex;
            gap: 5px;
        }

        form {
            display: grid;
            gap: 15px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        input, textarea {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid var(--accent-color);
            background-color: var(--primary-color);
            color: var(--text-color);
            font-size: 16px;
        }

        .small-text {
            font-size: 12px;
            color: #aaa;
            margin-top: 10px;
        }

        @media (max-width: 768px) {
            .header-buttons {
                flex-direction: column;
                align-items: stretch;
            }

            .filters {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1 style="color: white; margin: 0; font-size: 24px; font-weight: bold;">Osamo shop</h1>
        </div>
    </header>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <!-- Important Info Modal -->
    <div id="importantInfoModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeImportantInfo()">&times;</span>
            <div class="important-info">
                <h2>ВНИМАНИЕ!</h2>
                <p>Покупая у меня вещь, вы автоматически подтверждаете что ознакомились с информацией ниже, соглашаетесь с ней и в дальнейшем не будете иметь претензий исходя из неё!</p>

                <div class="expandable" onclick="toggleExpandable(this)">
                    <h3>1) Оригинал?</h3>
                    <div class="expandable-content">
                        <p>Да, абсолютно все вещи которые я продаю, исключительно — оригинал. Любые прерки с вашей стороны, если нужно просите доп.фото. В случае если вещь оказлась фейковой — обмен/возврат в полном объёме.</p>
                    </div>
                </div>

                <div class="expandable" onclick="toggleExpandable(this)">
                    <h3>2) Оплата и доставка</h3>
                    <div class="expandable-content">
                        <p><strong>Оплата:</strong> Предоплата 100% (перевод на карту/наличка при личной встрече/крипта(usdt). Авито доставка — покрываете комиссию 9% +500 рублей.</p>
                        <p><strong>Доставка:</strong> Любыми удобными для вас способами(Сдэк/Почта/Авито) РФ/СНГ/По возможности другие страны</p>
                    </div>
                </div>

                <div class="expandable" onclick="toggleExpandable(this)">
                    <h3>3) Возврат</h3>
                    <div class="expandable-content">
                        <p>Возврат/обмен возможен только в связи с моей какой нибудь ошибкой (Отправил не ту вещь, не тот размер, не ориг, не верные замеры и т.д).</p>
                        <p>По большинству других причин возврата нет (по типу не подошел размер, не понравилось как сидит, разонравилась вещь, передумал и т.д.)</p>
                        <p>Также я не несу ответственность за состояние вещи после покупки, я не могу знать/предугадать что у вас например, порвётся рукав/появятся катышки или же отклеится подошва.</p>
                        <p>Есть как БУ вещи так и Новые, но при этом им может быть много лет, и кто знает как поведёт себя тот или иной материал спусться столько времени, предусматривайте это самостоятельно, я за это ответсвенность не несу!.</p>
                        <p>Также я не несу ответственность за вещь после отправки, это уже лежит на транспортной компании. В случае утери все претензии к ней!</p>
                        <p>Могу по вашему желанию застраховать товар (обычно ТК берут 1% от стоимости), в случае утери вам возместят всю сумму!</p>
                    </div>
                </div>

                <div class="expandable" onclick="toggleExpandable(this)">
                    <h3>4) Гарантии (не скам и т.д.)</h3>
                    <div class="expandable-content">
                        <p><strong>Отзывы:</strong> в общей сложности 250-300 отзывов в Тг+с аккаунта Авито. Можно посмотреть нажав на кнопку "Отзывы" на главной странице или же найти пост с отзывыми через закреп в канале.</p>
                        <p><strong>Авито доставка (безопасная сделка):</strong> по вашему желанию могу отправить вещь авито доставкой, но вы покрваете комиссию 9%+500 рублей</p>
                        <p>По желанию могу снять кружок/видео с вещью</p>
                    </div>
                </div>

                <div class="expandable" onclick="toggleExpandable(this)">
                    <h3>5) FAQ (частые вопросы)</h3>
                    <div class="expandable-content">
                        <p><strong>Бронь:</strong> бронирую вещь после частичной предоплаты (обычно около 10%), если передумали, то задаток не возвращается.</p>
                        <p><strong>Если долго отвечаю:</strong> Дублируйте сообщение, возможно не увидел/был занят, но обычно отвечаю при ближайшей возможности, спамить не надо!</p>
                        <p><strong>Отправка:</strong> отправляю при первой возможности когда есть время, обычно в течении суток.</p>
                        <p><strong>Нежелательные вопросы:</strong> часто пишут-где взял? за сколько взял? научи заказывать и т.д., или цена -30к, а за 15 отдашь? — НЕТ!</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showChannel() {
            window.location.href = 'https://t.me/osamo_shop';
        }

        function showReviews() {
            window.location.href = 'https://t.me/feadosamo';
        }

        function showImportantInfo() {
            document.getElementById('importantInfoModal').style.display = 'block';
        }

        function closeImportantInfo() {
            document.getElementById('importantInfoModal').style.display = 'none';
        }

        function toggleExpandable(element) {
            element.classList.toggle('active');
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('importantInfoModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

# Home page template
HOME_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
    <!-- Buttons moved from header to scroll with products -->
    <div class="header-buttons" style="margin-bottom: 20px;">
        <a href="#" class="btn btn-secondary" onclick="showChannel()">Канал</a>
        <a href="#" class="btn btn-secondary" onclick="showReviews()">Отзывы</a>
        <a href="#" class="btn btn-secondary" onclick="showImportantInfo()">⚠️ Важная информация</a>
        {% if session.get('admin_logged_in') %}
            <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary">👤 Админ панель</a>
            <a href="{{ url_for('logout') }}" class="btn btn-secondary">🔑 Выйти</a>
        {% else %}
            <a href="{{ url_for('admin_login') }}" class="btn btn-secondary">👤 Войти</a>
        {% endif %}
    </div>

    <div class="filters">
        <div class="filter-group">
            <h3>Категория</h3>
            <select id="categoryFilter" onchange="filterProducts()">
                <option value="">Все</option>
                <option value="обувь">Обувь</option>
                <option value="одежда">Одежда</option>
                <option value="другое">Другое</option>
            </select>
        </div>

        <div class="filter-group">
            <h3>Размер</h3>
            <select id="sizeFilter" onchange="filterProducts()">
                <option value="">Все</option>
                <!-- Обувь (Европейские размеры) -->
                <option value="36">36</option>
                <option value="37">37</option>
                <option value="38">38</option>
                <option value="39">39</option>
                <option value="40">40</option>
                <option value="41">41</option>
                <option value="42">42</option>
                <option value="43">43</option>
                <option value="44">44</option>
                <option value="45">45</option>
                <option value="46">46</option>
                <!-- Одежда -->
                <option value="XS">XS</option>
                <option value="S">S</option>
                <option value="M">M</option>
                <option value="L">L</option>
                <option value="XL">XL</option>
                <option value="XXL">XXL</option>
                <option value="XXXL">XXXL</option>
                <!-- Универсальные и другие -->
                <option value="Универсальный">Универсальный</option>
                <option value="One Size">One Size</option>
                <option value="Free Size">Free Size</option>
            </select>
        </div>

        <div class="filter-group">
            <h3>Состояние</h3>
            <select id="conditionFilter" onchange="filterProducts()">
                <option value="">Все</option>
                <option value="Новое">Новое</option>
                <option value="БУ">БУ</option>
            </select>
        </div>
    </div>

    <div class="products-grid" id="productsGrid">
        {% for product in products %}
        <div class="product-card" onclick="window.location.href='/product/{{ product.id }}'">
            <img src="{{ product.images[0] }}" alt="{{ product.name }}" class="product-image">
            <div class="product-info">
                <div class="product-name">{{ product.name }}</div>
                <div class="product-price">{{ product.price }}</div>
            </div>
        </div>
        {% endfor %}
        </div>
    </div>

    <!-- Product Carousel Modal -->
    <div id="productCarouselModal" class="modal">
        <div class="modal-content" style="max-width: 900px;">
            <span class="close" onclick="closeProductCarousel()">&times;</span>
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 id="carouselProductName" style="color: white; font-size: 24px; margin-bottom: 10px;"></h2>
            </div>
            <div style="position: relative;">
                <div id="productCarousel" style="display: flex; overflow: hidden; border-radius: 10px;">
                    <!-- Images will be inserted here by JavaScript -->
                </div>
                <button onclick="previousImage()" style="position: absolute; left: 10px; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 20px;">←</button>
                <button onclick="nextImage()" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 20px;">→</button>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <a id="viewProductDetails" href="#" class="btn" style="display: inline-block;">Посмотреть детали</a>
            </div>
        </div>
    </div>

    <script>
        // Carousel variables
        let currentProductId = null;
        let currentImages = [];
        let currentIndex = 0;

        function showProductCarousel(productId, productName, imagesString) {
            // Parse the images string back to array
            currentImages = imagesString.split(',');
            currentProductId = productId;
            currentIndex = 0;

            // Set product name
            document.getElementById('carouselProductName').textContent = productName;

            // Set view details link
            document.getElementById('viewProductDetails').href = '/product/' + productId;

            // Show first image
            showCurrentImage();

            // Show modal
            document.getElementById('productCarouselModal').style.display = 'block';
        }

        function showCurrentImage() {
            const carousel = document.getElementById('productCarousel');
            carousel.innerHTML = '';

            // Create image element
            const img = document.createElement('img');
            img.src = currentImages[currentIndex];
            img.style.width = '100%';
            img.style.height = '400px';
            img.style.objectFit = 'contain';
            img.style.borderRadius = '10px';

            carousel.appendChild(img);
        }

        function nextImage() {
            currentIndex = (currentIndex + 1) % currentImages.length;
            showCurrentImage();
        }

        function previousImage() {
            currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
            showCurrentImage();
        }

        function closeProductCarousel() {
            document.getElementById('productCarouselModal').style.display = 'none';
        }

        function filterProducts() {
            const category = document.getElementById('categoryFilter').value;
            const size = document.getElementById('sizeFilter').value;
            const condition = document.getElementById('conditionFilter').value;

            fetch('/filter_products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: category,
                    size: size,
                    condition: condition
                })
            })
            .then(response => response.json())
            .then(data => {
                const productsGrid = document.getElementById('productsGrid');
                productsGrid.innerHTML = '';

                data.products.forEach(product => {
                    const productCard = `
                        <div class="product-card" onclick="window.location.href='/product/${product.id}'">
                            <img src="${product.images[0]}" alt="${product.name}" class="product-image">
                            <div class="product-info">
                                <div class="product-name">${product.name}</div>
                                <div class="product-price">${product.price}</div>
                            </div>
                        </div>
                    `;
                    productsGrid.innerHTML += productCard;
                });
            })
            .catch(error => {
                console.error('Error filtering products:', error);
            });
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('productCarouselModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
{% endblock %}
'''

# Product detail template
PRODUCT_DETAIL_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
    <div class="header-buttons" style="margin-bottom: 20px;">
        <a href="{{ url_for('home') }}" class="btn btn-secondary">← Назад к товарам</a>
        <a href="#" class="btn btn-secondary" onclick="showChannel()">Канал</a>
        <a href="#" class="btn btn-secondary" onclick="showReviews()">Отзывы</a>
        <a href="#" class="btn btn-secondary" onclick="showImportantInfo()">⚠️ Важная информация</a>
        {% if session.get('admin_logged_in') %}
            <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary">👤 Админ панель</a>
            <a href="{{ url_for('logout') }}" class="btn btn-secondary">🔑 Выйти</a>
        {% else %}
            <a href="{{ url_for('admin_login') }}" class="btn btn-secondary">👤 Войти</a>
        {% endif %}
    </div>

    <div class="product-detail">
        <div class="product-images">
            {% for image in product.images %}
            <img src="{{ image }}" alt="{{ product.name }}" class="product-image-large" onclick="showProductCarousel({{ product.id }}, '{{ product.name }}', '{{ product.images|join(',') }}')">
            {% endfor %}
        </div>
        
        <div class="product-info">
            <h1>{{ product.name }}</h1>
            <p><strong>Категория:</strong> {{ product.category }}</p>
            <p><strong>Размер:</strong> {{ product.size }}</p>
            <p><strong>Состояние:</strong> {{ product.condition }}</p>
            <p><strong>Цена:</strong> <span style="color: var(--success-color); font-weight: bold;">{{ product.price }}</span></p>
            <p><strong>Описание:</strong></p>
            <p>{{ product.description }}</p>
        </div>
    </div>

    <script>
        function showProductCarousel(productId, productName, imagesString) {
            // Parse the images string back to array
            const images = imagesString.split(',');
            let currentIndex = 0;

            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.style.display = 'block';

            modal.innerHTML = `
                <div class="modal-content" style="max-width: 900px;">
                    <span class="close" onclick="this.parentElement.parentElement.style.display='none'">&times;</span>
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h2 style="color: white; font-size: 24px; margin-bottom: 10px;">${productName}</h2>
                    </div>
                    <div style="position: relative;">
                        <div id="carousel" style="display: flex; overflow: hidden; border-radius: 10px;">
                            <img src="${images[0]}" style="width: 100%; height: 400px; object-fit: contain; border-radius: 10px;">
                        </div>
                        <button onclick="this.parentElement.querySelector('#carousel').innerHTML = '<img src=\'' + images[(currentIndex - 1 + images.length) % images.length] + '\' style=\'width: 100%; height: 400px; object-fit: contain; border-radius: 10px;>'; currentIndex = (currentIndex - 1 + images.length) % images.length;" style="position: absolute; left: 10px; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 20px;">←</button>
                        <button onclick="this.parentElement.querySelector('#carousel').innerHTML = '<img src=\'' + images[(currentIndex + 1) % images.length] + '\' style=\'width: 100%; height: 400px; object-fit: contain; border-radius: 10px;>'; currentIndex = (currentIndex + 1) % images.length;" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 20px;">→</button>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            // Close modal when clicking outside
            modal.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            };
        }
    </script>
{% endblock %}
'''

# Admin login template
ADMIN_LOGIN_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
    <div class="header-buttons" style="margin-bottom: 20px;">
        <a href="{{ url_for('home') }}" class="btn btn-secondary">← Назад к товарам</a>
    </div>

    <div style="max-width: 400px; margin: 50px auto;">
        <h2 style="text-align: center; margin-bottom: 30px; color: white;">Админ панель</h2>
        <form method="POST" action="{{ url_for('admin_auth') }}">
            <div class="form-group">
                <label for="username">Логин:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Пароль:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn" style="width: 100%;">Войти</button>
        </form>
    </div>
{% endblock %}
'''

# Admin panel template
ADMIN_PANEL_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
    <div class="header-buttons" style="margin-bottom: 20px;">
        <a href="{{ url_for('home') }}" class="btn btn-secondary">← Назад к товарам</a>
        <a href="{{ url_for('add_product') }}" class="btn">➕ Добавить товар</a>
        <a href="{{ url_for('logout') }}" class="btn btn-secondary">🔑 Выйти</a>
    </div>

    <div class="admin-panel">
        <h2>Админ панель</h2>
        <div class="product-list">
            {% for product in products %}
            <div class="product-item">
                <div>
                    <h3>{{ product.name }}</h3>
                    <p>{{ product.category }} • {{ product.size }} • {{ product.condition }}</p>
                    <p style="color: var(--success-color); font-weight: bold;">{{ product.price }}</p>
                </div>
                <div class="product-actions">
                    <a href="{{ url_for('edit_product', product_id=product.id) }}" class="btn btn-secondary">✏️ Редактировать</a>
                    <a href="{{ url_for('delete_product', product_id=product.id) }}" class="btn" style="background: #ff4757;">🗑️ Удалить</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
{% endblock %}
'''

# Add product template
ADD_PRODUCT_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
    <div class="header-buttons" style="margin-bottom: 20px;">
        <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary">← Назад</a>
    </div>

    <div class="admin-panel">
        <h2>Добавить товар</h2>
        <form method="POST">
            <div class="form-group">
                <label for="name">Название:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="category">Категория:</label>
                <select id="category" name="category" required>
                    <option value="обувь">Обувь</option>
                    <option value="одежда">Одежда</option>
                    <option value="другое">Другое</option>
                </select>
            </div>
            <div class="form-group">
                <label for="size">Размер:</label>
                <input type="text" id="size" name="size" required>
            </div>
            <div class="form-group">
                <label for="condition">Состояние:</label>
                <select id="condition" name="condition" required>
                    <option value="Новое">Новое</option>
                    <option value="БУ">БУ</option>
                </select>
            </div>
            <div class="form-group">
                <label for="price">Цена:</label>
                <input type="text" id="price" name="price" required>
            </div>
            <div class="form-group">
                <label for="description">Описание:</label>
                <textarea id="description" name="description" rows="4" required></textarea>
            </div>
            <div class="form-group">
                <label>Изображения (URL):</label>
                <input type="text" name="image1" placeholder="URL изображения 1">
                <input type="text" name="image2" placeholder="URL изображения 2">
                <input type="text" name="image3" placeholder="URL изображения 3">
                <input type="text" name="image4" placeholder="URL изображения 4">
                <input type="text" name="image5" placeholder="URL изображения 5">
                <p class="small-text">Введите URL изображений (можно несколько). Используйте https://placeholder.com для заглушки.</p>
            </div>
            <button type="submit" class="btn">Добавить товар</button>
        </form>
    </div>
{% endblock %}
'''

# Edit product template
EDIT_PRODUCT_TEMPLATE = BASE_TEMPLATE + '''
{% block content %}
    <div class="header-buttons" style="margin-bottom: 20px;">
        <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary">← Назад</a>
    </div>

    <div class="admin-panel">
        <h2>Редактировать товар</h2>
        <form method="POST">
            <div class="form-group">
                <label for="name">Название:</label>
                <input type="text" id="name" name="name" value="{{ product.name }}" required>
            </div>
            <div class="form-group">
                <label for="category">Категория:</label>
                <select id="category" name="category" required>
                    <option value="обувь" {% if product.category == 'обувь' %}selected{% endif %}>Обувь</option>
                    <option value="одежда" {% if product.category == 'одежда' %}selected{% endif %}>Одежда</option>
                    <option value="другое" {% if product.category == 'другое' %}selected{% endif %}>Другое</option>
                </select>
            </div>
            <div class="form-group">
                <label for="size">Размер:</label>
                <input type="text" id="size" name="size" value="{{ product.size }}" required>
            </div>
            <div class="form-group">
                <label for="condition">Состояние:</label>
                <select id="condition" name="condition" required>
                    <option value="Новое" {% if product.condition == 'Новое' %}selected{% endif %}>Новое</option>
                    <option value="БУ" {% if product.condition == 'БУ' %}selected{% endif %}>БУ</option>
                </select>
            </div>
            <div class="form-group">
                <label for="price">Цена:</label>
                <input type="text" id="price" name="price" value="{{ product.price }}" required>
            </div>
            <div class="form-group">
                <label for="description">Описание:</label>
                <textarea id="description" name="description" rows="4" required>{{ product.description }}</textarea>
            </div>
            <div class="form-group">
                <label>Изображения (URL):</label>
                {% for i in range(5) %}
                <input type="text" name="image{{ i+1 }}" placeholder="URL изображения {{ i+1 }}" value="{{ product.images[i] if i < product.images|length else '' }}">
                {% endfor %}
                <p class="small-text">Введите URL изображений (можно несколько). Используйте https://placeholder.com для заглушки.</p>
            </div>
            <button type="submit" class="btn">Сохранить изменения</button>
        </form>
    </div>
{% endblock %}
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE, products=products, session=session)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template_string(PRODUCT_DETAIL_TEMPLATE, product=product, session=session)
    return redirect(url_for('home'))

@app.route('/admin')
def admin_login():
    return render_template_string(ADMIN_LOGIN_TEMPLATE, session=session)

@app.route('/admin/login', methods=['POST'])
def admin_auth():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        session.permanent = True
        return redirect(url_for('admin_panel'))
    return redirect(url_for('admin_login'))

@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template_string(ADMIN_PANEL_TEMPLATE, products=products, session=session)

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        images = []
        for i in range(1, 6):
            image_url = request.form.get(f'image{i}')
            if image_url:
                images.append(image_url)

        new_product = {
            "id": len(products) + 1,
            "name": request.form.get('name'),
            "category": request.form.get('category'),
            "size": request.form.get('size'),
            "condition": request.form.get('condition'),
            "price": request.form.get('price'),
            "description": request.form.get('description'),
            "images": images if images else ["https://via.placeholder.com/300x200?text=No+Image"]
        }
        products.append(new_product)
        return redirect(url_for('admin_panel'))

    return render_template_string(ADD_PRODUCT_TEMPLATE, session=session)

@app.route('/admin/delete_product/<int:product_id>')
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    global products
    products = [p for p in products if p['id'] != product_id]
    return redirect(url_for('admin_panel'))

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        # Update basic product info
        product['name'] = request.form.get('name')
        product['category'] = request.form.get('category')
        product['size'] = request.form.get('size')
        product['condition'] = request.form.get('condition')
        product['price'] = request.form.get('price')
        product['description'] = request.form.get('description')

        # Update images - collect all 5 image URLs
        images = []
        for i in range(1, 6):
            image_url = request.form.get(f'image{i}')
            if image_url:  # Only add non-empty image URLs
                images.append(image_url)

        # Ensure at least one image
        product['images'] = images if images else ["https://via.placeholder.com/300x200?text=No+Image"]

        return redirect(url_for('admin_panel'))

    return render_template_string(EDIT_PRODUCT_TEMPLATE, product=product, session=session)

@app.route('/filter_products', methods=['POST'])
def filter_products():
    data = request.get_json()
    category = data.get('category', '')
    size = data.get('size', '')
    condition = data.get('condition', '')

    filtered_products = products

    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    if size:
        filtered_products = [p for p in filtered_products if p['size'] == size]
    if condition:
        filtered_products = [p for p in filtered_products if p['condition'] == condition]

    return jsonify({'products': filtered_products})

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)