from ..particle_list import *
from ..diagram import *
from ..feynman_rules import *

class QED_Vertex(Vertex):
    def __init__(self, name, diagram):
        super().__init__(name, diagram)
        self.max_number_of_particle = 3
        self.max_number_of_photon = 1
        self.max_number_of_electron = 2
        self.vertex_value = qed_vertex_value()
        
    def __repr__(self):
        return f'QED_Vertex({self.name})'
    
    def actualise_number(self):
        self.number_of_photon = sum(1 for i in range(len(self.particle_connected)) if isinstance(self.particle_connected[i], Photon))
        self.number_of_electron = sum(1 for i in range(len(self.particle_connected)) if (isinstance(self.particle_connected[i], Electron) 
                                        or isinstance(self.particle_connected[i], AntiElectron)))

    def check_validity(self):
        if self.number_of_particle > self.max_number_of_particle:
            raise Exception(f"There is too many particle connected to this vertex : {self.number_of_particle} instead of {self.max_number_of_particle} max.")
        if self.number_of_photon > self.max_number_of_photon:
            raise Exception(f"There is too many photons connected to this vertex : {self.number_of_photon} instead of {self.max_number_of_photon} max.")
        if self.number_of_electron > self.max_number_of_electron:
            raise Exception(f"There is too many electrons/positrons connected to this vertex : {self.number_of_electron} instead of {self.max_number_of_electron} max.")
        if self.total_charge_in != self.total_charge_out and self.number_of_particle == self.max_number_of_particle:
            raise Exception("Conservation of electrical charge is violated.")