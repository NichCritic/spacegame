"A wooden chair"

obj = {}

wood = {'type': 'wood',
        'descriptor': 'wooden'}

crystal= {'type':'crystal',
          'descriptor': 'crystal'}

chair = {
    '__proto__': obj,
    'name': 'chair',
    'functions': ['sit'],
    'material': wood,
    'descriptors': []
}


table = {
    '__proto__': obj,
    'name': 'table',
    'material': None,
    'descriptors': ['round']
}

"A sweet smell wafts from the roses in the crystal vase on the round table"


rose = {
    'name': 'rose',
    'action': {'type':'smell', 'verb': 'waft', 'strength':100, 'character':'sweet'},
    'descriptors': [],
    'material':""
}

vase = {
    'name': 'vase',
    'material': crystal,
    'descriptors': []
}

rel1 = {
    'location':'in',
    'subject': rose,
    'object':vase
}

rell2 = {
    'location':'on',
    'subject': rel1,
    'object': table
}

