import requests, time, csv
from datetime import datetime, timedelta

url= 'https://mystore.ncrsilver.com/app/Account/LogOn'
url2 = 'https://mystore.ncrsilver.com/app/Customer/GetCustomers'
s = requests.Session()
page = 1
maxcount=2
today = datetime.now()

#Change this variable to match the days til reward expires for the plan.
#If there is no expiration date set to 0.

days_until_expired = 90
r = s.post(url, data={"username":"RSRaustinBAM","password":"austin5521"})
all_customers = []

while page <= maxcount:
 #   url3='https://mystore.ncrsilver.com/app/Customer/GetCustomers?_dc=1605718082271'
    data2={
    'PageRowCount': "1000",
    'RequestedPageNum':page,
    'TotalRowCount':"-1",
    'SearchArg':	"",
    'SortDirection':"ASC",
    'SortColumn':"Name",
    'page':page,
    'start':"0",
    'limit':"1000",
    'sort':"[{\"property\":\"Name\",\"direction\":\"ASC\"}]",
    'isAjaxRequest':"true",
    }
    r3 = s.post(url2, data2)
    print(r3)
    values = r3.json()
    all_customers.append(values['ResultSet'])
    maxcount = values['TotalPageCount']
    page += 1
    time.sleep(1)
    print ('ITS WORKING, ITS WORKING')
fields = ['CustomerId', 'Name', 'PhoneNumber1', 'PhoneNumber2', 'ExternalCustomerId','Balance' ]
customers = []
count = 0
try:
    for customer_list in all_customers:
        for customer in customer_list:
            url4 = 'https://mystore.ncrsilver.com/app/Customer/GetCustomer'
            r4 = s.post(url4, data = {'customerId':customer['CustomerId']})
            customers.append(r4.json())
            time.sleep(.25)
        count += 1
        print(count)
except Exception as e:
    print (e)
rewards=[]
for customer in customers:
    num_of_rewards = 0
    lifetime_points = 0
    points_to_reward = 0

    if customer['Entity']['LoyaltyProgramRewards']:
        for reward in customer['Entity']['LoyaltyProgramRewards']:

            #If reward_expired is True it won't write the reward to file.
            reward_expired = True
            cus_rewards = {}
            lifetime_points += reward['PointsQuantity']
            if reward['RewardMetDateTime'] and not reward['RewardRedeemedDateTime']:

                #If there is a days til expired it checks if the reward is expired using the days_until_expired variable set above.
                if days_until_expired:
                    #Check if reward is expired.
                    full_date_earned = reward['RewardMetDateTime'].split('T')[0]
                    reward_expire_date = datetime.strptime(full_date_earned, '%Y-%m-%d') + timedelta(days_until_expired)

                    if reward_expire_date > today:
                        num_of_rewards += 1
                        reward_expired = False

                #If days_until_expired is not set, the rewards won't expire and is only checks if the reward is earned and not redeemed.
                else:
                    num_of_rewards += 1
                    reward_expired = False

            # NCR issues a not earned reward to keep track of the points to next reward.
            # Set reward_expired to false so the points_to_reward can be written to the customer.
            if not reward['RewardMetDateTime']:
                points_to_reward = reward['ThresholdQuantity'] - reward['PointsQuantity']
                reward_expired = False

            #cus_rewards = {'CustomerId': customer['Entity']['ExternalCustomerId'], 'Name': customer['Entity']['CustomerName'], 'RewardEarnDate' : reward['RewardMetDateTime'], 'RedeemedDate': reward['RewardRedeemedDateTime'], 'ExpirationDate': reward['ExpirationDateTime'], 'PointsQuantity': reward['PointsQuantity'], 'ThresholdQuantity': reward['ThresholdQuantity']}
            if not reward_expired:
                cus_rewards = {'CustomerId': customer['Entity']['ExternalCustomerId'], 'Name':customer['Entity']['CustomerName'],'NumberofRewards': num_of_rewards,'LifetimePoints': lifetime_points,'PointsToNextReward':points_to_reward, 'RewardEarnedDate': reward['RewardMetDateTime']}
                rewards.append(cus_rewards)

#fieldnames = ['CustomerId','Name', 'RewardEarnDate', 'RedeemedDate', 'ExpirationDate', 'PointsQuantity', 'ThresholdQuantity','Lifetime Points','NumberofRewards','']
fieldnames = ['CustomerId', 'Name','NumberofRewards','LifetimePoints','PointsToNextReward', 'RewardEarnedDate']
with open ('reward_scrape.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for reward in rewards:
        writer.writerow(reward)
