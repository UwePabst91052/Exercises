from Workpackage import *


def print_workdays(workpackages):
    for wp in workpackages:
        for wd in wp.workdays:
            print(str(wd.date) + " <=> " + str(wd.date.days))


def main():
    workpackages = []
    wp = Workpackage("Arbeitspaket")
    workpackages.append(wp)
    wp.add_workday("02.02.2020")
    wp.add_workday("03.02.2020")
    wp.add_workday("03.03.2020")
    wp.add_workday("01.02.2020")
    wp.add_workday("04.02.2020")
    wp.add_workday("01.03.2020")
    wp.add_workday("02.03.2020")
    wp.add_workday("05.06.2020")
    wp.add_workday("02.05.2020")
    wp.add_workday("03.05.2020")
    wp.add_workday("04.05.2020")
    wp.add_workday("01.05.2020")
    wp.add_workday("01.03.2020")
    wp.add_workday("04.03.2020")
    wp.add_workday("02.05.2020")
    wp.add_workday("03.06.2020")
    wp.add_workday("04.06.2020")

    print_workdays(workpackages)

    print("\n\n=====================================\n\n")
    wp.sort_workdays()

    print_workdays(workpackages)


main()
