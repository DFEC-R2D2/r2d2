from collections import namedtuple

# pygecko messages
# KeyPad = namedtuple('KeyPad', 'cmd')
Audio = namedtuple('Audio','file voice')
Servo = namedtuple('Servo', 'action')  # 'wave', ('open', 1)
