import Full_Power_Flow_Calculator as fpf_c
import Full_Power_Flow_Draw as fpf_d


# help(fpf_d.add_impedance) #If you need help

Zcarga = fpf_d.init_impedance(['ZL1'], [1 + 1j])  # Se crea el diccionario

Zcarga = fpf_d.add_impedance(Zcarga, name='Zc1', prev='ZL1', Zl=0, features={'Type': 's', 'S': 1000 + 80j})  # se conecta una carga a la linea 1

Zcarga = fpf_d.add_impedance(Zcarga, name='ZL2', prev='ZL1', Zl=1 + 1j)  # se conecta la linea 2 a la linea 1
Zcarga = fpf_d.add_impedance(Zcarga, name='Zc2', prev='ZL2', Zl=0, features={'Type': 's', 'S': 1500 + 300j})  # se conecta carga 2 a linea 2

Zcarga = fpf_d.add_impedance(Zcarga, name='ZL3', prev='ZL2', Zl=1 + 1j)
Zcarga = fpf_d.add_impedance(Zcarga, name='Zc3', prev='ZL3', Zl=0, features={'Type': 'i', 'ic': 5, 'FP': 0.8})

Zcarga = fpf_d.add_impedance(Zcarga, name='ZL4', prev='ZL2', Zl=1 + 1j)
Zcarga = fpf_d.add_impedance(Zcarga, name='Zc4', prev='ZL4', Zl=0, features={'Type': 'i', 'ic': 8, 'FP': 0.7})
Zcarga = fpf_d.add_impedance(Zcarga, name='ZL5', prev='ZL4', Zl=1 + 1j)

Zcarga = fpf_d.add_impedance(Zcarga, name='Zc5', prev='ZL5', Zl=0, features={'Type': 'z', 'Zc': 1000 + 100j})
Zcarga = fpf_d.add_impedance(Zcarga, name='ZL6', prev='ZL5', Zl=1 + 1j)
Zcarga = fpf_d.add_impedance(Zcarga, name='Zc6', prev='ZL6', Zl=0, features={'Type': 's', 'S': 15000 + 300j})

vs = 1000
fpf_c.run(Zs=Zcarga, vf=vs, min_error=.00000001)
fpf_c.Show_Full_Imp(Zs=Zcarga)
print('------------------------------------------')

fpf_c.Show_Full_Info(Zs=Zcarga, vf=vs)
Perdidas_Totales = fpf_c.total_loss(Zs=Zcarga, vf=vs)
print('------------------------------------------')
print('------------------------------------------')
print('Lás pérdidas totales son: ', sum(Perdidas_Totales).real / 1000, '[kW]')
