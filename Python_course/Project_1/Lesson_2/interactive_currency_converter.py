#convert ILS amount to USD

ils_amount = float(input("Сколько шекелей меняем?\n"))
rate = float(input("По какому курсу?\n"))
usd_amount = float(ils_amount/rate)

print(f"{ils_amount}\u20AA по курсу {rate} \u20AA/\u0024 = {usd_amount:.2f}\u0024")