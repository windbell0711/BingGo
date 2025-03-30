"""
-*- coding: utf-8 -*-
@Time    : 2025-01-21
@Github  : windbell0711/BingGo
@Author  : Lilold333
@Coauthor: windbell0711
@License : Apache 2.0
@File    : main.py
"""
#TODO:删除注释

from display import BieGuanWoException

debug = True

if not debug:
    try:
        import time
        import os
        import sys
        from kivy.resources import resource_add_path, resource_find

        import display

        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))

        b = display.BingGo()
        b.run()

    except BieGuanWoException:
        print("接收到BieGuanWoException，程序已退出。")

    except Exception as e:
        print("!!!!!!!!!!ERROR!!!!!!!!!!")
        import traceback
        print("collecting information...")
        with open(file="log_error.txt", mode='a', encoding='utf-8', newline="\n") as f:
            f.write("\n\n\n\n\n!ERROR " + str(time.time()))
            try:
                print(b.war_screen.war.logs)
                f.write("\n\nlogs: " + str(b.war_screen.war.logs))
            except Exception as ee:
                print("error while trying to write logs: " + str(ee))
                f.write("\n\nlogs: Fail to get logs.")
            f.write("\n\nerror raised: " + traceback.format_exc())
        input("We are sorry that an exception occurred. We've save your game in log_error.txt. You can send it to us and we'll assist you to kill the problems. You can also raise an issue at https://github.com/windbell0711/BingGo/issues. Sorry again.\n")
        raise e
else:
    # input()
    import time
    import os
    import sys
    from kivy.resources import resource_add_path, resource_find

    import display

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    b = display.BingGo()
    b.run()