try:
    import os, sys
    from kivy.resources import resource_add_path, resource_find

    import display

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    display.BingGo().run()
except Exception as e:
    print("!!!!!!!!!!ERROR!!!!!!!!!!")
    print(e)

input()
