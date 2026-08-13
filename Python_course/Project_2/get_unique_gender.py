users = '''
first_name,email,gender
Haslett,hgwillyam0@statcounter.com,Male
Nappie,nizchaki1@cyberchimps.com,Male
Linnell,lhamper2@lycos.com,Agender
Nikaniki,nelvy3@abc.net.au,Female
Verne,vlecount4@quantcast.com,Male
Ruby,rshillan5@hhs.gov,Female
Martie,mgiscken6@liveinternet.ru,Male
Gabi,gmackintosh7@fotki.com,Male
Gabi,gbretherton8@sakura.ne.jp,Male
Cortie,cwarlowe9@ox.ac.uk,Male
Glenn,gdominguesa@opera.com,Genderqueer
Kennie,ktrailb@exblog.jp,Male
Avram,agirodinc@pcworld.com,Male
Cherice,cdumphriesd@opera.com,Female
Rena,rglisanee@homestead.com,Genderfluid
Bibbie,bpaishf@ocn.ne.jp,Female
Conan,crichesg@rakuten.co.jp,Genderqueer
Zed,zcrisellh@google.nl,Male
Judie,jstratteni@hao123.com,Female
Delores,ddengej@weebly.com,Female
'''

list_of_genders = set()
for line in users.strip().split("\n")[1:]:
    gender = line.split(",")[-1]
    list_of_genders.add(gender)

print("Unique genders:")
for gender in list_of_genders:
    print(gender)