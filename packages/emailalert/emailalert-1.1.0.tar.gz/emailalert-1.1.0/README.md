use the library in other Python scripts. 
Create a new Python script in a different directory and 
import and use the send function from the library

```
from alertmail.alertmail import send

recipient = ['kianseng.lim@sony.com', 'Junji.Yamauchi@sony.com']
subject = '【エラー通知】Grid Expansionシステム'
message = '*** このメールはGrid Expansionシステムから自動配信しています ***'

 alert = send(recipient,subject,message)

print(alert) 

```