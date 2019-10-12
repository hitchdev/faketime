from commandlib import Command
from faketime import Faketime
from datetime import datetime
faketime = Faketime("/tmp/currenttime.txt")
faketime.change_time(datetime(2050, 6, 7, 10, 9, 22, 713689))
print(faketime.env_vars)
Command("date").with_env(**faketime.env_vars).run()
