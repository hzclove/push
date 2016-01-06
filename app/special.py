def select_users():
    home = os.path.abspath('.')
    cids = {'getui':[], 'xiaomi':[], 'umeng_iOS':[], 'umeng_android':[]}
    with open(home+'/getui') as f:
        for l in f:
            l = l.strip()
            cids['getui'].append(l)
    with open(home+'/xiaomi') as f:
        for l in f:
            l = l.strip()
            cids['xiaomi'].append(l)
    with open(home+'/umeng') as f:
        for l in f:
            l = l.strip()
            cids['umeng_android'].append(l)
    return cids
