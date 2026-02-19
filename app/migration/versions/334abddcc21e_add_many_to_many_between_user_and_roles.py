"""Add many to many between User and Roles + change permissions to boolean

Revision ID: 334abddcc21e
Revises: 2026_02_18_seed_rbac_data
Create Date: 2026-02-19 15:43:57.911099
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '334abddcc21e'
down_revision = '2026_02_18_seed_rbac_data'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создание промежуточной таблицы many-to-many User ↔ Role
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # Изменение типов колонок в access_roles_rules на Boolean
    # Для зарезервированных слов (create, update, delete) используем двойные кавычки
    op.alter_column(
        'access_roles_rules', 'read',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='read::boolean'
    )
    op.alter_column(
        'access_roles_rules', 'read_all',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='read_all::boolean'
    )
    op.alter_column(
        'access_roles_rules', 'create',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='"create"::boolean'
    )
    op.alter_column(
        'access_roles_rules', 'update',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='"update"::boolean'
    )
    op.alter_column(
        'access_roles_rules', 'update_all',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='update_all::boolean'
    )
    op.alter_column(
        'access_roles_rules', 'delete',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='"delete"::boolean'
    )
    op.alter_column(
        'access_roles_rules', 'delete_all',
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using='delete_all::boolean'
    )

    # Добавление связи product_id в orders (если это часть миграции)
    op.add_column('orders', sa.Column('product_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'orders', 'products', ['product_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Обратное изменение типов колонок обратно в VARCHAR
    op.alter_column(
        'access_roles_rules', 'delete_all',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='delete_all::text'
    )
    op.alter_column(
        'access_roles_rules', 'delete',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='"delete"::text'
    )
    op.alter_column(
        'access_roles_rules', 'update_all',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='update_all::text'
    )
    op.alter_column(
        'access_roles_rules', 'update',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='"update"::text'
    )
    op.alter_column(
        'access_roles_rules', 'create',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='"create"::text'
    )
    op.alter_column(
        'access_roles_rules', 'read_all',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='read_all::text'
    )
    op.alter_column(
        'access_roles_rules', 'read',
        existing_type=sa.Boolean(),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
        postgresql_using='read::text'
    )

    # Удаление связи в orders
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'product_id')

    # Удаление many-to-many таблицы
    op.drop_table('user_roles')