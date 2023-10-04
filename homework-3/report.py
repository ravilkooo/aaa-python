def create_report_csv_header() -> str:
    """
    Generates a header string for the summary report CSV file

        Returns:
            csv_header (str): The header string in CSV format
    """
    return ';'.join(['Департамент', 'Численность',
                     'Мин ЗП', 'Макс ЗП', 'Сред ЗП'])


def download_data(link: str = './Corp_Summary.csv') -> dict:
    """
    Loads employee data from a file located at the specified [link],
    and returns it as a dictionary

        Parameters:
            link (str): The path to the employee file

        Returns:
            data_base_dict (dict): A dictionary containing information
            about the company's employees
    """
    data_base_dict = dict()
    with open(link, 'r', encoding="utf8") as f:
        lines = f.readlines()
        data_base_dict = dict()
        for line in lines[1:]:
            # name, department, team, job, review, salary
            raw_data = line.strip().split(';')
            raw_data[4] = float(raw_data[4])
            raw_data[5] = int(raw_data[5])
            employee = (raw_data[0], raw_data[3], raw_data[4], raw_data[5])
            if raw_data[1] in data_base_dict:
                if raw_data[2] in data_base_dict[raw_data[1]]:
                    data_base_dict[raw_data[1]][raw_data[2]].append(employee)
                else:
                    data_base_dict[raw_data[1]][raw_data[2]] = [employee]
            else:
                data_base_dict[raw_data[1]] = dict()
                data_base_dict[raw_data[1]][raw_data[2]] = [employee]
    return data_base_dict


def team_hierarchy(data_base_dict: dict):
    """
    Displays the hierarchy of teams within the company in the console

        Parameters:
            data_base_dict (dict): A dictionary containing information
            about the company's employees
    """
    for department in data_base_dict:
        print(department)
        team_number = len(data_base_dict[department])
        team_counter = 0
        for team in data_base_dict[department]:
            team_counter += 1
            if team_counter == team_number:
                print(f'{"": ^5}╚{team}')
            else:
                print(f'{"": ^5}╠{team}')


def print_report_header():
    """
    Prints the header of the summary report table to the console
    """
    print('{:-^64}'.format(''))
    print('{:^15}'.format('Департамент'), end='')
    print('|{:^15}'.format('Численность'), end='')
    for s in ['Мин ЗП', 'Макс ЗП', 'Сред ЗП']:
        print('|{:^10}'.format(s), end='')
    print()
    print('{:-^64}'.format(''))


def print_report_line(department: str, dep_summary: list):
    """
    Prints line of the report table about department summary infrormation
    to the console

        Parameters:
        department (str): name of the department
        dep_summary (list): summary information about department
    """
    print('{:<14} '.format(department), end='')
    print('|{:>14} '.format(dep_summary[0]), end='')
    for s in [dep_summary[1], dep_summary[2]]:
        print('|{:>9} '.format(s), end='')
    print('|{:>9.2f} '.format(dep_summary[3]))


def show_report(data_base_dict: dict) -> dict:
    """
    Displays a summary report for all departments in the console and returns it
    as a dictionary

        Parameters:
            data_base_dict (dict): A dictionary containing information
            about the company's employees

        Returns:
            summary_report (dict): A dictionary containing the summary report
            for all departments
    """
    summary_report = dict()
    print_report_header()
    for department in data_base_dict:
        empl_number = 0
        first_team = next(iter(data_base_dict[department]))
        first_empl_sal = float(data_base_dict[department][first_team][0][-1])
        max_sal = first_empl_sal
        min_sal = first_empl_sal
        sum_sal = 0
        for team in data_base_dict[department]:
            for employee in data_base_dict[department][team]:
                empl_number += 1
                employee_sal = float(employee[-1])
                max_sal = max(max_sal, employee_sal)
                min_sal = min(min_sal, employee_sal)
                sum_sal += employee_sal
        avg_sal = sum_sal / empl_number
        summary_report[department] = [empl_number, min_sal, max_sal, avg_sal]
        print_report_line(department, summary_report[department])
    # Prints the footer of the summary report table to the console
    print('{:-^64}'.format(''))
    return summary_report


def save_report(summary_report: dict, link: str = 'Report.csv'):
    """
    Saves a summary report for all departments in the file located at the
    specified [link]

        Parameters:
            summary_report (dict): A dictionary containing the summary report
            for all departments
            link (str): The path to the file
    """
    with open(link, 'w', encoding="utf8") as f:
        f.write(create_report_csv_header())
        f.write('\n')
        if (summary_report):
            for department, info in summary_report.items():
                f.write(f'{department};{info[0]};')
                f.write(';'.join(map(lambda x: "{:.2f}".format(x), info[1:])))
                f.write('\n')


def print_menu():
    """
    Prints the program menu to the console
    """
    print('1) Иерархия команд')
    print('2) Сводный отчёт по департаментам')
    print('3) Сохранить сводный отчёт')


def start_program():
    """
    Launches the program
    """
    data_base_dict = download_data()
    summary_report = None
    exit_program = False
    while not exit_program:
        print_menu()
        option = int(input())
        if option == 1:
            team_hierarchy(data_base_dict)
        elif option == 2:
            summary_report = show_report(data_base_dict)
        elif option == 3:
            save_report(summary_report)
