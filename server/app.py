from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    try:
        bakeries = Bakery.query.all()
        bakery_list = [bakery.serialize() for bakery in bakeries]
        return jsonify(bakery_list)
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred"}), 500

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    try:
        bakery = Bakery.query.get(id)
        if bakery:
            return jsonify(bakery.serialize(with_baked_goods=True))
        else:
            return jsonify({"message": "Bakery not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred"}), 500

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        baked_goods_list = [baked_good.serialize() for baked_good in baked_goods]
        return jsonify(baked_goods_list)
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred"}), 500

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    try:
        baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
        return jsonify(baked_good.serialize())
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)
