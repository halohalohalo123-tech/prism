import sys
import os

# إضافة مسار المشروع
path = '/home/Ha0la1/prism'
if path not in sys.path:
    sys.path.append(path)

import dash
from dash import html
import numpy as np

# إنشاء التطبيق بشكل مباشر ونظيف ليقرأه سيرفر PythonAnywhere بدون أخطاء
app = dash.Dash(__name__)

# تصميم صفحة مؤقتة أو ترحيبية تتأكدي من خلالها أن الموقع يعمل تماماً بدون مشاكل 502
app.layout = html.Div(
    style={
        "backgroundColor": "#050816",
        "color": "#00F5FF",
        "padding": "50px",
        "textAlign": "center",
        "fontFamily": "Arial",
        "minHeight": "100vh"
    },
    children=[
        html.H1("PRISM Dashboard is Live!"),
        html.P("تم تشغيل لوحة التحكم بنجاح على سيرفر PythonAnywhere.", style={"color": "#39FF14", "fontSize": "20px"})
    ]
)

# المتغير الأساسي المطلوب للـ WSGI
server = app.server