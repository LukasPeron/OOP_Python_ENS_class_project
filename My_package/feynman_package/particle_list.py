class Particle(object):
    def __init__(self, name, momentum):
        self.name = name
        self.momentum = momentum
        if "+" in self.momentum or "-" in self.momentum:
            self.momentum = "(" + momentum + ")"
        self.propagator = False
        self.loop = False
        self.initial = False
        self.final = False
    
    def __repr__(self):
        return f'Particle({self.name}, {self.momentum})'

list_of_quarks = []
list_of_neutrino = []
def to_list_of_quarks(klass):
    list_of_quarks.append(klass)
    return klass
def to_list_of_neutrino(klass):
    list_of_neutrino.append(klass)
    return klass

class Antiparticle(Particle):
    pass

class Fermion(Particle):
    def __init__(self, name, momentum):
        super().__init__(name, momentum)
    particle_type = 'fermion'
    
    def __repr__(self):
        return f'Fermion({self.name}, {self.momentum})'

class Boson(Particle):
    def __init__(self, name, momentum):
        super().__init__(name, momentum)
    particle_type = 'boson'
    
    def __repr__(self):
        return f'Boson({self.name}, {self.momentum})'

class Lepton(Fermion):
    def __init__(self, name, momentum):
        super().__init__(name, momentum)

    def __repr__(self):
        return f'Lepton({self.name}, {self.momentum})'

class Neutrino(Particle):
    pass

class Electron(Lepton):
    charge = -1
    particle_label='e^-'
    
    def __repr__(self):
        return f'Electron({self.name}, {self.momentum})'

class AntiElectron(Lepton, Antiparticle):
    charge = 1
    particle_type = 'anti fermion'
    particle_label='e^+'
    
    def __repr__(self):
        return f'AntiElectron({self.name}, {self.momentum})'    

class Muon(Lepton):
    charge = -1
    particle_label='\mu^-'
    
    def __repr__(self):
        return f'Muon({self.name}, {self.momentum})'
    
class AntiMuon(Lepton, Antiparticle):
    charge = 1
    particle_type = 'anti fermion'
    particle_label='\mu^+'
    
    def __repr__(self):
        return f'AntiMuon({self.name}, {self.momentum})'

class Tau(Lepton):
    charge = -1
    particle_label='\\tau^-'
    
    def __repr__(self):
        return f'Tau({self.name}, {self.momentum})'

class AntiTau(Lepton, Antiparticle):
    charge = 1
    particle_type = 'anti fermion'
    particle_label='\\tau^+'
    
    def __repr__(self):
        return f'AntiTau({self.name}, {self.momentum})'
    
@to_list_of_neutrino
class NeutrinoElectron(Lepton, Neutrino):
    charge = 0
    particle_label='\\nu_e'
    
    def __repr__(self):
        return f'Neutrino_electron({self.name}, {self.momentum})'
    
@to_list_of_neutrino
class NeutrinoMuon(Lepton, Neutrino):
    charge = 0
    particle_label='\\nu_{\mu}'
    
    def __repr__(self):
        return f'Neutrino_muon({self.name}, {self.momentum})'
    
@to_list_of_neutrino
class NeutrinoTau(Lepton, Neutrino):
    charge = 0
    particle_label = '\\nu_{\\tau}'
    
    def __repr__(self):
        return f'Neutrino_tau({self.name}, {self.momentum})'

class Quark(Fermion):
    def __repr__(self):
        return f'Quark({self.name}, {self.momentum})'

@to_list_of_quarks
class Up(Quark):
    charge = 1/3
    particle_label='u'
    
    def __repr__(self):
        return f'Up({self.name}, {self.momentum})'
    
@to_list_of_quarks
class Down(Quark):
    charge = -2/3
    particle_label = 'd'
    
    def __repr__(self):
        return f'Down({self.name}, {self.momentum})'
    
@to_list_of_quarks
class Charm(Quark):
    charge = 1/3
    particle_label = 'c'
    
    def __repr__(self):
        return f'Charm({self.name}, {self.momentum})'
    
@to_list_of_quarks
class Strange(Quark):
    charge = -2/3
    particle_label = 's'
    
    def __repr__(self):
        return f'Strange({self.name}, {self.momentum})'
    
@to_list_of_quarks
class Top(Quark):
    charge = 1/3
    particle_label = 't'
    
    def __repr__(self):
        return f'Top({self.name}, {self.momentum})'
    
@to_list_of_quarks
class Bottom(Quark):
    charge = -2/3
    particle_label = 'b'
    
    def __repr__(self):
        return f'Bottom({self.name}, {self.momentum})'

class Photon(Boson):
    charge = 0
    particle_type = 'photon'
    particle_label = '\gamma'
    
    def __repr__(self):
        return f'Photon({self.name}, {self.momentum})'

class Gluon(Boson):
    charge = 0
    particle_type = 'gluon'
    particle_label = 'g'
    
    def __repr__(self):
        return f'Gluon({self.name}, {self.momentum})'

class Z0(Boson):
    charge = 0
    particle_label = 'Z'
    
    def __repr__(self):
        return f'Z0({self.name}, {self.momentum})'

class W_minus(Boson):
    charge = -1
    particle_label = 'W^-'
    
    def __repr__(self):
        return f'W_minus({self.name}, {self.momentum})'

class W_plus(Boson, Antiparticle):
    charge = 1
    particle_label = 'W^+'

class Higgs(Boson):
    charge = 0
    particle_label = 'H'
    
    def __repr__(self):
        return f'W_plus({self.name}, {self.momentum})'

for particle_klass in list_of_quarks:
    globals()[f'Anti{particle_klass.__name__}'] = type('Anti{particle_klass.__name__}', (particle_klass, Antiparticle), 
                                                       {'charge':-particle_klass.charge, 'particle_type':'anti '+particle_klass.particle_type,
                                                        'particle_label':'\\bar'+'{'+f'{particle_klass.particle_label}'+'}'})

for particle_klass in list_of_neutrino:
    globals()[f'Anti{particle_klass.__name__}'] = type('Anti{particle_klass.__name__}', (particle_klass, Neutrino, Antiparticle), 
                                                       {'charge':-particle_klass.charge, 'particle_type':'anti '+particle_klass.particle_type,
                                                        'particle_label':'\\bar'+'{'+f'{particle_klass.particle_label}'+'}'})