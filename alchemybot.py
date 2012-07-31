import sys
import socket
import string
import time, os
import random


argv_flag = {'-c':None, '-h':None, '-p':None, '-k':None}
flag_help = {'-c':'channel ',
             '-h':'host',
             '-p':'port',
             '-k':'character to call on bot'}
show_help = 'Icorrect argument, "{} -help" for help'.format(sys.argv[0])

def cmd_arg():
    '''return IrcBot object based on values supplied by sys.argv'''
    arguments = sys.argv
    if len(sys.argv) == 1:
        connect = IrcBot()
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-help':
            print('')
            for key in flag_help.keys():
                print('\t{0} -- {1}'.format(key, flag_help[key]))
            sys.exit()
        else:
            print(show_help)
    else:
        h, p, c , k = None, None, None, None
        for flag in argv_flag.keys():
            for user_flag in arguments:
                if flag == user_flag:
                    index = arguments.index(user_flag)
                    value = arguments[index + 1]
                    argv_flag[flag] = value
        connect = IrcBot(h=argv_flag['-h'], p=argv_flag['-p'], c=argv_flag['-c'],
                          k=argv_flag['-k'])
    return connect

class IrcBot:
    def __init__(self, h=None, p=None, c=None, k=None):
        '''adjust values based on sys.argv'''
        if h is None:
            self.host = "irc.freenode.net"
        else:
            self.host = h
        if p is None:
            self.port = 6667
        else:
            self.port = p
        if c is None:
            self.channel = '#robgraves'
        else:
            if c[:1] != '#':
                c = '#'+c
            self.channel = c
        if k is None:
            self.contact = ':'
        else:
            self.contact = k
            
        self.nick = "alchemybot"
        self.ident = "alchemybot"
        self.realname = "alchemybot"
        self.list_cmds = {
            'help':(lambda:self.help()),
            'c':lambda:self.combine(a=None,b=None),
            'restart':lambda:self.restart(password=None),
            'view':lambda:self.view()
            }
        
        self.op = ['metulburr','Awesome-O', 'robgraves','corp769',
                  'metulburr1', 'robgravesny', 'Optichip', 'Craps_Dealer']
        self.data = None
        self.operation = None
        self.addrname = None
        self.username = None
        self.text = None
        self.timer= None
        
        #self.picklepath = '/home/metulburr/Documents/alchemybotlist.pkl'
        
        self.made = ['earth', 'water','air','fire']
        self.items = {
            ('city', 'water'): 'venice',
            ('coin', 'paper'): 'money',
            ('fish', 'poison'): 'fugu',
            ('berry', 'pressure'): 'juice',
            ('cheese', 'dough'): 'pizza',
            ('philosophy', 'stone'): 'philosophers_stone',
            ('warrior', 'cart'): 'chariot',
            ('air', 'fire'): 'energy',
            ('brick', 'concrete'): 'brick_house',
            ('zombie', 'corpse'): 'undead',
            ('alcohol', 'water'): 'vodka',
            ('cat', 'country'): 'egypt',
            ('clay', 'life'): 'golem',
            ('cloth', 'man'): 'clothing',
            ('man', 'bat'): 'batman*',
            ('storm', 'electricity'): 'thunderstorm',
            ('wolf', 'man'): 'dog',
            ('earth', 'algae'): 'mushroom',
            ('assassin', 'firearms'): 'sniper',
            ('coca_cola', 'geyser'): 'mentos',
            ('snake', 'electricity'): 'electric_eel',
            ('man', 'metal'): 'tool',
            ('tool', 'wool'): 'cloth',
            ('fire', 'sand'): 'glass',
            ('water', 'seed'): 'flower',
            ('brick_house', 'sick'): 'hospital',
            ('the_beatles', 'country'): 'united_kingdom',
            ('earth', 'plankton'): 'worm',
            ('pressure', 'sand'): 'silicon',
            ('earth', 'earth'): 'pressure',
            ('hero', 'fire'): 'firefighter',
            ('skyscraper', 'light'): 'lighthouse',
            ('life', 'dust'): 'mite',
            ('shells', 'worm'): 'snail',
            ('grass', 'fruit'): 'berry',
            ('sex', 'city'): 'sex_and_the_city',
            ('clay', 'limestone'): 'cement',
            ('vampire', 'werewolf'): 'twilight_saga',
            ('corpse', 'bird'): 'vulture',
            ('man', 'man'): 'sex',
            ('wood', 'knife'): 'stake',
            ('steam_engine', 'gasoline'): 'combustion_engine',
            ('tree', 'tree'): 'grove',
            ('lizard', 'swamp'): 'frog',
            ('man', 'flu'): 'sick',
            ('desert', 'tree'): 'cactus',
            ('scissors', 'combustion_engine'): 'lawn_mower',
            ('feather', 'paper'): 'book',
            ('fire', 'limestone'): 'lime',
            ('paper', 'zombie'): 'mummy',
            ('sith', 'jedi'): 'star_wars',
            ('grape', 'alcohol'): 'wine',
            ('beast', 'forest'): 'bear',
            ('glass', 'sand'): 'hourglass',
            ('glass', 'bacteria'): 'petri_dish',
            ('man', 'light_bulb'): 'idea',
            ('grass', 'swamp'): 'reed',
            ('scotland', 'clothing'): 'kilt',
            ('electricity', 'light_bulb'): 'light',
            ('beast', 'hunter'): 'wool',
            ('bee', 'tree'): 'honey',
            ('lava', 'pressure'): 'volcano',
            ('life', 'sand'): 'seed',
            ('boat', 'combustion_engine'): 'motorboat',
            ('bird', 'hunter'): 'feather',
            ('metal', 'wind'): 'sound',
            ('hunter', 'fish'): 'fisherman',
            ('beast', 'water'): 'whale',
            ('carbon_dioxide', 'water'): 'soda_water',
            ('boiler', 'coal'): 'steam_engine',
            ('arable', 'seed'): 'wheat',
            ('moon', 'metal'): 'silver',
            ('alcohol', 'wheat'): 'beer',
            ('mushroom', 'algae'): 'lichen',
            ('book', 'sex'): 'kama_sutra',
            ('forest', 'hero'): 'robin_hood',
            ('man', 'yogurt'): 'diet',
            ('vodka', 'country'): 'russia',
            ('boat', 'man'): 'sailor',
            ('philosophers_stone', 'silver'): 'gold',
            ('metal', 'tool'): 'arms',
            ('air', 'lava'): 'stone',
            ('light', 'beetle'): 'firefly',
            ('stone', 'water'): 'sand',
            ('dilemma', 'scientist'): 'philosophy',
            ('fire', 'stone'): 'metal',
            ('beast', 'man'): 'livestock',
            ('country', 'country'): 'continent',
            ('country', 'fondue'): 'switzerland',
            ('man', 'vicodin'): 'house_m.d.',
            ('earth', 'moss'): 'grass',
            ('fossil', 'life'): 'zombie',
            ('hourglass', 'electricity'): 'clock',
            ('oxygen', 'man'): 'carbon_dioxide',
            ('storm', 'water'): 'typhoon',
            ('wine', 'soda_water'): 'champagne',
            ('flu', 'bird'): 'avian_flu',
            ('mold', 'scientist'): 'penicillin',
            ('paper', 'tobacco'): 'cigarettes',
            ('earth', 'seed'): 'tree',
            ('clay', 'fire'): 'brick',
            ('ufo', 'arable'): 'crop_circles',
            ('bird', 'ice'): 'penguin',
            ('scientist', 'energy'): 'albert_einstein',
            ('fire', 'meat'): 'barbecue',
            ('sea', 'volcano'): 'island',
            ('energy', 'metal'): 'electricity',
            ('limestone', 'manure'): 'saltpeter',
            ('star', 'life'): 'alien',
            ('arms', 'man'): 'hunter',
            ('sky', 'chariot'): 'sun',
            ('1UP', 'man'): 'mario',
            ('stone', 'tool'): 'statue',
            ('sugar', 'fire'): 'caramel',
            ('man', 'time'): 'old_man',
            ('usa', 'statue'): 'statue_of_liberty',
            ('water', 'wood'): 'boat',
            ('bicycle', 'combustion_engine'): 'motorcycle',
            ('earth', 'egg'): 'dinosaur',
            ('arms', 'hunter'): 'warrior',
            ('wheel', 'wood'): 'cart',
            ('man', 'sex'): 'baby',
            ('metal', 'bird'): 'airplane',
            ('water', 'sand'): 'beach',
            ('aluminium', 'glass'): 'mirror',
            ('meat', 'bread'): 'sandwich',
            ('cheese', 'sky'): 'moon',
            ('ash', 'fat'): 'soap',
            ('coca_cola', 'country'): 'usa',
            ('cart', 'steam_engine'): 'locomotive',
            ('brick_house', 'beer'): 'bar',
            ('bacteria', 'plankton'): 'fish',
            ('tree', 'beast'): 'panda',
            ('steam', 'earth'): 'geyser',
            ('kerogen', 'pressure'): 'bitumen',
            ('alcohol', 'peat'): 'scotch_whiskey',
            ('man', 'alcohol'): 'alcoholic',
            ('sound', 'idea'): 'music',
            ('jedi', 'swamp'): 'yoda',
            ('blood', 'man'): 'vampire',
            ('arms', 'poison'): 'poisoned_weapons',
            ('hospital', 'scientist'): 'doctor',
            ('fire', 'bread'): 'toast',
            ('ceramics', 'coin'): 'piggy_bank',
            ('robin_hood', 'arms'): 'bow',
            ('bitumen', 'pressure'): 'petroleum',
            ('microchip', 'book'): 'e_book',
            ('lawn mower', 'arable'): 'tractor',
            ('fire', 'grass'): 'tobacco',
            ('silver', 'pressure'): 'coin',
            ('vw_beetle', 'country'): 'germany',
            ('air', 'earth'): 'dust',
            ('air', 'bacteria'): 'flu',
            ('cart', 'combustion_engine'): 'car',
            ('mushroom', 'mud'): 'mold',
            ('aluminium', 'oxygen'): 'ruby',
            ('fire', 'glass'): 'lamp',
            ('moon', 'beast'): 'wolf',
            ('bacteria', 'swamp'): 'sulfur',
            ('energy', 'swamp'): 'life',
            ('flower', 'beetle'): 'bee',
            ('moss', 'swamp'): 'fern',
            ('petroleum', 'pressure'): 'gasoline',
            ('earth', 'corpse'): 'grave',
            ('book', 'book'): 'library',
            ('forest', 'ghost'): 'totoro',
            ('soda_water', 'carmine'): 'coca_cola',
            ('firearms', 'man'): 'soldier',
            ('stone', 'wheat'): 'flour',
            ('warrior', 'lightsaber'): 'jedi',
            ('chocolate', 'fire'): 'hot_chocolate',
            ('clay', 'man'): 'ceramics',
            ('seed', 'mexico'): 'cocoa',
            ('sushi', 'country'): 'japan',
            ('jedi', 'assassin'): 'sith',
            ('air', 'energy'): 'storm',
            ('egg', 'sand'): 'turtle',
            ('earth', 'water'): 'swamp',
            ('livestock', 'man'): 'milk',
            ('tree', 'lightbulb'): 'christmas_tree',
            ('metal_golem', 'electicity'): 'robot',
            ('cloth', 'wooden_ship'): 'sailing_ship',
            ('chicken', 'hut'): 'hen_coop',
            ('petroleum', 'country'): 'saudi_arabia',
            ('airplane', 'metal'): 'aluminium',
            ('dinosaur', 'air'): 'pterodactyl',
            ('woman', 'fish'): 'mermaid',
            ('silicon', 'electricity'): 'transistor',
            ('fire', 'pig'): 'bacon',
            ('beast', 'life'): 'man',
            ('sand', 'swamp'): 'clay',
            ('feather', 'cloth'): 'pillow',
            ('life', 'stone'): 'egg',
            ('beast', 'cart'): 'team',
            ('earth', 'tool'): 'arable',
            ('algae', 'fire'): 'iodine',
            ('boat', 'cloth'): 'sailboat',
            ('swamp', 'tree'): 'peat',
            ('knife', 'knife'): 'scissors',
            ('arms', 'light'): 'lightsaber',
            ('dinosaur', 'water'): 'plesiosauria',
            ('lava', 'life'): 'lava_golem',
            ('pig', 'flu'): 'swine_flu',
            ('reed', 'tool'): 'paper',
            ('alien', 'airplane'): 'ufo',
            ('metal', 'steam'): 'boiler',
            ('mouse', 'hunter'): 'cat',
            ('quark_cheese', 'fire'): 'cheese',
            ('man', 'tobacco'): 'cancer',
            ('oxygen', 'electricity'): 'ozone',
            ('tractor', 'country'): 'belarus',
            ('dust', 'water'): 'mud',
            ('fire', 'flying_dinosaur'): 'dragon',
            ('fire', 'alcohol'): 'molotov_cocktail',
            ('bacteria', 'milk'): 'yogurt',
            ('assassin', 'time'): 'prisoner',
            ('transylvania', 'country'): 'romania',
            ('kama_sutra', 'country'): 'india',
            ('air', 'worm'): 'butterfly',
            ('air', 'water'): 'steam',
            ('water', 'glass'): 'ice',
            ('dragon', 'warrior'): 'hero',
            ('vampire', 'country'): 'transylvania',
            ('soured_milk', 'fire'): 'whey',
            ('life', 'swamp'): 'bacteria',
            ('life', 'water'): 'algae',
            ('beast', 'museum'): 'zoo',
            ('light', 'storm'): 'rainbow',
            ('snake', 'bird'): 'quetzalcoatl',
            ('1up', 'egg'): 'yoshi',
            ('flour', 'water'): 'dough',
            ('bird', 'vampire'): 'bat',
            ('continent', 'continent'): 'planet',
            ('fish', 'fish'): 'caviar',
            ('lava', 'lamp'): 'lava_lamp',
            ('chicken', 'fire'): 'fried_chicken',
            ('shells', 'stone'): 'limestone',
            ('city', 'city'): 'country',
            ('lamp', 'ghost'): 'genie',
            ('skyscraper', 'skyscraper'): 'city',
            ('bird', 'fire'): 'phoenix',
            ('car', 'life'): 'transformers',
            ('alcohol', 'worm'): 'tequila',
            ('old_man', 'christmas_tree'): 'santa_claus',
            ('grass', 'livestock'): 'manure',
            ('uncut_diamond', 'tool'): 'diamond',
            ('china', 'cloth'): 'silk',
            ('alcohol', 'flower'): 'perfume',
            ('venice', 'country'): 'italy',
            ('man', 'mcdonalds'): 'obesity',
            ('cheese', 'fire'): 'fondue',
            ('sick', 'doctor'): 'vicodin',
            ('dragon', 'country'): 'china',
            ('fire', 'water'): 'alcohol',
            ('snake', 'worm'): 'lizard',
            ('fish', 'electricity'): 'electric_ray',
            ('scotch_whisky', 'country'): 'scotland',
            ('cat', 'dog'): 'catdog',
            ('man', 'seed'): 'farmer',
            ('egg', 'life'): 'chicken',
            ('dough', 'fire'): 'bread',
            ('champagne', 'country'): 'france',
            ('beetle', 'sand'): 'scorpion',
            ('cheese', 'beast'): 'mouse',
            ('fire', 'man'): 'corpse',
            ('sand', 'shells'): 'pearl',
            ('air', 'steam'): 'cloud',
            ('ghost', 'energy'): 'ectoplasm',
            ('fire', 'tree'): 'coal',
            ('life', 'hourglass'): 'time',
            ('air', 'cloud'): 'sky',
            ('water', 'electricity'): 'oxygen',
            ('man', 'pig'): 'salo',
            ('earth', 'worm'): 'beetle',
            ('swamp', 'worm'): 'snake',
            ('wheel', 'wool'): 'spinning_wheel',
            ('air', 'egg'): 'bird',
            ('arms', 'gunpowder'): 'firearms',
            ('sand', 'sand'): 'desert',
            ('lime', 'reed'): 'sugar',
            ('tree', 'farmer'): 'fruit',
            ('cactus', 'beetle'): 'cochineal',
            ('beetle', 'manure'): 'scarab',
            ('fire', 'life'): 'fire_elemental',
            ('car', 'beetle'): 'vw_beetle',
            ('dam', 'beast'): 'beaver',
            ('whale', 'earth'): 'elephant',
            ('yarn', 'tool'): 'sweater',
            ('library', 'man'): 'scientist',
            ('oxygen', 'hydrogen'): 'oxyhydrogen',
            ('egg', 'diamond'): 'faberge_egg',
            ('grove', 'grove'): 'forest',
            ('air', 'air'): 'wind',
            ('steam', 'hut'): 'sauna',
            ('transistor', 'transistor'): 'microchip',
            ('tool', 'wood'): 'wheel',
            ('ash', 'glass'): 'ashtray',
            ('plankton', 'stone'): 'shells',
            ('ash', 'life'): 'ghost',
            ('salo', 'country'): 'ukraine',
            ('fossil', 'pressure'): 'kerogen',
            ('chicken', 'egg'): 'dilemma',
            ('wood', 'life'): 'pinocchio',
            ('knife', 'tool'): 'swiss_army_knife',
            ('cochineal', 'fire'): 'carmine',
            ('steam_engine', 'wooden_ship'): 'steamer',
            ('man', 'stone'): 'hut',
            ('sauna', 'country'): 'finland',
            ('desert', 'beast'): 'camel',
            ('scorpion', 'water'): 'lobster',
            ('star_wars', 'robot'): 'r2_d2',
            ('bird', 'storm'): 'thunderbird',
            ('water', 'water'): 'sea',
            ('meat', 'tool'): 'knife',
            ('cocoa', 'sugar'): 'chocolate',
            ('alcohol', 'oxygen'): 'vinegar',
            ('tequila', 'country'): 'mexico',
            ('brick_house', 'glass'): 'skyscraper',
            ('swamp', 'algae'): 'moss',
            ('flour', 'beetle'): 'weevil',
            ('storm', 'sand'): 'sandstorm',
            ('coca_cola', 'sandwich'): 'mcdonalds',
            ('electricity', 'glass'): 'light_bulb',
            ('sugar', 'seed'): 'beetroot',
            ('sun', 'flower'): 'sunflower',
            ('tool', 'tree'): 'wood',
            ('milk', 'yogurt'): 'soured_milk',
            ('kangaroo', 'country'): 'austrialia',
            ('man', 'poisoned_weapons'): 'assassin',
            ('cement', 'water'): 'concrete',
            ('beetle', 'beetle'): 'the_beatles',
            ('life', 'metal'): 'metal_golem',
            ('brick', 'water'): 'dam',
            ('fire', 'tobacco'): 'smoke',
            ('hospital', 'car'): 'ambulance',
            ('dust', 'fire'): 'gunpowder',
            ('hunter', 'ghost'): 'ghostbusters',
            ('earth', 'wood'): 'grape',
            ('frog', '1UP'): 'kangaroo',
            ('boat', 'wood'): 'wooden_ship',
            ('sun', 'scientist'): 'star',
            ('coal', 'pressure'): 'uncut_diamond',
            ('gasoline', 'fire'): 'explosion',
            ('corpse', 'electricity'): 'frankenstein',
            ('egg', 'fire'): 'omelette',
            ('sea', 'fire'): 'salt',
            ('fish', 'algae'): 'sushi',
            ('volcano', 'country'): 'iceland',
            ('water', 'metal'): 'rust',
            ('doctor', 'lobster'): 'dr._zoidberg',
            ('tree', 'life'): 'ent',
            ('wheel', 'wheel'): 'bicycle',
            ('spinning_wheel', 'wool'): 'yarn',
            ('earth', 'fire'): 'lava',
            ('beetroot', 'fire'): 'borscht',
            ('bicycle', 'cancer'): 'lance_armstrong',
            ('earth', 'lizard'): 'beast',
            ('dinosaur', 'earth'): 'fossil',
            ('grave', 'grave'): 'cemetery',
            ('beast', 'vampire'): 'werewolf',
            ('fire', 'lizard'): 'salamander',
            ('baby', 'time'): 'woman',
            ('brick_house', 'fossil'): 'museum',
            ('mushroom', 'tool'): 'poison',
            ('bacteria', 'water'): 'plankton',
            ('blood', 'worm'): 'leech',
            ('thunderstorm', 'metal'): 'lightning_rod',
            ('corpse', 'wood'): 'coffin',
            ('livestock', 'mud'): 'pig',
            
            
        #micahs definitions
            ('metal', 'music'):'dave_mustaine',
            ('microchip', 'electricity'):'computer',
            ('computer', 'man'):'minecraft',
            ('car', 'electricity'):'electric_car',
            ('man', 'usa'):'president',
            ('president', 'prisoner'):'richard_nixon',
            ('pizza', 'man'):'delivery_driver',
            ('corpse', 'man'):'skeleton',
            ('thunderstorm', 'man'):'benjamin_franklin',
            ('computer', 'sky'):'satellite',
            ('satellite', 'satellite'):'space_station',
            ('wood', 'tool'):'bowl',
            ('president', 'woman'):'first_lady',
            ('assassin', 'president'):'abraham_lincoln',
            ('wood', 'man'):'contractor',
            ('contractor', 'contractor'):'construction',
            ('electricity', 'prisoner'):'electric_chair',
            ('pearl', 'man'):'enderman',
            ('electricity', 'metal'):'wire',
            ('hut', 'hut'):'village',
            ('desert', 'water'):'oasis',
            ('air', 'pressure'):'atmosphere',
            ('stone', 'metal'):'blade',
            ('stone', 'stone'):'boulder',
            ('sand', 'wind'):'dune',
            ('sky', 'water'):'rain',
            ('rain', 'rain'):'flood',
            ('sea', 'water'):'ocean',
            ('brick', 'brick'):'wall',
            ('wall', 'wall'):'great_wall_of_china',
            ('ocean', 'wind'):'wave',
            ('brick_house', 'wind'):'windmill',
            ('earth', 'rain'):'plant',
            ('man', 'rain'):'cold',
            ('cold', 'rain'):'snow',
            ('snow', 'snow'):'igloo',
            ('man', 'snow'):'snowman',
            ('cold', 'time'):'frostbite',
            ('forest', 'rain'):'rainforest',
            ('earth', 'energy'):'earthquake',
            ('sun', 'tool'):'solar_cell',
            ('man', 'woman'):'love',
            ('music', 'music'):'song',
            ('man', 'song'):'singer',
            ('singer', 'singer'):'quire',
            ('star', 'sky'):'space',
            ('space', 'airplane'):'rocket',
            ('farmer', 'grass'):'hay',
            ('livestock', 'hay'):'horse',
            ('sun', 'moon'):'eclipse',
            ('gunpowder', 'metal'):'bullet',
            ('bullet', 'metal'):'gun',
            ('knife', 'grass'):'scythe',
            ('scythe', 'corpse'):'grim_reaper',
            ('glass', 'metal'):'glasses',
            ('glasses', 'man'):'nerd',
            ('blade', 'metal'):'sword',
            ('sword', 'metal'):'katana',
            
            }
        #sound
        
        self.sock = self.irc_conn()
        self.wait_event()
        
    def irc_conn(self):
        '''connect to server/port channel, send nick/user '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('connecting to "{0}/{1}"'.format(self.host, self.port))
        sock.connect((self.host, self.port))
        print('sending NICK "{}"'.format(self.nick))
        sock.send("NICK {0}\r\n".format(self.nick).encode())
        sock.send("USER {0} {0} bla :{0}\r\n".format(
            self.ident,self.host, self.realname).encode())
        print('joining {}'.format(self.channel))
        sock.send(str.encode('JOIN '+self.channel+'\n'))
        return sock
    
    def say(self, string):
        '''send string to irc channel with PRIVMSG '''
        self.sock.send('PRIVMSG {0} :{1}\r\n'.format(self.channel, string).encode())
    
    def send_operation(self, operation=None, msg=None, username=None):
        '''send operation to irc with operation arg'''
        if msg is None:
            #send ping pong operation
            self.sock.send('{0} {1}\r\n'.format(operation, self.channel).encode())
        elif msg != None:
            #send private msg to one username
            self.sock.send('PRIVMSG {0} :{1}\r\n'.format(self.username,msg).encode())
    def get_user(self, stringer):
        start = stringer.find('~')
        end = stringer.find('@')
        user = stringer[start +1:end]
        return user
        
    def format_data(self):
        '''get data from server:
        self.operation = EXAMPLE: PRIVMSG, JOIN, QUIT
        self.text = what each username says
        self.addrname = the first name on address
        self.username = the username
        self.timer = time 
        '''
        data=self.sock.recv(1042) #recieve server messages
        data = data.decode('utf-8') #data decoded
        self.data = data.strip('\n\r') #data stripped
        try:
            self.operation = data.split()[1]
            textlist = data.split()[3:]
            text = ' '.join(textlist)
            self.text = text[1:]
            self.addrname = self.get_user(data) 
            self.username = data[:data.find('!')][1:]
        except IndexError:
            pass
        self.timer = time.asctime(time.localtime(time.time()))
        
    def print_console(self):
        '''print to console '''
        #print('{0} ({1}): {2}'.format(self.username, self.timer, self.text))
        print(self.data)
        
    def ping_pong(self):
        '''server ping pong handling'''
        try:
            if self.data[:4] == 'PING':
                self.send_operation('PONG')
        except TypeError: #startup data
            pass
        
    def upon_join(self):
        '''when someone joins the channel'''
        if self.operation == 'JOIN':
            pass
    
    def upon_leave(self):
        '''when someone leaves the channel'''
        if self.operation == 'QUIT' or self.operation == 'PART':
            pass
        
    def wait_event(self):
        #time.sleep(10) #wait to connect before starting loop
        while True:
            self.ping_pong()
            self.format_data()
            self.print_console()
            self.upon_join()
            self.upon_leave()
            self.check_cmd()
            
    def not_cmd(self, cmd):
        return '{0}: "{1}" is not one of my commands'.format(self.username, cmd)

    def check_cmd(self):
        '''check if contact is first char of text and send in cmd and its args to crapdealer_commands.commands'''
        if self.text[:1] == self.contact:
            returner = self.commands(self.text.split()[0][1:], self.text.split()[1:])
            if returner != None:
                self.say(returner)

    def commands(self, cmd, *args):
        try:
            arg1 = args[0][0]
        except IndexError:
            arg1 = ''
        try:
            arg2 = args[0][1]
        except IndexError:
            arg2 = ''

        if cmd in self.list_cmds:
            if not arg1: #if no arguments
                self.list_cmds[cmd]()
            else: #argument with function, run function directly
                if cmd == 'help':# and arg1 in self.list_cmds.keys():
                    self.help(arg1)
                elif cmd == 'c':
                    try:
                        self.combine(arg1,arg2)
                    except:
                        pass
                elif cmd == 'restart':
                    try:
                        self.restart(arg1)
                    except:
                        pass
            #self.say('cmd is: {}'.format(cmd))
            #self.say('first two args are: {0} {1}'.format(arg1, arg2))
        elif cmd != '':
            self.say(self.not_cmd(cmd))
            
    def help(self, arg=None):
        helper = '{0}: {1}help  --show all commands'.format(self.username,self.contact)
        combine = '{0}: {1}c [element] [element] --combine [element] with [element] either order'.format(self.username,self.contact)
        restart = '{0}: {1}restart --restart alchemy from first 4 elements'.format(self.username,self.contact)
        view = '{0}: {1}view --view your made elements'.format(self.username,self.contact)
        
        if arg is None:
            tmp = []
            for key in self.list_cmds.keys():
                tmp.append(key)
            self.say('{0}help [cmd] for desc. cmds = {1}'.format(self.contact,tmp))
        else:
            if arg == 'help':
                self.say(helper)
            if arg == 'c':
                self.say(combine)
            if arg == 'restart':
                self.say(restart)
            if arg == 'view':
                self.say(view)
                
    def combine(self, a,b):
        lister = self.made
        if a is None or b is None:
            self.help('c')
            return
            
        if a not in lister:
            self.say('{}: You do not have {}'.format(self.username, a))
            return
        elif b not in lister:
            self.say('{}: You do not have {}'.format(self.username, b))
            return
        try:
            if self.items[(a,b)] in lister:
                self.say('{}: You have already made {}'.format(self.username, self.items[(a,b)]))
                return
        except KeyError:
            pass
        try:
            if self.items[(b,a)] in lister:
                self.say('{}: You have already made {}'.format(self.username, self.items[(b,a)]))
                return
        except KeyError:
            pass
        try:
            try:
                if self.items[(a,b)] in lister:
                    return
                self.made.append(self.items[(a,b)])
                #self.create_pkl(self.made)
                self.say('{} has made {}'.format(self.username, self.items[(a,b)]))
            except KeyError:
                pass
            try:
                if self.items[(b,a)] in lister:
                    return
                self.made.append(self.items[(b,a)])
                #self.create_pkl(self.made)
                self.say('{} has made {}'.format(self.username, self.items[(b,a)]))
            except KeyError:
                pass
        except KeyError:
            print('incorrect values')
            
    def restart(self, password):
        if password == '99dsom2r':
            self.made = ['earth', 'water','air','fire']
            self.say('{}: Game restarted with first 4 elements'.format(self.username))
        else:
            self.say('{}: You need a password'.format(self.username))
        
    def view(self):
        lister = sorted(self.made)
        header ='Made Items: {}, Total Items: {}'.format(len(lister), len(self.items))
        self.sock.send('PRIVMSG {} :{} {}\r\n'.format(self.username,header, lister).encode())
        self.say('Made Items: {}, Total Items: {}'.format(len(lister), len(self.items)))
        self.say(lister)
    
    def create_pkl(picklepath, obj):
        files = open(picklepath, 'wb')
        pickle.dump(obj, files)
        files.close()
        
    def load_pkl(picklepath):
        files = open(picklepath, 'rb')
        obj = pickle.load(files)
        return obj

if __name__ == '__main__':
    connect = cmd_arg()
    try:
        print('channel: ', connect.channel)
        print('port: ', connect.port)
        print('host: ', connect.host)
        print('contact: ', connect.contact)
    except NameError:
        print(show_help)
        
        #stone