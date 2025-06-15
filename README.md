```
embedded_test_automation/
├── config/
│   ├── device_config.yaml        # information about relay, serial, ssh
│   └── test_config.yaml          # timeout, image, log path
├── drivers/
│   ├── relay_controller.py       # power control
│   ├── serial_controller.py      # uart controller (read uart log)
│   └── ssh_controller.py         # ssh & scp
├── tests/
│   └── test_boot_login.py        # test: boot + login
├── utils/
│   ├── config_loader.py          # load YAML
│   ├── log_parser.py             # get data by patter in log
│   └── wait_tools.py             # timeout, retry
├── requirements.txt              # pyserial, paramiko, pytest, pyyaml

```
