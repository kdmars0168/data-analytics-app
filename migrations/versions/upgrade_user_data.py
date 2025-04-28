import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table
from alembic import op
from alembic.runtime.migration import MigrationContext
from alembic.operations import Operations
from data_analytics_app.migrations.versions.a4774f9540c1_create_user_table import upgrade


def test_upgrade_creates_tables():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()
    metadata = MetaData()

    # Apply the upgrade migration
    context = MigrationContext.configure(connection)
    op_obj = Operations(context)
    upgrade()

    # Reflect the database schema
    metadata.reflect(bind=engine)

    # Assert 'user' table exists with correct columns
    user_table = metadata.tables.get("user")
    assert user_table is not None
    assert isinstance(user_table.c.id.type, sa.Integer)
    assert isinstance(user_table.c.name.type, sa.String)
    assert isinstance(user_table.c.email.type, sa.String)
    assert isinstance(user_table.c.password_hash.type, sa.String)

    # Assert 'uploaded_data' table exists with correct columns
    uploaded_data_table = metadata.tables.get("uploaded_data")
    assert uploaded_data_table is not None
    assert isinstance(uploaded_data_table.c.id.type, sa.Integer)
    assert isinstance(uploaded_data_table.c.filename.type, sa.String)
    assert isinstance(uploaded_data_table.c.user_id.type, sa.Integer)
    assert isinstance(uploaded_data_table.c.uploaded_at.type, sa.DateTime)

    # Assert 'shared_data' table exists with correct columns
    shared_data_table = metadata.tables.get("shared_data")
    assert shared_data_table is not None
    assert isinstance(shared_data_table.c.id.type, sa.Integer)
    assert isinstance(shared_data_table.c.data_id.type, sa.Integer)
    assert isinstance(shared_data_table.c.shared_with_user_id.type, sa.Integer)

    connection.close()
