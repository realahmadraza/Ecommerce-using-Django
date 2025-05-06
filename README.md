# 🛍️ E-Commerce Django Project

A full-featured e-commerce web application built with Django, showcasing advanced Django patterns, business logic, and third-party integration. This README provides an overview, setup instructions, and details on the functionality implemented.

---

## 🚀 Features

1. **Generic Views** for clean, reusable logic across list and detail pages.
2. **Popular Products**: dynamically computed based on highest sales count.
3. **Live Sales Recording**: uses Django signals to track each order in real time.
4. **Category & Collection Filtering**: filter products by category or custom collections.
5. **All Products View**: consolidated view of every product in the catalog.
6. **Offer Filter**: view products with discounts of 20% or greater.
7. **Product Detail & Cart**: detailed product page where users can add items to the cart and proceed to purchase.
8. **Razorpay Integration**: secure online payments via Razorpay.
9. **Cart Management**: users can delete items from their cart.
10. **Search Functionality**: search products by keywords.
11. **Advanced Filters**: filter by price range, gender, and special offers.
12. **Recommendations**: personalized product recommendations based on user search history.
13. **Context Processor**: custom context processor for site-wide data (e.g., cart count, categories).
14. **Admin Panel**: full management of products, orders, and users via Django admin.
15. **Address Management**: users can add, edit, and manage multiple shipping addresses.
16. **About Page**: Dynamic page describing the site, team, or purpose.

---

## 🛠️ Technologies & Libraries

* **Framework:** Django 5.x
* **Database:** SQLite3 (default) / MySQL (optional)
* **Python:** 3.13
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
* **Payments:** Razorpay Python SDK
* **packages:** django-phonenumber-field, django-debug-toolbar = "*"

---

## 📁 Project Structure

```
Ecomm/                  # Root project folder
├── Ecomm/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/               # Main application
│   ├── migrations/
│   ├── templates/
│   │   ├── shop/
│   │   │   ├── product_list.html
│   │   │   ├── product_detail.html
│   │   │   └── about.html
│   ├── views.py        # Generic views & business logic
│   ├── models.py       # AllProduct, Order, Address, etc.
│   ├── signals.py      # Live sales recording
│   ├── context_processors.py
│   └── urls.py
├── static/             # CSS, JS, images
├── media/              # Uploaded product images
├── db.sqlite3          # Development database
├── manage.py
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   * Create a `.env` file in the project root
   * Add your Django `SECRET_KEY`, database credentials, and Razorpay keys:

     ```env
     SECRET_KEY=your_django_secret_key
     DEBUG=True
     DB_NAME=...
     DB_USER=...
     DB_PASS=...
     RAZORPAY_KEY_ID=...
     RAZORPAY_KEY_SECRET=...
     ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (for admin panel)

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Open in browser**
   Navigate to `http://127.0.0.1:8000/` to see the site.

---

## 🎯 Usage

* Browse products, apply filters, and add items to cart.
* Complete purchases using Razorpay.
* Manage your shipping addresses in your profile.
* Admin users can log in at `/admin/` to manage inventory and orders.

---

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Feature: description"`
4. Push to branch: `git push origin feature-name`
5. Open a pull request

---

## 👤 Author

**Your Name** – [GitHub Profile](https://github.com/realahmadraza)

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
