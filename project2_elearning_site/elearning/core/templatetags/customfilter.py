from django import template
import math
from core.models import UserCourse

register = template.Library()

@register.simple_tag
def cal_sellprice(price, discount):
    if discount is None or discount == 0:
        return price
    
    sellprice = price
    sellprice = price - (price*discount*0.01)
    return math.floor(sellprice)


@register.filter(name='rupee')
def rupee(price):
    return f'₹{price}'

@register.filter(name='is_enrolled')
def is_enrolled(course):
    usercourse = UserCourse.objects.get(course = course)
    print(usercourse,'=======')
    if usercourse is not None:
        return True
    return False
    