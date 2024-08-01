from .feynman_rules import *
from .particle_list import *
from IPython.display import display, Math, Image
from pylatex import Document, Command
from pylatex.utils import NoEscape
from pdf2image import convert_from_path
import os

def suppr_doublon(lst1, lst2):
    return list(dict.fromkeys(lst1)), list(dict.fromkeys(lst2))

def loop_sorting(lst):
        if isinstance(lst[0], Antiparticle):
            return lst
        else:
            return [lst[1], lst[0]]

class Diagram(object):
    def __init__(self, channel):
        self.channel = channel
        self.index_final = 0
        self.index_initial = 0
    
    def __repr__(self, *args):
        return f'Diagram({self.args})'
    
    def add_vertex(self, *args):
        self.vertice_list = list(args)
        for i in range (len(self.vertice_list)):
            if self.channel == "t" or self.channel=="u":
                if self.vertice_list[i].particle_in != []:
                    self.index_initial = i
                if self.vertice_list[i].particle_out != []:
                    self.index_final = i
            else:
                self.index_initial = 0
                self.index_final = -1
    
    def display(self, pref_user, save_files=False, show_code=False, show_image=True):
        code = "\\feynmandiagram"+f"[{pref_user}]"+"{\n"
        particle_line = []
        internal_line = []
        for vertex in self.vertice_list:
            counter_loop = 0
            for part in vertex.particle_in:
                particle_line.append(f"{part.name}[particle = \({part.particle_label}\)] -- [{part.particle_type}, momentum'=\({part.momentum}\)] {vertex.name}," + "\n")
            for part in vertex.particle_out:
                particle_line.append(f"{vertex.name} -- [{part.particle_type}, momentum'=\({part.momentum}\)] {part.name}[particle = \({part.particle_label}\)]," + "\n")
            for intern in vertex.propagator_in:
                lst_intern_in = vertex.propagator_in
                i = lst_intern_in.index(intern)
                if intern.loop:
                    if counter_loop%2==0:
                        internal_line.append(f"{vertex.vertex_in[i].name} -- [{intern.particle_type}, half left, edge label = \({intern.particle_label}\), momentum'=\({intern.momentum}\)] {vertex.name}," + "\n")
                        counter_loop+=1
                    else:
                        internal_line.append(f"{vertex.vertex_in[i].name} -- [{intern.particle_type}, half right, edge label = \({intern.particle_label}\), momentum'=\({intern.momentum}\)] {vertex.name}," + "\n")
                        counter_loop+=1
                else:
                    internal_line.append(f"{vertex.vertex_in[i].name} -- [{intern.particle_type}, edge label = \({intern.particle_label}\), momentum'=\({intern.momentum}\)] {vertex.name}," + "\n")
            for intern in vertex.propagator_out:
                lst_intern_out = vertex.propagator_out
                i = lst_intern_out.index(intern)
                if intern.loop:
                    if counter_loop%2==0:
                        internal_line.append(f"{vertex.name} -- [{intern.particle_type}, half left, edge label = \({intern.particle_label}\), momentum'=\({intern.momentum}\)] {vertex.vertex_out[i].name}," + "\n")
                        counter_loop+=1
                    else:
                        internal_line.append(f"{vertex.name} -- [{intern.particle_type}, half right, edge label = \({intern.particle_label}\), momentum'=\({intern.momentum}\)] {vertex.vertex_out[i].name}," + "\n")
                        counter_loop+=1
                else:
                    internal_line.append(f"{vertex.name} -- [{intern.particle_type}, edge label = \({intern.particle_label}\), momentum'=\({intern.momentum}\)] {vertex.vertex_out[i].name}," + "\n")
        particle_line, internal_line = suppr_doublon(particle_line, internal_line)
        for i in range(len(particle_line)):
            code += particle_line[i]
        for i in range(len(internal_line)):
            code += internal_line[i]
        code += "};"
        if show_code:
            print(code)
        if show_image:
            doc = Document("my_diagram")
            doc.documentclass = Command('documentclass', options=['preview'], arguments=['standalone'],)
            doc.preamble.append(NoEscape(r"\usepackage[compat=1.0.0]{tikz-feynman}"))
            doc.preamble.append(NoEscape(r"\usepackage{slashed}"))
            doc.append(NoEscape(code))
            doc.generate_tex()
            os.system("lualatex my_diagram.tex")
            image = convert_from_path('my_diagram.pdf', 500)
            image[0].save('my_diagram.png', 'PNG')
            display(Image(filename='my_diagram.png', width=400, height=150))
        if not save_files:
            for extension in ["tex", "pdf", "png", "log", "aux"]:
                os.remove("my_diagram."+extension)
    
    def external_code_tu_channel(self, vertex, in_out, i, particle_counted, vertex_counted):
        code = ""
        if in_out=="in":
            particle=vertex.particle_in
        else:
            particle=vertex.particle_out
        code += external(particle[i%2])
        particle_counted.append(particle[i%2])
        code += vertex.vertex_value
        i+=1
        code += external(particle[i%2])
        particle_counted.append(particle[i%2])
        vertex_counted.append(vertex)
        return code, particle_counted, vertex_counted

    def external_code_s_channel(self, vertex, particle_counted, vertex_counted):
        temp_code = ""
        if isinstance(vertex.particle_in[0], Antiparticle):
            temp_code, particle_counted, vertex_counted = self.external_code_s_channel_anti(self, vertex, particle_counted, vertex_counted)
        else:
            if isinstance(vertex.particle_out[0], Antiparticle):
                temp_code, particle_counted, vertex_counted = self.external_code_s_channel_anti(vertex, particle_counted, vertex_counted)
            else:
                temp_code, particle_counted, vertex_counted = self.external_code_s_channel_ordinary(vertex, particle_counted, vertex_counted)
        return temp_code, particle_counted, vertex_counted

    def external_code_s_channel_anti(self, vertex, particle_counted, vertex_counted):
        temp_code = ""
        temp_code += external(vertex.particle_in[0])
        particle_counted.append(vertex.particle_in[0])
        temp_code += vertex.vertex_value
        temp_code += external(vertex.particle_out[0])
        particle_counted.append(vertex.particle_out[0])
        vertex_counted.append(vertex)
        return temp_code, particle_counted, vertex_counted
    
    def external_code_s_channel_ordinary(self, vertex, particle_counted, vertex_counted):
        temp_code = ""
        temp_code += external(vertex.particle_out[0])
        particle_counted.append(vertex.particle_out[0])
        temp_code += vertex.vertex_value
        temp_code += external(vertex.particle_in[0])
        particle_counted.append(vertex.particle_in[0])
        vertex_counted.append(vertex)
        return temp_code, particle_counted, vertex_counted
    
    def integral_initial_code_tu_channel(self, initial_code, vertex, particle_counted, vertex_counted):
        if len(vertex.particle_in) == 2:
            if isinstance(vertex.particle_in[0], Antiparticle):
                temp_code, particle_counted, vertex_counted = self.external_code_tu_channel(vertex, "in", 0, particle_counted, vertex_counted)
                initial_code += temp_code
            else:
                if not isinstance(vertex.particle_in[1], Antiparticle) and isinstance(vertex.particle_in[1], Fermion):
                    temp_code, particle_counted, vertex_counted = self.external_code_tu_channel(vertex, "in", 0, particle_counted, vertex_counted)
                    initial_code += temp_code
                else:
                    temp_code, particle_counted, vertex_counted = self.external_code_tu_channel(vertex, "in", 1, particle_counted, vertex_counted)
                    initial_code += temp_code
        else:
            initial_code += external(vertex.particle_in[0])
            particle_counted.append(vertex.particle_in[0])
            initial_code += vertex.vertex_value
            vertex_counted.append(vertex)
        return initial_code, particle_counted, vertex_counted
    
    def integral_initial_code_s_channel(self, initial_code, vertex, particle_counted, vertex_counted):
        temp_code, particle_counted, vertex_counted = self.external_code_s_channel(vertex, particle_counted, vertex_counted)
        initial_code += temp_code
        return initial_code, particle_counted, vertex_counted
    
    def integral_final_code_tu_channel(self, final_code, vertex, particle_counted, vertex_counted):
        if len(vertex.particle_out) == 2:
            if not isinstance(vertex.particle_out[0], Antiparticle) and isinstance(vertex.particle_out[0], Fermion):
                temp_code, particle_counted, vertex_counted = self.external_code_tu_channel(vertex, "out", 0, particle_counted, vertex_counted)
                final_code += temp_code
            else:
                if isinstance(vertex.particle_out[1], Antiparticle):
                    temp_code, particle_counted, vertex_counted = self.external_code_tu_channel(vertex, "out", 0, particle_counted, vertex_counted)
                    final_code += temp_code
                else:
                    temp_code, particle_counted, vertex_counted = self.external_code_tu_channel(vertex, "out", 1, particle_counted, vertex_counted)
                    final_code += temp_code
        else:
            final_code += external(vertex.particle_out[0])
            particle_counted.append(vertex.particle_out[0])
            final_code += vertex.vertex_value
            vertex_counted.append(vertex)
        return final_code, particle_counted, vertex_counted

    def integral_final_code_s_channel(self, final_code, vertex, particle_counted, vertex_counted):
        temp_code, particle_counted, vertex_counted = self.external_code_s_channel(vertex, particle_counted, vertex_counted)
        final_code += temp_code
        return final_code, particle_counted, vertex_counted
    
    def integral_initial_code(self, particle_counted, vertex_counted):
        initial_code = ''
        vertex_initial = self.vertice_list[self.index_initial]
        for vertex in self.vertice_list:
            if vertex == vertex_initial:
                if not vertex.channel=="s":
                    initial_code, particle_counted, vertex_counted = self.integral_initial_code_tu_channel(initial_code, vertex, particle_counted, vertex_counted)
                else:
                    initial_code, particle_counted, vertex_counted = self.integral_initial_code_s_channel(initial_code, vertex, particle_counted, vertex_counted)
        return initial_code, particle_counted, vertex_counted

    def integral_inter_code(self, particle_counted, vertex_counted):
        inter_code = ''
        for vertex in self.vertice_list:
            for particle in vertex.propagator_out:
                if particle not in particle_counted:
                    inter_code += qed_propagator(particle)
                    particle_counted.append(particle)
                    if vertex.vertex_out[vertex.propagator_out.index(particle)] not in vertex_counted:
                        vertex_counted.append(vertex.vertex_out[vertex.propagator_out.index(particle)])
                        inter_code += vertex.vertex_value
        return inter_code, particle_counted, vertex_counted

    def integral_final_code(self, particle_counted, vertex_counted):
        final_code = ''
        vertex_final = self.vertice_list[self.index_final]
        for vertex in self.vertice_list:
            if vertex == vertex_final:
                if not vertex.channel=="s":
                    final_code, particle_counted, vertex_counted = self.integral_final_code_tu_channel(final_code, vertex, particle_counted, vertex_counted)
                else:
                    final_code, particle_counted, vertex_counted = self.integral_final_code_s_channel(final_code, vertex, particle_counted, vertex_counted)
        return final_code
    
    def integral(self, show_code=False):
        entete = "\int \dfrac{\mathrm{"+"d}^4 p}{(2\pi)^4}"
        particle_counted = []
        vertex_counted = []
        initial_code, particle_counted, vertex_counted = self.integral_initial_code(particle_counted, vertex_counted)
        final_code = self.integral_final_code(particle_counted, vertex_counted)
        inter_code, particle_counted, vertex_counted = self.integral_inter_code(particle_counted, vertex_counted)
        full_code = entete + initial_code + "\left[" + inter_code + "\\right]" + final_code
        if show_code:
            print(full_code)
        return Math(full_code)

