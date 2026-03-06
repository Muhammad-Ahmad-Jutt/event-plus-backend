4️⃣ Routes Layer

This is your controller layer.

📌 What goes inside routes/

Flask blueprints.

Think:

“How does the outside world talk to my system?”

Example:

# routes/auth_routes.py

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = auth_service.register_user(
        email=data["email"],
        password=data["password"]
    )

    return jsonify({"message": "User created"}), 201
✅ Routes Contain:

request.get_json()

calling services

returning jsonify

HTTP status codes

JWT decorators (@jwt_required)

❌ Routes Should NOT Contain:

Business logic

DynamoDB calls

Password hashing

Complex validation

Routes = thin layer