from cognitiveload import User, db

idents = [
    '7yvd4',
    'iz2ps',
    '7swyk',
    'e4gay',
    '2gu87',
    'f1gjp',
    'ef5rq',
    'ctsax',
    'bd47a',
    'c24ur',
    'hpbxa',
    'tn4vl',
    '1mpau',
    'dkhty',
    '94mnx',
    '7dwjy',
    'r89k1',
    'pmyfl',
    'td5pr',
    'gyqu9',
    'fzchw',
    'l53hg',
    '3n2f9',
    '62i9y',
    'ewcqb',
    'pdq51',
    'b3ry5',
    'y87xb',
    '3trsy',
    'm1j3v',
    'iejq4',
    'f3j25',
    'yljm5',
    'ibvx8',
    'b7mrd',
    '2nxs5',
    'wjxci',
    'lmdxn',
    '5gpsc',
    'rc1in',
    '8a1ep',
    '5j37e',
    '6frz4',
    'iz3x1',
    '3caqi',
    'rau7s',
    'nt574',
    'nqut1',
    'm6shv',
    '9by7u',
    'e9vbd',
    'lbw39',
    '49mnc',
    'mzwx9',
    'jsh3w',
    'iwbsq',
    'iplbt',
    'baey2',
    'f291e',
    'dwai1',
    'p15ze',
    '1dsa5',
    'kl546',
    'rn2tx',
    'tl98q',
    'jdqa2',
    'x3k5q',
    'kqs4u',
    'kr1sp',
    'rahz7',
    'tbjim',
    'gq4v9',
    'xkf36',
    'hzbx5',
    '25zr8',
    'hg3ye',
    's48um',
    'kaywz',
    'ks63l',
    'tvqcs',
    'shmuv',
    'muf4i',
    '4qxbk',
    '3ck2n',
    '9fgkm',
    'inc31',
    'xmai1',
    's2hcn',
    'duwjy',
    'y47hv',
    '6x1w5',
    'w3tcf',
    'yahtb',
    'gip9w',
    '82mbc',
    'l2iey',
    '8i49s',
    'kuen1',
    '35pzl',
    'jergh',
]

for ident in idents:
    db.session.add(User(ident=ident))
db.session.commit()