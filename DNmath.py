def bonus_spilt(original,count):
  if count > 0 :
    other = count - 1
    spiltBouns = original / (other * 1.003 + 1)
    currency = currency_converter(spiltBouns)
    return currency
  else : return "人數錯誤"

def currency_converter(count):
  copper_value = int(count * 10000)
  gold = copper_value // (100 * 100)
  silver = (copper_value // 100) % 100
  copper = copper_value % 100
  
  result = ""
  if gold > 0:
    result += f"{gold}金 "
    if silver > 0 or copper > 0:
        result += f"{silver:02d}銀 "
  elif silver > 0:
    result += f"{silver}銀 "

  if copper > 0 or (gold == 0 and silver == 0):
    result += f"{copper}銅" if gold == 0 else f"{copper:02d}銅"

  return result.strip()
