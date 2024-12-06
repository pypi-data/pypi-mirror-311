# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:21:15 2024

@author: ASUS
"""

from .plus_minus import numberplus, numberminus
from .mul_div import numbermultiply, numberdivision

def numbermod(a, b):
    """
    Compute the modulus (remainder) of two numbers.

    Parameters:
    - a (int or float): The dividend.
    - b (int or float): The divisor.

    Returns:
    - int or float: The remainder when a is divided by b.
    """
    # 计算商的整数部分
    quotient = numberdivision(a, b)
    quotient_int = int(quotient)  # 取商的整数部分

    # 计算余数
    result = numberminus(a, numbermultiply(quotient_int, b))
    return result
