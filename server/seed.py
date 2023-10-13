#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Bakery, BakedGood

fake = Faker()

with app.app_context():
    db.create_all()

    BakedGood.query.delete()
    Bakery.query.delete()

    bakeries = []
    for i in range(20):
        b = Bakery(name=fake.company())
        db.session.add(b)
        bakeries.append(b)

    db.session.commit()

    baked_goods = []
    names = []
    for i in range(200):
        name = fake.first_name()
        while name in names:
            name = fake.first_name()
        names.append(name)

        bg = BakedGood(
            name=name,
            price=randint(1, 10),
            bakery=rc(bakeries)
        )

        db.session.add(bg)
        baked_goods.append(bg)

    most_expensive_baked_good = rc(baked_goods)
    most_expensive_baked_good.price = 100
    db.session.add(most_expensive_baked_good)

    db.session.commit()
