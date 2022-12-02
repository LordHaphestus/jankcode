from pysb import SbApi
import time

# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5NmYzZTEwYy03MmUxLTRlYTUtYmU4NS1mMjc3YWZlYWNkNjEiLCJpYXQiOjE1NTA4MDUxNjYsInN1YiI6MTAwMDE2LCJhdWQiOjc5MTYsImlzcyI6bnVsbH0.4ctJjZuAjQpTzabEdAnUcVFivZdKPLTfESJSpHZz1_Y'
# sb_url = 'rsr'

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjYmQzMDFlZC00YWZlLTQ1NmEtOWNlNi1mNmU0Mjg1MzkxMjgiLCJpYXQiOjE2Njg2NjQxOTIsInN1YiI6MTAwMDExLCJhdWQiOjQ5MDA3LCJpc3MiOiJkY2IxNTdiNDUzODU5M2IxY2Q4YzE0YTUxZjk5YmEyOSJ9.UOdJeUTupIU0W4Yaq4-Nd8djWd64o-UZeWUPPjohVuc'
sb_url = 'bamfoxvalley'

# token = input("Enter API Token")
# sb_url = input("Enter SB URL")

api = SbApi(token, sb_url)

# Get the range, range has to be 1 more than the total wanted ex if you want 20 rewards your range is 1, 21
# coupon = input("Input the range of coupons here ex 1, 21")
# check if coupon exists

# if coupon doesnt exist, create coupon(s)

dollar = input("How Much is one coupon?")

#input("What range of coupons do you want created?")
coupon = range(1,11)
less_than_rewards = []
for x in coupon:
    less_than_rewards.append(str(x-1))
    coupon_id = api.create_coupon({'code': 'BAM' + str(x), 'name': 'Rewards: $' + str(int(x)*int(dollar)) + ' Off'}).json()['id']
    time.sleep(1)
    api.update_coupon(coupon_id, {'condition_definition':{"$and": [{'customer.custom.number_of_rewards': {'$nin': less_than_rewards}}]}, 'action_definition': [{'type': "DiscountTicket", 'params': {'discount': int(x)*int(dollar), 'item_conditions': None, 'discount_type': "amount"}}], 'disabled': False})

    print(coupon_id)
# Change code
# Change Name
# Change gte number
# change discount
# if coupon exists print error
