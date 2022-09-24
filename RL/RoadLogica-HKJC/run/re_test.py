patt = r'第(\d+)場 - (.*?)(\d+年\d+月\d+日),(星期.),(.*?),([0-9:]+)(.*?),(.*)(\d+)米(.*)獎金:\$(.*?),評分:(.*?),(第.班)'
string = '第1場 - 樂華讓賽2020年2月8日,星期六,沙田,12:15草地,"C+3"賽道,1000米獎金:$967,000,評分:60-40,第四班'
import re
# print(re.search(patt, string))

from utils.time import Time, TimeUnit
print(Time.time_calculate(t_type=TimeUnit.MINUTE, num=-3))