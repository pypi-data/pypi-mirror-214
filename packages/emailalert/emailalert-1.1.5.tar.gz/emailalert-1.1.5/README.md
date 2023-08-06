use the library in other Python scripts. 
Create a new Python script in a different directory and 
import and use the send function from the library

```
from sck.emailalert import send as alert

recipient = ['kianseng.lim@sony.com', 'kianseng.lim@sony.com']
subject = '【エラー通知】Grid Expansionシステム'
message = '*** このメールはGrid Expansionシステムから自動配信しています ***'
folder_path = './'
file_extension = '.txt'

alert(recipient,subject,message, folder_path, file_extension)

print(alert) 

```