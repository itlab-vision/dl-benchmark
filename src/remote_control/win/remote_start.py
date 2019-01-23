import wmi, time

def get_process():
    c = wmi.WMI("ws-2k-110-06", user="Kumbrasev.p", password="Qwerty123")
    #c = wmi.WMI()

    process_startup = c.Win32_ProcessStartup.new()
    process_startup.ShowWindow = 1
    process_id, result = c.Win32_Process.Create(CommandLine=('CMD.EXE /c (python C:\\Users'
        '\\kumbrasev.p\\Documents\\GitHub\\openvino-dl-benchmark\\src'
        '\\remote_control\\win\\ftp_client.py -ip 10.0.16.80 -l Kumbrasev.p -p Qwerty123)'),
        ProcessStartupInformation=process_startup)
    if result == 0:
        print("Process started successfully: %d" % process_id)
    else:
        raise(RuntimeError, "Problem creating process: %d" % result)


        


if __name__ == '__main__':
    get_process()