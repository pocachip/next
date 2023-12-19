from datetime import datetime

now = datetime.now()
a_str = now.strftime('%Y-%m-%d %H:%M:%S')
print(a_str)
