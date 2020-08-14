# !/usr/bin/python
# -*-coding:utf-8 -*-
from AutoBookseatTKB import AutoBookseatTKB

print("Test started...")
atb = AutoBookseatTKB('AutoBookseatTKB-settings.json')
atb.login()

# atb.wait_until_noon_or_midnight()
atb.refresh()

atb.select_class()
atb.send_securitycode()
atb.select_location()
atb.select_date()
atb.select_sessions()
atb.click_send()
# atb.accept_alerts()
# print("Task completed. Plese check your booking:)")
