import pytest
from app import create_app, db

@pytest.fixture(scope='function')
def test_client():
    app = create_app()

    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as testing_client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield testing_client

    with app.app_context():
        db.drop_all()