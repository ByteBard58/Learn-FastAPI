# FastAPI Learning

A small FastAPI project for product management (CRUD + query/filter), built while learning from a tutorial.

- **Source**: Tutorial from **Sheryians AI School**. Click [Here](https://www.youtube.com/watch?v=YxT0K5oEehk&t=1097s) to check that out.

## ✅ Project structure

```
FastAPI/
├─ app/
│  ├─ schema/
│  │  └─ product_rule.py
│  ├─ __init__.py
│  └─ app.py
├─ Data/
│  ├─ __init__.py
│  ├─ product.py
│  └─ products.json
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements.txt
```

## 🚀 Routes

- `GET /` home endpoint returning server info and example payload
- `GET /product` search by query params: `name`, `price_min`, `price_max`, `sort`, `order`
- `GET /product/{id}` fetch a single product by UUID
- `POST /product` create a product with comprehensive schema validation
- `PUT /product/{id}` update a product by UUID (partial update via `Item_put`)
- `DELETE /product/{sku}` remove a product by SKU

## 🧪 Validation highlights

- SKU pattern: `BRAND-XXXGB-###` and 3-digit suffix enforced
- `currency` limited to `INR`
- `price` > 0, `stock` >= 0
- `is_active` cannot be `True` when `stock` is `0`
- `seller` must use verified `email` and `website`, matching data from sample data
- `dimensions_cm` has computed `volume`

## ⚙️ Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

Open docs at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## 🧾 Example requests

- Get all products (with query filters):
  - `GET /product?name=xiaomi&price_min=10000&price_max=50000&sort=true&order=0`
- Get by ID:
  - `GET /product/{id}`
- Create product:
  - `POST /product` with `Item` JSON body
- Update product:
  - `PUT /product/{id}` with `Item_put` JSON body
- Delete product:
  - `DELETE /product/{sku}`

## 📌 Notes

- There is no authentication; it is a learning example.

## 😀 Thanks
Thank You for taking the time to review my work. If you have any advice or suggestion for me, feel free to email me. You can find my contact info on my [GitHub Profile Page](https://github.com/ByteBard58).

Have a great day !