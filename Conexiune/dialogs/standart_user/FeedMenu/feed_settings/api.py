async def fill_front(fs):
    front = {}
    if fs.sex:
        front['sex'] = fs.sex
    if fs.min_age:
        front['min_age'] = fs.min_age
    if fs.max_age:
        front['max_age'] = fs.max_age
    if fs.location:
        front['location'] = fs.location
    return front


async def handle_back(fs, back):
    if 'u_id' not in back:
        back['u_id'] = fs.user_fk

    if fs.sex:
        back['sex'] = fs.sex
    elif 'sex' in back:
        del back['sex']
    if fs.min_age:
        back['min_age'] = fs.min_age
    elif 'min_age' in back:
        del back['min_age']
    if fs.max_age:
        back['max_age'] = fs.max_age
    elif 'max_age' in back:
        del back['max_age']
    if fs.location:
        back['location'] = fs.location
    elif 'location' in back:
        del back['location']
