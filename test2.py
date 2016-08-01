huang = ['huanglu', 22]
zhang = ['zhangqingru', 21]
database = [huang, zhang]
print database

greeting = 'hello'
print greeting[0]
print greeting[-1]

fourth = raw_input('Year:')[3]
print fourth

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Seq', 'Oct', 'Nov', 'Dec']
endings = ['st','nd','rd']+17*['th']+['st','nd','rd']+7*['th']+['st']
year = raw_input('Year:')
month = raw_input('Month:')
day = raw_input('Day:')
month_num = int(month)
day_num = int(day)
month_name = months[month_num-1]
day_name = day+endings[day_num-1]
print month_name+' '+day_name+' '+year

numbers = [1,2,3,4,5,6,7,8,9,10]
print numbers[2:4]
print numbers[-4:-1]
