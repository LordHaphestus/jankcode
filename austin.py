from pysb import SbApi

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjYmQzMDFlZC00YWZlLTQ1NmEtOWNlNi1mNmU0Mjg1MzkxMjgiLCJpYXQiOjE2Njg2NjQxOTIsInN1YiI6MTAwMDExLCJhdWQiOjQ5MDA3LCJpc3MiOiJkY2IxNTdiNDUzODU5M2IxY2Q4YzE0YTUxZjk5YmEyOSJ9.UOdJeUTupIU0W4Yaq4-Nd8djWd64o-UZeWUPPjohVuc'
sb_url = 'bamfoxvalley'


# token = input("Enter API Token")
# sb_url = input("Enter SB URL")

api = SbApi(token, sb_url)
# Check for Lifetime points field
points_field_lifetime_points = api.get_custom_fields_by_filter({'key': 'lifetime_pointes'})
if not points_field_lifetime_points:
    api.create_custom_field({'key': 'lifetime_points', 'group_id': 'customer', 'name': 'Lifetime Points','required': False,'unique': False,'validation_type': 'text'})
else: print("Lifetime Points Already Exists")

# Check for Number of Rewards field
points_field_number_of_rewards = api.get_custom_fields_by_filter({'key': 'number_of_rewards'})
if not points_field_number_of_rewards:
    api.create_custom_field({'key': 'number_of_rewards', 'group_id': 'customer', 'name': 'Number of Rewards','required': False,'unique': False,'validation_type': 'text','metadata': {'show_on_customer_list': True}})
else: print("Number of Rewards Already Exists")

# Check for Lifetime points field
points_field_rewards_member = api.get_custom_fields_by_filter({'key': 'rewards_member'})
if not points_field_rewards_member:
    api.create_custom_field({'key': 'rewards_member', 'group_id': 'customer', 'name': 'Rewards Member','required': False,'unique': False,'validation_type': 'list','validation_options': ["true","false"],'metadata': {'show_on_customer_list': True}})
else: print("Rewards Member Already Exists")

# Check for Lifetime points field
points_field_points_to_next_reward = api.get_custom_fields_by_filter({'key': 'points_to_next_reward'})
if not points_field_points_to_next_reward:
    api.create_custom_field({'key': 'points_to_next_reward', 'group_id': 'customer', 'name': 'Points to Next Reward','required': False,'unique': False,'validation_type': 'text','metadata': {'show_on_customer_list': True}})
else: print("Points to Next Reward Already Exists")

# api.create_coupon()
