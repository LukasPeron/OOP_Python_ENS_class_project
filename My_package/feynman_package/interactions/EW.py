from ..particle_list import *
from ..diagram import *

class EW_ffZ_Vertex(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.max_number_of_particle = 3
        self.max_number_of_Z = 1
        self.max_number_of_fermion = 2
        
    def __repr__(self):
        return f'EW__ffZ_Vertex({self.name})'
    
    def actualise_number(self):
        self.number_of_Z = sum(1 for i in range(len(self.particle_connected)) if isinstance(self.particle_connected[i], Z0))
        self.number_of_fermion = sum(1 for i in range(len(self.particle_connected)) if (isinstance(self.particle_connected[i], Fermion) 
                                        or (isinstance(self.particle_connected[i], Fermion) and isinstance(self.particle_connected[i], Antiparticle))))

    def check_validity(self):
        if self.number_of_particle > self.max_number_of_particle:
            raise Exception(f"There is too many particle connected to this vertex : {self.number_of_particle} instead of {self.max_number_of_particle} max.")
        if self.number_of_Z > self.max_number_of_Z:
            raise Exception(f"There is too many Z boson connected to this vertex : {self.number_of_Z} instead of {self.max_number_of_Z} max.")
        if self.number_of_fermion > self.max_number_of_fermion:
            raise Exception(f"There is too many fermions/antifermions connected to this vertex : {self.number_of_fermion} instead of {self.max_number_of_fermion} max.")
        if self.total_charge_in != self.total_charge_out and self.number_of_particle == self.max_number_of_particle:
            raise Exception("Conservation of electrical charge is violated.")

class EW_nlW_Vertex(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.max_number_of_particle = 3
        self.max_number_of_W = 1
        self.max_number_of_neutrino = 1
        self.max_number_of_lepton = 1
        
    def __repr__(self):
        return f'EW__ffZ_Vertex({self.name})'
    
    def actualise_number(self):
        self.number_of_W = sum(1 for i in range(len(self.particle_connected)) if (isinstance(self.particle_connected[i], W_minus) 
                                        or isinstance(self.particle_connected[i], W_plus)))
        self.number_of_lepton = sum(1 for i in range(len(self.particle_connected)) if (not(isinstance(self.particle_connected[i], Neutrino))
                                        and (isinstance(self.particle_connected[i], Lepton) 
                                        or (isinstance(self.particle_connected[i], Lepton) and isinstance(self.particle_connected[i], Antiparticle)))))
        self.number_of_neutrino = sum(1 for i in range(len(self.particle_connected)) if (isinstance(self.particle_connected[i], Neutrino) 
                                        or isinstance(self.particle_connected[i], AntiNeutrinoElectron) 
                                        or isinstance(self.particle_connected[i], AntiNeutrinoMuon) 
                                        or isinstance(self.particle_connected[i], AntiNeutrinoTau)))
        
    def check_validity(self):
        if self.number_of_particle > self.max_number_of_particle:
            raise Exception(f"There is too many particle connected to this vertex : {self.number_of_particle} instead of {self.max_number_of_particle} max.")
        if self.number_of_W > self.max_number_of_W:
            raise Exception(f"There is too many W boson connected to this vertex : {self.number_of_W} instead of {self.max_number_of_W} max.")
        if self.number_of_neutrino > self.max_number_of_neutrino:
            raise Exception(f"There is too many neutrinos/antineutrinos connected to this vertex : {self.number_of_neutrino} instead of {self.max_number_of_neutrino} max.")
        if self.number_of_lepton > self.max_number_of_lepton:
            raise Exception(f"There is too many leptons connected to this vertex : {self.number_of_lepton} instead of {self.max_number_of_lepton} max.")
        if self.total_charge_in != self.total_charge_out and self.number_of_particle == self.max_number_of_particle:
            raise Exception("Conservation of electrical charge is violated.")