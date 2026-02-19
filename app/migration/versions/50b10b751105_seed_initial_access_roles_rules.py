"""Seed initial RBAC data: business_elements, roles, access_rules

Revision ID: 2026_02_18_seed_rbac_data
Revises: 219951375a43
Create Date: 2026-02-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, text
from datetime import datetime

# Revision identifiers
revision = '2026_02_18_seed_rbac_data'
down_revision = '219951375a43'
branch_labels = None
depends_on = None

now = datetime.utcnow()


def upgrade() -> None:
    conn = op.get_bind()

    # ───────────────────────────────────────────────
    # 1. Business Elements (ресурсы / сущности)
    # ───────────────────────────────────────────────
    business_elements_tbl = table(
        "business_elements",
        column("id", sa.Integer),
        column("name", sa.String),
        column("description", sa.String),
        column("created_at", sa.DateTime),
        column("updated_at", sa.DateTime),
    )

    result = conn.execute(text("SELECT COUNT(*) FROM business_elements"))
    if result.scalar() == 0:
        op.bulk_insert(
            business_elements_tbl,
            [
                {"name": "User",       "description": "Пользователи",              "created_at": now, "updated_at": now},
                {"name": "Product",    "description": "Товары",                    "created_at": now, "updated_at": now},
                {"name": "Order",      "description": "Заказы",                    "created_at": now, "updated_at": now},
                {"name": "Review",     "description": "Отзывы",                    "created_at": now, "updated_at": now},
                {"name": "Category",   "description": "Категории",                 "created_at": now, "updated_at": now},
                {"name": "AccessRule", "description": "Правила доступа (RBAC)",    "created_at": now, "updated_at": now},
            ],
        )
        print("→ Добавлены business_elements")


    # ───────────────────────────────────────────────
    # 2. Roles
    # ───────────────────────────────────────────────
    roles_tbl = table(
        "roles",
        column("id", sa.Integer),
        column("name", sa.String),
        column("description", sa.String),
        column("created_at", sa.DateTime),
        column("updated_at", sa.DateTime),
    )

    result = conn.execute(text("SELECT COUNT(*) FROM roles"))
    if result.scalar() == 0:
        op.bulk_insert(
            roles_tbl,
            [
                {"name": "admin",     "description": "Полный доступ",                              "created_at": now, "updated_at": now},
                {"name": "moderator", "description": "Модератор контента",                         "created_at": now, "updated_at": now},
                {"name": "seller",    "description": "Продавец",                                   "created_at": now, "updated_at": now},
                {"name": "buyer",     "description": "Покупатель (зарегистрированный пользователь)", "created_at": now, "updated_at": now},
                {"name": "guest",     "description": "Гость (неавторизованный пользователь)",      "created_at": now, "updated_at": now},
            ],
        )
        print("→ Добавлены роли")


    # ───────────────────────────────────────────────
    # 3. Access Roles Rules
    # ───────────────────────────────────────────────
    elements = conn.execute(
        text("SELECT id, name FROM business_elements")
    ).fetchall()

    roles_dict = dict(
        conn.execute(text("SELECT name, id FROM roles")).fetchall()
    )

    element_map = {row[1]: row[0] for row in elements}  # name → id

    if not element_map or not roles_dict:
        return

    rules = []

    # ───────────────────────────────────────────────
    # Полные права для admin
    # ───────────────────────────────────────────────
    admin_id = roles_dict.get("admin")
    if admin_id:
        for elem_name in ["User", "Product", "Order", "Review", "Category", "AccessRule"]:
            elem_id = element_map.get(elem_name)
            if elem_id:
                rules.append({
                    "role_id": admin_id,
                    "element_id": elem_id,
                    "read": True, "read_all": True,
                    "create": True,
                    "update": True, "update_all": True,
                    "delete": True, "delete_all": True,
                    "created_at": now, "updated_at": now,
                })

    # ───────────────────────────────────────────────
    # Moderator
    # ───────────────────────────────────────────────
    moderator_id = roles_dict.get("moderator")
    if moderator_id:
        # User
        rules.append({
            "role_id": moderator_id, "element_id": element_map.get("User"),
            "read": True, "read_all": True,
            "create": False,
            "update": True, "update_all": False,
            "delete": True, "delete_all": False,
            "created_at": now, "updated_at": now,
        })
        # Product
        rules.append({
            "role_id": moderator_id, "element_id": element_map.get("Product"),
            "read": True, "read_all": True,
            "create": False,
            "update": True, "update_all": True,
            "delete": True, "delete_all": True,
            "created_at": now, "updated_at": now,
        })
        # Review
        rules.append({
            "role_id": moderator_id, "element_id": element_map.get("Review"),
            "read": True, "read_all": True,
            "create": False,
            "update": True, "update_all": True,
            "delete": True, "delete_all": True,
            "created_at": now, "updated_at": now,
        })

    # ───────────────────────────────────────────────
    # Seller
    # ───────────────────────────────────────────────
    seller_id = roles_dict.get("seller")
    if seller_id:
        # Product — свои товары
        rules.append({
            "role_id": seller_id, "element_id": element_map.get("Product"),
            "read": True, "read_all": False,
            "create": True,
            "update": True, "update_all": False,
            "delete": True, "delete_all": False,
            "created_at": now, "updated_at": now,
        })
        # Order — свои заказы
        rules.append({
            "role_id": seller_id, "element_id": element_map.get("Order"),
            "read": True, "read_all": False,
            "create": False,
            "update": True, "update_all": False,
            "delete": False, "delete_all": False,
            "created_at": now, "updated_at": now,
        })
        # Review — свои отзывы или модерация
        rules.append({
            "role_id": seller_id, "element_id": element_map.get("Review"),
            "read": True, "read_all": False,
            "create": True,
            "update": True, "update_all": False,
            "delete": True, "delete_all": False,
            "created_at": now, "updated_at": now,
        })

    # ───────────────────────────────────────────────
    # Buyer (покупатель)
    # ───────────────────────────────────────────────
    buyer_id = roles_dict.get("buyer")
    if buyer_id:
        # Product — просмотр каталога
        rules.append({
            "role_id": buyer_id, "element_id": element_map.get("Product"),
            "read": True, "read_all": True,
            "create": False, "update": False, "update_all": False,
            "delete": False, "delete_all": False,
            "created_at": now, "updated_at": now,
        })
        # Order — свои заказы
        rules.append({
            "role_id": buyer_id, "element_id": element_map.get("Order"),
            "read": True, "read_all": False,
            "create": True,
            "update": True, "update_all": False,
            "delete": True, "delete_all": False,
            "created_at": now, "updated_at": now,
        })
        # Review — свои отзывы
        rules.append({
            "role_id": buyer_id, "element_id": element_map.get("Review"),
            "read": True, "read_all": True,
            "create": True,
            "update": True, "update_all": False,
            "delete": True, "delete_all": False,
            "created_at": now, "updated_at": now,
        })

    # ───────────────────────────────────────────────
    # Guest (неавторизованный)
    # ───────────────────────────────────────────────
    guest_id = roles_dict.get("guest")
    if guest_id:
        # Только просмотр
        for elem_name in ["Product", "Category", "Review"]:
            elem_id = element_map.get(elem_name)
            if elem_id:
                rules.append({
                    "role_id": guest_id,
                    "element_id": elem_id,
                    "read": True, "read_all": True,
                    "create": False,
                    "update": False, "update_all": False,
                    "delete": False, "delete_all": False,
                    "created_at": now, "updated_at": now,
                })

    # ───────────────────────────────────────────────
    # Вставка всех правил (с предварительной очисткой)
    # ───────────────────────────────────────────────
    if rules:
        rules_tbl = table(
            "access_roles_rules",
            column("role_id", sa.Integer),
            column("element_id", sa.Integer),
            column("read", sa.Boolean),
            column("read_all", sa.Boolean),
            column("create", sa.Boolean),
            column("update", sa.Boolean),
            column("update_all", sa.Boolean),
            column("delete", sa.Boolean),
            column("delete_all", sa.Boolean),
            column("created_at", sa.DateTime),
            column("updated_at", sa.DateTime),
        )

        # Очистка старых записей для этих ролей (на всякий случай)
        conn.execute(
            text("DELETE FROM access_roles_rules WHERE role_id IN (SELECT id FROM roles)")
        )

        op.bulk_insert(rules_tbl, rules)
        print(f"→ Добавлено {len(rules)} правил доступа")


def downgrade() -> None:
    # Опционально: удаление добавленных записей
    conn = op.get_bind()
    conn.execute(text("DELETE FROM access_roles_rules WHERE role_id IN (SELECT id FROM roles)"))
    conn.execute(text("DELETE FROM roles WHERE name IN ('admin', 'moderator', 'seller', 'buyer', 'guest')"))
    conn.execute(text("DELETE FROM business_elements WHERE name IN ('User','Product','Order','Review','Category','AccessRule')"))
    pass