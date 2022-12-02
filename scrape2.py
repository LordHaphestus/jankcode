import requests, time, csv
url= 'https://mystore.ncrsilver.com/app/Account/LogOn'
url2 = 'https://mystore.ncrsilver.com/app/Customer/GetCustomers'
s = requests.Session()
r= s.post(url, data={"username":"austin321","password":"Austin1!"})
page = 1
maxcount=2
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
    values=r3.json()
    all_customers.append(values['ResultSet'])
    maxcount = values['TotalPageCount']
    page += 1
    time.sleep(1)
    print ('ITS WORKING, ITS WORKING')
fields = ['CustomerId', 'Name', 'PhoneNumber1', 'PhoneNumber2', 'ExternalCustomerId','Balance' ]
customers=[]
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
except exception as e:
    print (e)
rewards=[]
for customer in customers:
    num_of_rewards = 0
    lifetime_points = 0
    points_to_reward = 0
    cus_rewards = {}
    if customer['Entity']['LoyaltyProgramRewards']:
        for reward in customer['Entity']['LoyaltyProgramRewards']:
            lifetime_points += reward['PointsQuantity']
            if reward['RewardMetDateTime'] and not reward['RewardRedeemedDateTime']:
                num_of_rewards += 1
            if not reward['RewardMetDateTime']:
                points_to_reward = reward['ThresholdQuantity'] - reward['PointsQuantity']
        #cus_rewards = {'CustomerId': customer['Entity']['ExternalCustomerId'], 'Name': customer['Entity']['CustomerName'], 'RewardEarnDate' : reward['RewardMetDateTime'], 'RedeemedDate': reward['RewardRedeemedDateTime'], 'ExpirationDate': reward['ExpirationDateTime'], 'PointsQuantity': reward['PointsQuantity'], 'ThresholdQuantity': reward['ThresholdQuantity']}
        cus_rewards = {'CustomerId': customer['Entity']['ExternalCustomerId'], 'Name':customer['Entity']['CustomerName'],'NumberofRewards': num_of_rewards,'LifetimePoints': lifetime_points,'PointsToNextReward':points_to_reward}
        rewards.append(cus_rewards)
#fieldnames = ['CustomerId','Name', 'RewardEarnDate', 'RedeemedDate', 'ExpirationDate', 'PointsQuantity', 'ThresholdQuantity','Lifetime Points','NumberofRewards','']
fieldnames = ['CustomerId', 'Name','NumberofRewards','LifetimePoints','PointsToNextReward']
with open ('reward_scrape.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for reward in rewards:
        writer.writerow(reward)
