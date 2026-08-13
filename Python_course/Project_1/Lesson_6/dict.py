users = [
    {
        "id": 6,
        "first_name": "Iona",
        "last_name": "Wensley",
        "email": "iwensley5@google.co.uk",
        "gender": "Female",
        "ip_address": "62.49.95.53",
    },
    {
        "id": 7,
        "first_name": "Shaun",
        "last_name": "Brownhill",
        "email": "sbrownhill6@twitter.com",
        "gender": "Female",
        "ip_address": "74.80.124.109",
    },
    {
        "id": 8,
        "first_name": "Babbie",
        "last_name": "Waylett",
        "email": "bwaylett7@timesonline.co.uk",
        "gender": "Female",
        "ip_address": "216.97.233.154",
    }]

#create new list : emails
email_list = []
for i in range(len(users)):
        email = users[i]["email"]
        email_list.append(email)
        
print(f'List of emails: {email_list}')

user_properties = []
for k in users[0].keys():
    user_properties.append(k)
    
print(f'List of keys: {user_properties}')

users = {
        "iwensley5@google.co.uk": {
            "id": 6,
            "first_name": "Iona",
            "last_name": "Wensley",
            "email": "iwensley5@google.co.uk",
            "gender": "Female",
            "ip_address": "62.49.95.53",
        },
        "sbrownhill6@twitter.com": {
            "id": 7,
            "first_name": "Shaun",
            "last_name": "Brownhill",
            "email": "sbrownhill6@twitter.com",
            "gender": "Female",
            "ip_address": "74.80.124.109",
        },
        "bwaylett7@timesonline.co.uk": {
            "id": 8,
            "first_name": "Babbie",
            "last_name": "Waylett",
            "email": "bwaylett7@timesonline.co.uk",
            "gender": "Female",
            "ip_address": "216.97.233.154",
        }
    }
#print(f'List of names: {users["iwensley5@google.co.uk"]["first_name"]}')
names = []
for v in users.values():
   names.append(v["first_name"]) 
    
print(f'List of names: {names}')