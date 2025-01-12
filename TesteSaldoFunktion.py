from Workpackage import *
from ReadWorkpackes import *


def main():
    file = open("./Dateien/Homeoffice.xml", 'r', encoding='utf-8')
    workpackages = read_workpackages(file)
    sum_balance = 0
    for wp in workpackages:
        sum_balance += wp.get_workpackage_balance("01.03.2020", "31.03.2020")
        for wd in wp.workdays:
            date_str = str(wd.date)
            if "01.03.2020" <= wd.date <= "31.03.2020":
                wd_balance = Time.convert_seconds_to_time_string(wd.get_workday_balance())
                print("Saldo für {0} am {1}: {2}".format(wp.wp_name, date_str, wd_balance))
    balance_str = Time.convert_seconds_to_time_string(sum_balance)
    print("\nGesamtsaldo: " + balance_str)


if __name__ == "__main__":
    main()
