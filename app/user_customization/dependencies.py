from enum import Enum

class WorkType(str, Enum):
    THESIS_BACHELOR = "bachelor_thesis"                    # Бакалаврская работа
    THESIS_DIPLOMA = "diploma_thesis"                      # Дипломная работа
    PROJECT_DIPLOMA = "diploma_project"                    # Дипломный проект
    DISSERTATION_MASTER = "master_dissertation"            # Магистерская диссертация

    COURSE_PROJECT = "course_project"                      # Курсовой проект
    COURSE_WORK =  "course_work"                            # Курсовая работа

    PRACTICE_REPORT_EDUCATIONAL = "practice_report_educational"           # Отчёт об учебной практике
    PRACTICE_REPORT_PRODUCTION = "practice_report_production"             # Отчёт о производственной практике
    PRACTICE_REPORT_SCIENTIFIC_PEDAGOGICAL = "practice_report_scientific_pedagogical"  # Отчёт о научно-педагогической практике
    PRACTICE_REPORT = "practice_report"                    # Отчёт о практике (общий)

    LAB_REPORT = "lab_report"                              # Отчёт по лабораторной работе
    PRACTICAL_WORK_REPORT = "practical_work_report"        # Отчёт о практической работе
    PROJECT_EXECUTION_REPORT = "project_execution_report"  # Отчёт о выполнении проекта

    RESEARCH_REPORT_MASTER = "research_report_master"      # Отчёт о научно-исследовательской работе магистранта

    REFERENCE = "reference"                                # Реферат (как самостоятельный документ)
    CALC_GRAPHIC_WORK = "calc_graphic_work"                # Расчётно-графическая работа
    CALC_GRAPHIC_ASSIGNMENT = "calc_graphic_assignment"    # Расчётно-графическое задание
    CALC_ASSIGNMENT = "calc_assignment"                    # Расчётное задание
    CONTROL_WORK = "control_work"                          # Контрольная работа
    ESSAY = "essay"                                        # Эссе