"""
-*- coding: utf-8 -*-
@Time    : 2025-01-17
@Github  : windbell0711/BingGo
@License : Apache 2.0
@File    : main.py
"""  # TODO: 删除注释
import config

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

        while True:
            # 创建游戏实例
            instance = display.BingGo()
            instance.run()

            # 检查是否需要重启
            if not hasattr(instance, 'war_screen') or not instance.war_screen.restart_expected:
                break

            # 显式清理资源
            del instance
            import gc

            gc.collect()

    except Exception as e:
        print("!!!!!!!!!!ERROR!!!!!!!!!!")
        import traceback
        print("collecting information...")
        with open(file="log_error.txt", mode='a', encoding='utf-8', newline="\n") as f:
            f.write("\n\n\n\n\n!ERROR " + str(time.time()))
            try:
                print(instance.war_screen.war.logs)
                f.write("\n\nlogs: " + str(instance.war_screen.war.logs))
            except Exception as ee:
                print("error while trying to write logs: " + str(ee))
                f.write("\n\nlogs: Fail to get logs.")
            f.write("\n\nerror raised: " + traceback.format_exc())
        input("We are sorry that an exception occurred. We've save your game in log_error.txt. You can send it to us and we'll assist you to kill the problems. You can also raise an issue at https://github.com/windbell0711/BingGo/issues. Sorry again.\n")
        raise e

else:
    import time
    import os
    import sys
    from kivy.resources import resource_add_path, resource_find

    import display

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    while True:
        # 创建游戏实例
        instance = display.BingGo()
        instance.run()

        # 检查是否需要重启
        if not hasattr(instance, 'war_screen') or not instance.war_screen.restart_expected:
            break

        config.init_setting()

        # 显式清理资源
        del instance
        import gc
        gc.collect()