class Vertex(object):
    def __init__(self, name, diagram):
        self.name = name
        self.particle_in = []
        self.particle_out = []
        self.propagator_in = []
        self.propagator_out = []
        self.vertex_in = []
        self.vertex_out = []
        self.channel = diagram.channel
        
    def __repr__(self):
        return f'QED_Vertex({self.name})'
    
    def large_actualise_number(self):
        self.particle_connected = self.particle_in + self.particle_out
        self.propagator_connected = self.propagator_in + self.propagator_out
        self.vertex_connected = self.vertex_in + self.vertex_out
        self.number_of_particle = len(self.particle_connected) + len(self.propagator_connected)
        self.total_charge_in = sum(particle.charge for particle in self.particle_in) + sum(propag.charge for propag in self.propagator_in) 
        self.total_charge_out = sum(particle.charge for particle in self.particle_out) + sum(propag.charge for propag in self.propagator_out)
    
    def verify(self):
        self.actualise_number()
        self.check_validity()    
    
    def connect_particle_in(self, *particles):
        part_list = list(particles)
        for part in part_list:
            part.initial = True
            self.particle_in.append(part)
            self.large_actualise_number()
            self.verify()

    def connect_particle_out(self, *particles):
        part_list = list(particles)
        for part in part_list:
            part.final = True
            self.particle_out.append(part)
            self.large_actualise_number()
            self.verify()

    def connect_vertex_in(self, vertex, propagator):
        propagator.propagator = True
        self.vertex_in.append(vertex)
        self.propagator_in.append(propagator)
        self.large_actualise_number()
        self.verify()

    def connect_vertex_out(self, vertex, propagator):
        propagator.propagator = True
        self.vertex_out.append(vertex)
        self.propagator_out.append(propagator)
        self.large_actualise_number()
        self.verify()
        vertex.connect_vertex_in(self, propagator)
    
    def connect_loop_in(self, vertex, *propagators):
        propag_list = loop_sorting(list(propagators))
        for propag in propag_list :
            propag.loop = True
            self.vertex_in.append(vertex)
            self.propagator_in.append(propag)
            self.large_actualise_number()
            self.verify()
    
    def connect_loop_out(self, vertex, *propagators):
        propag_list = loop_sorting(list(propagators))
        for propag in propag_list :
            propag.loop = True
            self.vertex_out.append(vertex)
            self.propagator_out.append(propag)
            self.verify()
        vertex.connect_loop_in(self, *propagators)