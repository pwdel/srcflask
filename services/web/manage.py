import click
from flask.cli import FlaskGroup

from project import app, db
from project.models import User

# from previous command line control
# from project import User

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# previous command line control
@cli.command("seed_db")
def seed_db():
    user = User(name='Person Admin', email='admin@test.com', organization='WhateverCo', user_type='admin')
    # use our set_password method
    user.set_password('password')
    # commit our new user record and log the user in
    db.session.add(user)
    db.session.commit()
    # add sponsor initial user
    user = User(name='Sponsory Sponsington', email='test@test.com', organization='SponsorCo', user_type='sponsor',user_status='approved')
    # use our set_password method
    user.set_password('123456')
    # commit our new user record and log the user in
    db.session.add(user)
    db.session.commit()
    # add editor initial user
    user = User(name='Editor Edintarian', email='edit@test.com', organization='EditCo', user_type='editor',user_status='approved')
    # use our set_password method
    user.set_password('123456')
    # commit our new user record and log the user in
    db.session.add(user)
    db.session.commit()


@cli.command("test_message")
def test_message():
	click.echo('hey this is a test message, thanks for reading!')


if __name__ == "__main__":
    cli()
