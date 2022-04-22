import numpy as np
import matplotlib.pyplot as plt
import tp_exoplanete
import glob

### Partie I

# a)

tp_exoplanete.plot_spectrum("1d/417430_s1d.fits")

# b)

tp_exoplanete.plot_spectrum("1d/416770_s1d.fits","G2.mas")


"""
Cela nous permet de determiner un décalage en longueur d'onde entre les deux rayonnements dû à la vitesse radiale de l'étoile observée.
"""

# i)

"""
Les traits rouges correspondent aux longueur d'onde d'émission pour une étoile sans vitesse radiale.
"""

# ii)

"""
Cela correspond à l'absorption de l'atmosphère
"""

# iii)

"""
La largeur des raies est liée au pouvoir de résolution
"""

# iv)

"""
On observe un delta lambda de 3997.1002 - 3997.0652 = 0.035 Angstrom dans le bleu, 
et un delta lambda de 6929.333 - 6929.232 = 0.101 Angstrom dans le rouge
"""

# v)

"""
Il y a un nombre fini de mesures et observations. De ce fait, la longueur d'onde et l
'intensité de chaque spectre est discretisée et correspond donc à un point précis. 
Matplotlib relie chacun de ces points entre eux par un segment
"""

# vi)

"""
La longueur d'onde du premier pic observé à la question v) est 3997.0826, 
ce qui nous donne un pouvoir de résolution de 3997.0826/0.035=114202.36

La longueur d'onde du deuxieme pic observé à la question v) est 6929.284, 
ce qui nous donne un pouvoir de résolution de 6929.284/0.101=68606.77

La résolution varie donc bien selon la zone du spectre observée
"""

# vii)

"""
Page 280 de la publication Osterbrock et al., 1996, PASP, 108, on trouve une longueur d'onde de [OI] de 5577.338

Les spécialistes de l'usage des spectromètres font habituellement référence au spectre résultant d'un état
d'ionisation donné d'un élément chimique par le symbole de l'élément suivi par un nombre romain. Le nombre 
I est utilisé pour faire référence à l'élément neutre (non ionisé), II à l'élément ionisé une fois, III à 
l'élément ionisé deux fois etc...

L'élément [0I] correspond donc à l'oxygène neutre.
"""

# viii)

"""
Sur le spectre on observe un pic en absorption (car c'est un pic vers le bas) vers 6562.761 Angstrom

"L’énergie nécessaire pour ioniser l’hydrogène étant quasiment la même que celle nécessaire pour faire 
passer un électron du niveau n = 1 au niveau n = 3, la probabilité qu’un électron ne soit pas éjecté de 
l’atome mais passe vers ce niveau n = 3 est très faible. Par contre, après avoir été ionisé, l’électron 
et le proton vont se recombiner pour former un nouvel atome d’hydrogène. Dans ce nouvel atome, l’électron 
peut se trouver sur n’importe lequel des niveaux d’énergie, et ensuite, va cascader vers le niveau fondamental
(n = 1), en émettant un photon lors de chaque transition. On a calculé qu’environ une fois sur deux, cette 
cascade comprend la transition n = 3 vers n = 2, et l’atome va alors émettre la raie H-alpha. Cette raie est 
donc émise juste après que l’atome ionisé a récupéré un électron et cesse d'être ionisé." Source Wikipédia
"""


### Partie II

Vr_jour1 = [2.03E+03,6.76E+03,8.70E+03]
Vr_jour2 = [6.95E+03,1.22E+04,1.26E+04]

Vr = [Vr_jour1, Vr_jour2]
 
jour1 = [tp_exoplanete.read_date("1d/417430_s1d.fits")]
jour2 = [tp_exoplanete.read_date("1d/416770_s1d.fits")]

date = [jour1, jour2]

plt.plot(date,Vr, '.')
plt.xlabel('Date')
plt.ylabel('Vitesse Radiale')
plt.grid()
plt.show()


### Partie III

tp_exoplanete.compute_ccf("1d/417430_s1d.fits","G2.mas")
tp_exoplanete.compute_ccf("1d/416770_s1d.fits","G2.mas")

tp_exoplanete.plot_ccf("1d/417430_ccf.dat")
plt.title("spectre 1")
plt.show()

tp_exoplanete.plot_ccf("1d/416770_ccf.dat")
plt.title("spectre 2")
plt.show()

Vr2_jour1 = -2.47
Vr2_jour2 = -2.03 

Vr2 = [Vr2_jour1, Vr2_jour2]

plt.plot(date,Vr, '.')
plt.plot(date,Vr2, '+')
plt.title("graph avec les nouvelles vitesse radial")
plt.show()


# Partie IV

c, a, v, s = tp_exoplanete.fit_gaussian("1d/417430_ccf.dat",show=True)
c, a, v, s = tp_exoplanete.fit_gaussian("1d/416770_ccf.dat",show=True)

Vr3_jour1 = -2.442
Vr3_jour2 = -2.055


Vr3 = [Vr3_jour1, Vr3_jour2]
plt.plot(date,Vr,'.')
plt.plot(date,Vr2,'+')
plt.plot(date,Vr3,'x')
plt.show()


### Partie V

i=0
l = len(glob.glob('1d/*.fits'))
date = np.zeros(l)
vr = np.zeros(l)
for filename in  glob.iglob('1d/*.fits', recursive = True):
    date[i] = tp_exoplanete.read_date(filename)
    print(date[i])
    tp_exoplanete.compute_ccf(filename,"G2.mas")
    ccf_dat = filename[:-9] + '_ccf.dat'
    c,a,v,s = tp_exoplanete.fit_gaussian(ccf_dat)
    vr[i] = v
    i+=1
   
np.sort(date)
np.sort(vr)

plt.plot(date, vr, '.')
plt.show()

# Partie VI

