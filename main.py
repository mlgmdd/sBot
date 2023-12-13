from app import App

if __name__ == "__main__":
    app = App()

    # app.local_data.clear_group_msg(group_id=603161290)
    msgs = app.bot.get_group_msg(group_id=732649746)
    app.local_data.save_group_msg(msgs, group_id=732649746)
    app.main_loop()



    # r = app.get_summary(group_id=603161290)
    # print(r)


    # print(msgs)


