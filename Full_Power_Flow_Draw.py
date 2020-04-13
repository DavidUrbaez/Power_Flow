def init_impedance(names, Zl):
    impedance = {
        names[0]: {'Z': Zl[0], 'V': 0, 'I': 0,
                   'Neighbors': None}}
    if len(names) > 1:
        for index, name in enumerate(names[1:]):
            impedance[name] = {'Z': Zl[index + 1], 'V': 0, 'I': 0,
                               'Neighbors': None}
    return impedance


def add_features(features, impedance):
    for feature, value in features.items():
        impedance[feature] = value
    return impedance


def add_impedance(Zs, name, prev, Zl, features={}):
    """
    This function adds the given integer arguments
    -> param Zs: Original Dict
    -> param name: name of the new line
    -> param prev: name of the prev line
    -> param Zl: line impedance
        -> param feature: optional for loads
            -->case S: features={'Type': 's', 'S': 15000 + 300j}
            -->case I: features={'Type': 'i', 'ic': 8, 'FP': 0.7}
            -->case Z: features={'Type': 'z', 'Zc': 1000 + 100j}
    """

    for z in Zs:
        if z == prev:
            if Zs[z]['Neighbors'] is not None:
                Zs[z]['Neighbors'][name] = add_features(features, {'Z': Zl, 'V': 0, 'I': 0, 'Neighbors': None})
            else:
                Zs[z]['Neighbors'] = {name: {'Z': Zl, 'V': 0, 'I': 0, 'Neighbors': None}}
                Zs[z]['Neighbors'][name] = add_features(features, Zs[z]['Neighbors'][name])
            break
        elif Zs[z]['Neighbors'] is not None:
            Zs[z]['Neighbors'] = add_impedance(Zs[z]['Neighbors'], name, prev, Zl, features)

    return Zs
