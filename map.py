class Location:
    def __init__(self, title, paths_title, name, paths_name):
        self.title = title
        self.paths = paths_title
        self.name = name
        self.paths_name = paths_name


paths_level = {'path': 0, 'lake': 5, 'meadow': 0, 'town': 0, 'forest': 0, 'meadow2': 0, 'meadow3': 0, 'forest2': 0,
               'forest3': 0, 'forest4': 0, 'path2': 10, 'flower-meadow': 10, 'path3': 0, 'path4': 0, 'path5': 0,
               'path6': 0, 'path7': 0, 'envris-forest': 50, 'seaside': 15, 'seaside2': 15, 'seaside-town': 15,
               'rocks': 30, 'dark-forest': 20, 'dark-forest2': 20, 'dark-envris-forest': 60, 'portal': 0,
               'portal2': 100}

locations = [Location('town', ['path'], 'Торговый город', ['Тропинка к городу']),
             Location('path', ['lake', 'meadow', 'town', 'forest'], 'Тропинка к городу',
                      ['Озеро', 'Луг', 'Торговый город', 'Лес']),
             Location('lake', ['meadow2', 'meadow3', 'path', 'path2'], 'Озеро', ['Луг', 'Луг', 'Тропинка к городу',
                                                                                 'Тропинка к цветочному лугу']),
             Location('meadow2', ['path6', 'lake'], 'Луг', ['Тропинка', 'Озеро']),
             Location('path6', ['forest3', 'meadow2'], 'Тропинка', ['Лес', 'Луг']),
             Location('forest3', ['envris-forest', 'forest4', 'path6'], 'Лес', ['Инврисовый лес', 'Лес', 'Тропинка']),
             Location('forest4', ['path7', 'forest3', 'envris-forest'], 'Лес', ['Тропинка', 'Лес', 'Инврисовый лес']),
             Location('envris-forest', ['forest3', 'forest4'], 'Инврисовый лес', ['Лес', 'Лес']),
             Location('path7', ['meadow3', 'forest4'], 'Тропинка', ['Луг', 'Лес']),
             Location('meadow3', ['lake', 'path7', 'flower-meadow'], 'Луг', ['Озеро', 'Тропинка', 'Цветочный луг']),
             Location('flower-meadow', ['path2', 'meadow3'], 'Цветочный луг', ['Тропинка к цветочному лугу', 'Луг']),
             Location('path2', ['meadow', 'lake', 'flower-meadow'], 'Тропинка к цветочному лугу',
                      ['Луг', 'Озеро', 'Цветочный луг']),
             Location('meadow', ['forest', 'path', 'path2', 'path3'], 'Луг', ['Лес', 'Тропинка к городу',
                                                                              'Тропинка к цветочному лугу',
                                                                              'Тропинка к скалам']),
             Location('forest', ['dark-forest', 'path', 'meadow', 'path4', 'dark-forest2'], 'Лес',
                      ['Темный лес', 'Тропинка к городу',
                       'Луг', 'Тропинка к морю', 'Темный лес']),
             Location('dark-forest', ['dark-envris-forest', 'dark-forest2', 'forest'], 'Темный лес',
                      ['Темный инврисовый лес',
                       'Темный лес', 'Лес']),
             Location('dark-envris-forest', ['dark-forest2', 'dark-forest', 'portal'], 'Темный инврисовый лес',
                      ['Темный лес',
                       'Темный лес',
                       'Прогуляться по лесу']),
             Location('portal', ['dark-envris-forest', 'portal2'], 'Портал', ['Вернуться', 'Войти в портал']),
             Location('portal2', ['portal'], 'Скоро...', ['Вернуться']),
             Location('dark-forest2', ['forest', 'dark-forest', 'dark-envris-forest'], 'Темный лес',
                      ['Лес', 'Темный лес', 'Темный инврисовый лес']),
             Location('path4', ['seaside2', 'forest2', 'path5', 'forest'], 'Тропинка к морю',
                      ['Скалистое побережье', 'Перелески', 'Тропинка к побережью', 'Лес']),
             Location('path5', ['seaside', 'path4'], 'Тропинка к побережье', ['Побережье', 'Тропинка к морю']),
             Location('seaside', ['seaside-town', 'path5'], 'Побережье', ['Прибрежный город', 'Тропинка к побережью']),
             Location('seaside-town', ['seaside2', 'seaside'], 'Прибрежный город',
                      ['Скалистое побережье', 'Побережье']),
             Location('seaside2', ['rocks', 'seaside-town', 'path5'], 'Скалистое побережье',
                      ['Скалы', 'Прибрежный город', 'Тропинка к морю']),
             Location('rocks', ['path3', 'seaside2'], 'Скалы', ['Тропинка к скалам', 'Скалистое побережье']),
             Location('path3', ['forest2', 'rocks', 'meadow'], 'Тропинка к скалам', ['Перелески', 'Скалы', 'Луг']),
             Location('forest2', ['path3', 'path4'], 'Перелески', ['Тропинка к скалам', 'Тропинка к морю'])]
