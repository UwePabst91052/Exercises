import Workpackage as Wp
from ReadWorkpackes import *
from BerichtAusdrucken import *

parameters = [
    ["01.01.2023", "31.01.2023", "Januar 2023"],
    ["01.02.2023", "28.02.2023", "Februar 2023"],
    ["01.03.2023", "31.03.2023", "März 2023"],
    ["01.04.2023", "30.04.2023", "April 2023"],
    ["01.05.2023", "31.05.2023", "Mai 2023"],
    ["01.06.2023", "30.06.2023", "Juni 2023"],
    ["01.07.2023", "31.07.2023", "Juli 2023"],
    ["01.08.2023", "31.08.2023", "August 2023"],
    ["01.09.2023", "30.09.2023", "September 2023"],
    ["01.10.2023", "31.10.2023", "Oktober 2023"],
    ["01.11.2023", "30.11.2023", "November 2023"],
    ["01.12.2023", "31.12.2023", "Dezember 2023"],
]
parameters4 = [
    ["01.08.2024", "31.08.2024", "August 2024"]
]

parameters2 = [['01.01.2023', '31.12.2023', 'Jahr 2023']]
parameters3 = [['01.01.2024', '31.12.2024', 'Jahr 2024']]

def get_count_wt(date, wp):
    for wd in wp.workdays:
        if str(wd.date) == date:
            return len(wd.worktimes)

def check_real_worked(date, wp1, wp2):
    countWtWp1 = get_count_wt(date, wp1)
    countWtWp2 = get_count_wt(date, wp2)
    if(countWtWp1 > 0 and countWtWp2 > 0):
        return True, -1
    else:
        if countWtWp1 > 0:
            index = 0
        else:
            index = 1
        return False, index

def show_num_workdays(from_date, until_date, workpackages):
    keylist = create_work_merged(workpackages, from_date, until_date)
    countOffice = 0
    countHome = 0
    countBoth = 0
    evaluation_period = "Auswertungszeitraum vom {0} bis {1}".format(from_date, until_date)
    for key in keylist.keys():
        value = keylist[key]
        if len(value) > 1:
            result = check_real_worked(key, value[0], value[1])
            if result[0]:
                countBoth += 1
            else:
                if value[result[1]].wp_name == "Homeoffice":
                    countHome += 1
                else:
                    countOffice += 1
        else:
            if value[0].wp_name == "Homeoffice":
                countHome += 1
            else:
                countOffice += 1
    report = report_number_of_workdays(keylist, countHome, countOffice, countBoth, evaluation_period)
    return report

def main():
    filename = ".\\Dateien\\HomeOffice.xml"
    
    inFile = open(filename, "r", encoding="utf-8")
    workpackages = read_workpackages(inFile)
    inFile.close()

    for timespan in parameters:
        outfilename = "D:\\temp\\ZeiterfassungBerichte\\Report " + timespan[2] + ".txt"
        outFile = open(outfilename, "w", encoding="utf-8")
        report = show_num_workdays(timespan[0], timespan[1], workpackages)
        outFile.write(report)
        outFile.close()

if __name__ == "__main__":
    main()
