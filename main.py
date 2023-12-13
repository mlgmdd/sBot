from app import App

if __name__ == "__main__":
    app = App()
    # app.bot.post_server.run()
    app.main_loop()



    # r = app.get_summary(group_id=603161290)
    # print(r)

    # msgs = post_server_app.bot.get_group_msg(group_id=603161290)
    # post_server_app.local_data.save_group_msg(msgs)
    # print(msgs)


