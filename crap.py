def create_reward_coupon(sb_connection, code='r', name='Rewards: 25% Off', discount=0.25):
	logger = logging.getLogger(__name__)

	coupon_id = sb_connection.pipe._api.create_coupon({'code': code, 'name': name}).json()['id']

	# Set conditions
	sb_connection.pipe._api.update_coupon(coupon_id, {'condition_definition': {"$and": [{"customer.custom.number_of_rewards": {"$nin": ["0"]}}, {"customer.custom.number_of_rewards": {"$gt": "0"}}]}, 'action_definition': [{'type': "DiscountItem", 'params': {'discount': discount, 'discount_type': "percent", 'item_conditions': None, 'item_price_attribute': "price"}}], 'disabled': False})

update_coupon(self, coupon_id, coupon_data):
