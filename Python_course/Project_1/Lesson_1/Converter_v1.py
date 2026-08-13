#convert ILS amount to USD
rate = 3.8
ils_amount = 700
usd_amount = int(ils_amount/rate)

print("ILS = " , ils_amount)
print("Rate ILS to USD = ", rate)
print("USD = ", usd_amount)