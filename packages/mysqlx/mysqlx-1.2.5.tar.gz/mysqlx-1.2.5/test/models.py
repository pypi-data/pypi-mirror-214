from decimal import Decimal
from mysqlx.orm import Model
from datetime import date, datetime


class BaseModel(Model):
    __pk__ = 'id'
    __update_by__ = 'update_by'
    __update_time__ = 'update_time'
    __del_flag__ = 'del_flag'

    def __init__(self, id: int = None, create_by: int = None, create_time: datetime = None, update_by: int = None, update_time: datetime = None, del_flag: int = None): 
        self.id = id 
        self.create_by = create_by 
        self.create_time = create_time 
        self.update_by = update_by 
        self.update_time = update_time 
        self.del_flag = del_flag 


class Fund(BaseModel):
    __table__ = 'fund'

    def __init__(self, id: int = None, code: str = None, name: str = None, alias: str = None, sort: int = None, last_profit: Decimal = None, net_worth_date: date = None, buy_rate: Decimal = None, day1: int = None, sell_rate1: Decimal = None, day2=None, sell_rate2: Decimal = None, day3=None, sell_rate3: Decimal = None, day4=None, sell_rate4: Decimal = None, sell_rate5: Decimal = None, hidden: int = None, statistics_date: date = None, show_trade_date: date = None, del_flag: int = None, ctl_flag: int = None):
        super().__init__(id=id, del_flag=del_flag) 
        self.code = code 
        self.name = name 
        self.alias = alias 
        self.sort = sort 
        self.last_profit = last_profit 
        self.net_worth_date = net_worth_date 
        self.buy_rate = buy_rate 
        self.day1 = day1 
        self.sell_rate1 = sell_rate1 
        self.day2 = day2 
        self.sell_rate2 = sell_rate2 
        self.day3 = day3 
        self.sell_rate3 = sell_rate3 
        self.day4 = day4 
        self.sell_rate4 = sell_rate4 
        self.sell_rate5 = sell_rate5 
        self.hidden = hidden 
        self.statistics_date = statistics_date 
        self.show_trade_date = show_trade_date 
        self.ctl_flag = ctl_flag 


class Person(BaseModel):
    __table__ = 'person'

    def __init__(self, id: int = None, name: str = None, age: int = None, sex: int = None):
        super().__init__(id=id) 
        self.name = name 
        self.age = age 
        self.sex = sex 


class Trade(BaseModel):
    __table__ = 'trade'

    def __init__(self, id: int = None, fund_id: int = None, buy_date: date = None, amount: Decimal = None, buy_fee: Decimal = None, buy_worth: Decimal = None, fund_num: Decimal = None, status: int = None, sell_date: date = None, sell_amount: Decimal = None, sell_worth: Decimal = None, sell7: int = None, confirm_date: date = None):
        super().__init__(id=id) 
        self.fund_id = fund_id 
        self.buy_date = buy_date 
        self.amount = amount 
        self.buy_fee = buy_fee 
        self.buy_worth = buy_worth 
        self.fund_num = fund_num 
        self.status = status 
        self.sell_date = sell_date 
        self.sell_amount = sell_amount 
        self.sell_worth = sell_worth 
        self.sell7 = sell7 
        self.confirm_date = confirm_date 


class FundDaliy(BaseModel):
    __table__ = 'fund_daliy'

    def __init__(self, id: int = None, fund_id: int = None, net_worth_date: date = None, net_worth: Decimal = None, day_growth: Decimal = None, day_profit: Decimal = None, total_profit: Decimal = None, last_profit: Decimal = None, curr_profit: Decimal = None, amount: Decimal = None, buy_fee: Decimal = None, sell_fee: Decimal = None, act_amount: Decimal = None, act_day_profit: Decimal = None):
        super().__init__(id=id) 
        self.fund_id = fund_id 
        self.net_worth_date = net_worth_date 
        self.net_worth = net_worth 
        self.day_growth = day_growth 
        self.day_profit = day_profit 
        self.total_profit = total_profit 
        self.last_profit = last_profit 
        self.curr_profit = curr_profit 
        self.amount = amount 
        self.buy_fee = buy_fee 
        self.sell_fee = sell_fee 
        self.act_amount = act_amount 
        self.act_day_profit = act_day_profit 


class Bonus(BaseModel):
    __table__ = 'bonus'

    def __init__(self, id: int = None, fund_id: int = None, dividend_date: date = None, amount: Decimal = None):
        super().__init__(id=id) 
        self.fund_id = fund_id 
        self.dividend_date = dividend_date 
        self.amount = amount 


class User(BaseModel):
    __table__ = 'user'

    def __init__(self, id: int = None, name: str = None, age: int = None, birth_date: date = None, sex: int = None, grade: float = None, point: float = None, money: Decimal = None, create_by: int = None, create_time: datetime = None, update_by: int = None, update_time: datetime = None, del_flag: int = None):
        super().__init__(id=id, create_by=create_by, create_time=create_time, update_by=update_by, update_time=update_time, del_flag=del_flag) 
        self.name = name 
        self.age = age 
        self.birth_date = birth_date 
        self.sex = sex 
        self.grade = grade 
        self.point = point 
        self.money = money 

