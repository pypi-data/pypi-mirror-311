# from lesya.language.name_case import NameCaseUa
from lesya.language.case_helpers import CaseUA, Gender


def test():
    from lesya.language.name_case import Lesya
    persons = []
    persons.append("Кравчук Леонід Данилович")
    persons.append("Редзюк Данило Петро")
    persons.append("Кушнір Василь Францевич")
    persons.append("Троцько Павло Карімович")
    persons.append("Устинов Ігор Юрійович")
    persons.append("Рілля Олег Йосипович")
    persons.append("Правдивець  Ілля Іванович")
    persons.append("Кравець  Сидір Іванович")
    persons.append("Швець  Ілля Іванович")
    persons.append("Заєць  Миколай Йосипович")
    persons.append("Воробей  Джек Стіговіч")
    persons.append("Узвіз Матвій Йосипович")
    persons.append("Лебідь  Анрі Йосипович")
    persons.append("Півень  Йосип Йосипович")
    persons.append("Стрілець Прокіп Йосипович")
    persons.append("Тілець Федір Йосипович")
    persons.append("Корінець Прокіп Йосипович")
    persons.append("Стрілець Мішель Йорданівна")
    persons.append("Кремінь Франсуа Йосипович")
    persons.append("Кисіль Жак Йосипович")
    persons.append("Федьо Дзига Петрович")
    persons.append("Дзех Джуліан Петрович")
    persons.append("Пес Максим Петрович")
    persons.append("Василина Володимир Петрович")
    persons.append("Завгородняя Ольга Петрівна")
    persons.append("Завгородній Бідон Петрович")
    persons.append("Палій Андрій Петрович")
    persons.append("Журавель Карім Петрович")
    persons.append("Гафаров  Карім  Шакир Огли")
    persons.append("Жнець  Яків Йосипович")
    persons.append("Болотній Андрій Петрович")

    persons.append("Якір  Андрій Ісакович")
    persons.append("Озмітель Кирило Ісакович")
    persons.append("Мягких Генадій Ісакович")
    persons.append("Пелих Ростислав Мітрофанович")
    persons.append("Горячих Володимир Мітрофанович")
    persons.append("Бодайбей  Сидір Йосипович")
    persons.append("Костів Петро Петрович")
    persons.append("Нечуй-Левицький Пантелеймон-Любомир Петрович")
    persons.append("Дональд Трамп")
    persons.append("Джо Байден")
    persons.append("Дуєйн Джонсон")
    persons.append("Тейлор Свіфт")
    persons.append("Камала Гаріс")
    persons.append("Камала Гаріс")
    persons.append("Емануель Макрон")
    persons.append("Емануель Макрон")
    persons.append("Тарас Григорович Шевченко")
    persons.append("Іван Семенович Нечуй-Левицький")

    # ncl = NameCaseUa()
    for person in persons:
        lesya = Lesya(person, gender='male')
        print(lesya.forms)
        print(CaseUA.DATIVE, lesya.dative)
        print(CaseUA.PREPOSITIONAL, lesya[CaseUA.PREPOSITIONAL])
        for case, form in lesya.forms.items():
            print(f'{case}: {form}')
        print('=' * 55)

    # person = Lesya('Джо Байден', gender='male')
    # print(person[CaseUA.DATIVE])  # Джозефу Байдену
    # print(person[CaseUA.PREPOSITIONAL])  # Джозефові Байденові
    #
    # person = Lesya('Камала Гаріс', gender=Gender.FEMALE)
    # print(person[CaseUA.DATIVE])  # Камалі Гаріс
    # print(person[CaseUA.PREPOSITIONAL])  # Камалі Гаріс

    person = Lesya('Тарас Григорович Шевченко')
    print(person[CaseUA.DATIVE])  # Тарасу Григоровичу Шевченку
    print(person[CaseUA.PREPOSITIONAL])  # Тарасові Григоровичу Шевченкові
    print(person['орудний'])  # Тарасом Григоровичем Шевченком


    person = Lesya('Людвіг ван Бетховен', gender='male')
    print(person.nominative)  # Іван Сидоренко
    print(person.genitive)  # Івана Сидоренка
    print(person.dative)  # Івану Сидоренку
    print(person.accusative)  # Івана Сидоренка
    print(person.instrumental)  # Іваном Сидоренком
    print(person.prepositional)  # Івані Сидоренку
    print(person.vocative)

    person = Lesya('Хасан ібн Хорезмі', gender='male')
    print(person.nominative)  # Іван Сидоренко
    print(person.genitive)  # Івана Сидоренка
    print(person.dative)  # Івану Сидоренку
    print(person.accusative)  # Івана Сидоренка
    print(person.instrumental)  # Іваном Сидоренком
    print(person.prepositional)  # Івані Сидоренку
    print(person.vocative)


if __name__ == '__main__':
    test()