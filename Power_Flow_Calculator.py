import numpy as np
import cmath


def polar2rect(r, theta): return r * np.cos(theta) + r * np.sin(theta) * 1j


def angle(z): return np.arctan(z.imag / z.real)


Find_I = {'i': lambda i, v, fp: polar2rect(i, angle(v) - np.arccos(fp)),
          'z': lambda v, z: v / z,
          's': lambda s, vln: np.conj(s / (3 * vln))}


def DownStream(Zs, vf):
    for z in Zs:
        Zs[z]['V'] = vf - Zs[z]['I'] * Zs[z]['Z']
        if Zs[z]['Neighbors'] is not None:
            DownStream(Zs[z]['Neighbors'], Zs[z]['V'])


def UpStream(Zs):
    for z in Zs:
        if Zs[z]['Neighbors'] is not None:
            Zs[z]['I'], Zs[z]['V'], _ = UpStream(Zs[z]['Neighbors'])
        else:
            if Zs[z]['Type'] == 'i':
                Zs[z]['I'] = Find_I[Zs[z]['Type']](Zs[z]['ic'], Zs[z]['V'], Zs[z]['FP'])
            elif Zs[z]['Type'] == 'z':
                Zs[z]['I'] = Find_I[Zs[z]['Type']](Zs[z]['V'], Zs[z]['Zc'])
            elif Zs[z]['Type'] == 's':
                Zs[z]['I'] = Find_I[Zs[z]['Type']](Zs[z]['S'], Zs[z]['V'])
    I_, V = [], []

    for z in Zs:
        I_.append(Zs[z]['I'])
        V.append(Zs[z]['V'] + Zs[z]['I'] * Zs[z]['Z'])
        vff = Zs[z]['I'] * Zs[z]['Z'] + Zs[z]['V']
    return sum(I_), np.mean(V), vff


def run(vf, Zs, min_error=0.00001, max_iter=6):
    error, iter = 100, 0
    while error > min_error:
        DownStream(Zs, vf)
        _, _, vff = UpStream(Zs)
        error = abs(abs(vff) - abs(vf)) / abs(vf)
        iter += 1
        if iter > max_iter:
            print('Max Iter: ', max_iter)
            break


def Show_Full_Info(Zs, vf, St=[]):
    for z in Zs:
        Vdif = vf - Zs[z]['V']
        Perdidas = 3 * Vdif * np.conj(Zs[z]['I'])
        print('------------------------------------------')
        print("Para ", z, 'los parámetros son: ')
        print('Corriente: ', cmath.polar(Zs[z]['I']), '[A]')

        if Zs[z]['Neighbors'] is not None:
            print('Voltaje Carga: ', cmath.polar(Zs[z]['V']), '[V]')
            print('Voltaje Diferencial: ', cmath.polar(Vdif * np.sqrt(3)), '[V]')
            print('Pérdidas Activas: ', Perdidas.real / 1000, '[kW]')
            print('Pérdidas Reactivas: ', Perdidas.imag / 1000, '[KVAR]')
            Stotal = Show_Full_Info(Zs[z]['Neighbors'], Zs[z]['V'])
        else:
            print('Voltaje: ', cmath.polar(vf), '[V]')
            print('Potencia Carga: ', cmath.polar(np.conj(Zs[z]['I']) * Zs[z]['V']), '[VA]')


def Show_Full_Imp(Zs, f=60):
    for z in Zs:
        if Zs[z]['Neighbors'] is not None:
            Show_Full_Imp(Zs[z]['Neighbors'])
        else:
            print('------------------------------------------')
            print("En el punto de operación para ", z, 'los parámetros son: ')
            Z = Zs[z]['V'] / Zs[z]['I']
            w = 2 * np.pi * f
            print('Impedancia: ', Z, '[Ohm]')
            print('Resistencia: ', Z.real, '[Ohm]')
            print('Inductancia: ', (Z / w).imag * 1000, '[mH]')


def total_loss(Zs, vf, St=[]):
    for z in Zs:
        if Zs[z]['Neighbors'] is not None:
            Vdif = vf - Zs[z]['V']
            Perdidas = 3 * Vdif * np.conj(Zs[z]['I'])
            St.append(Perdidas)
            Stotal = total_loss(Zs[z]['Neighbors'], Zs[z]['V'], St)
    return St
