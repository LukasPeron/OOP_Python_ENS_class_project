from .particle_list import *

def qed_propagator(particle):
    momentum = particle.momentum
    if isinstance(particle, Fermion):
        return "\dfrac{i("+"\gamma^\mu {"+f"{momentum}"+"}_\mu + m)" + "}{" + f"{momentum}^2 - m^2 + i \epsilon"+"}"
    if isinstance(particle, Photon):
        return "\dfrac{-ig_{\mu\\nu}}"+"{" + f"{momentum}^2 + i\epsilon" + "}"

def qed_vertex_value():
    return " iQe\gamma^\mu "

def external_fermion(particle):
    momentum = particle.momentum
    if particle.initial:
        return f"u^s({momentum})"
    if particle.final:
        return "\\bar{u" + "}" + f"^s({momentum})"  

def external_antifermion(particle):
    momentum = particle.momentum
    if particle.final:
        return f"v^s({momentum})"
    if particle.initial:
        return "\\bar{v" + "}" + f"^s({momentum})"

def external_photon(particle):
    momentum = particle.momentum
    if particle.initial:
        return f"\epsilon_\mu({momentum})"
    if particle.final:
        return f"\epsilon_\mu^*({momentum})"
    
def external(particle):
    if isinstance(particle, Antiparticle):
        return external_antifermion(particle)
    if not isinstance(particle, Antiparticle) and isinstance(particle, Fermion):
        return external_fermion(particle)
    if isinstance(particle, Photon):
        return external_photon(particle)