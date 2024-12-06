# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:51:15 2024

@author: ASUS
"""

# simplemathglh/__init__.py

# 从 plus_minus 模块导入函数
from .plus_minus import numberplus, numberminus

# 从 mul_div 模块导入函数
from .mul_div import numbermultiply, numberdivision

# 从 mod 模块导入函数
from .mod import numbermod

# 使用 __all__ 来明确哪些函数是包的公共接口
__all__ = ["numberplus", "numberminus", "numbermultiply", "numberdivision", "numbermod"]
