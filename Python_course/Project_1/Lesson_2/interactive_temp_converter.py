# convert grad cels to fahrengeit
# 
'''
Formula	
(0°C * 9/5) + 32 = 32°F
'''
temp_cels = float(input("Введите сколько градусов по Цельсию Вы хотите сконвертировать в градусы по Фаренгейту:"))
temp_fahr = (temp_cels * 9//5) + 32

#print("Градусов по Цельсию: ", temp_cels,"°C")
print(f"Градусов по Цельсию: {temp_cels} °C равно градусам по Фаренгейту: {temp_fahr} °F")