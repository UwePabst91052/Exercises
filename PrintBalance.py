import Workpackage as Wp
from ReadWorkpackes import *
from BerichtAusdrucken import create_work_merged
from BerichtAusdrucken import create_work_dictionary
from BerichtAusdrucken import report_work_summary_timespan

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
    ["01.01.2023", "31.12.2023", "Jahr 2023"]
]

parameters2 = [['01.01.2023', '31.12.2023', 'Jahr 2023']]
parameters3 = [['01.01.2024', '31.12.2024', 'Jahr 2024']]

def merge_wpckgs(workpackages):
    mergedWorkpackages = []
    mergedWorkpackages.append(Wp.Workpackage("Merged Workpackages"))

    for wp in workpackages:
        for wd in wp.workdays:
            mergedWorkpackages[0].add_workday(str(wd.date))
            for wt in wd.worktimes:
                wt_strings = str(wt).split(" ", 3)
                mergedWorkpackages[0].begin_working(wt_strings[0])
                mergedWorkpackages[0].finish_working(wt_strings[1])
    mergedWorkpackages[0].sort_workdays()
    return mergedWorkpackages


def show_balance(from_date, until_date, workpackages):
    workpackageMerged = merge_wpckgs(workpackages)
    keylist = create_work_dictionary(workpackageMerged)
    report = report_work_summary_timespan("Otto Normalverbraucher", workpackages, from_date, until_date)
    return report

def main():
    filename = ".\\Dateien\\HomeOfficeNeu.xml"
    
    inFile = open(filename, "r", encoding="utf-8")
    workpackages = read_workpackages(inFile)
    inFile.close()

    for timespan in parameters:
        outfilename = ".\\Dateien\\Balance " + timespan[2] + ".txt"
        outFile = open(outfilename, "w", encoding="utf-8")
        report = show_balance(timespan[0], timespan[1], workpackages)
        outFile.write(report)
        outFile.close()

if __name__ == "__main__":
    main()
