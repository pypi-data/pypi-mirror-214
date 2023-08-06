from pyfiglet import Figlet
from importlib.metadata import version


# with open('/home/felixl/Desktop/tmp/fonts.txt') as fh:
#     allfonts = [line.strip() for line in fh if line]
#
#
# good = ['big', 'clb8x10', 'larry3d', 'nancyj', 'ogre', 'roman', 'smisome1', 'stop', 'epic']
#
# for font in good:
#     custom_fig = Figlet(font=font)
#     print(font)
#     print(custom_fig.renderText('ncOrtho'))

custom_fig = Figlet(font='stop')

print(custom_fig.renderText('fDOG'))