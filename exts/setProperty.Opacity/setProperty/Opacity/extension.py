import omni.ext
import omni.kit.selection
import omni.ui as ui
from omni.usd import Usd
from pxr import UsdGeom, Sdf

class SetpropertyOpacityExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[setProperty.Opacity] setProperty Opacity startup")

        self.path_usd = 'omniverse://localhost/Projects/ToLive.usd'

        self.selected = []
        self.materiais = []
        self.materiais_selecionados = []

        self._window = ui.Window("ExOpacity", width=300, height=300)
        self.slider_opacity = None
        self.label = None
        self.name_usd = ((self.path_usd.split('/')[-1]).split('.'))[0]

        with self._window.frame:
            with ui.VStack():                    
                self.label = ui.Label("Label")

                def onMousePressed(x, y, button, modifier):
                    for material in self.materiais_selecionados:
                        set_intensity_opacity(self.slider_opacity.model.get_value_as_float(), material)

                self.slider_opacity = ui.FloatSlider(min=0.000, max=1.000, value=0.000, mouse_moved_fn=onMousePressed)

                def encontrar_materiais(prim):
                    for subprim in prim.GetChildren():                        
                        if subprim.GetName() == "Looks":
                            for material in subprim.GetChildren():
                                parts = str(material.GetPath()).split('/')
                                if parts[1] == 'World':
                                    aux_mat = '/' + parts[1] + '/' + self.name_usd + '/' + '/'.join(parts[2:])
                                    self.materiais.append(aux_mat)       
                                else:
                                    self.materiais.append(material.GetPath())   

                def carregar_materiais_from_usd():
                    stage = Usd.Stage.Open(self.path_usd)
                    if not stage:
                        return

                    # Listar todos os caminhos dos primitivos no estágio
                    primitivos = stage.Traverse()

                    # Extrair diretórios de cada caminho de primitivo
                    self.materiais = []
                    for prim in primitivos:
                        encontrar_materiais(prim)
                    #self.label.text = str(self.materiais[0])
                    #/World/Projeto_Laion/DR_TUBULACAO_003/Geometry/DR_TUBULACAO_003_0/_6E81_148627
                    
                def carregar_obj_selecionados():
                    ctx = omni.usd.get_context()
                    self.selected = ctx.get_selection().get_selected_prim_paths()
                    #self.label.text = str(self.selected[0])
                    #/World/ToLive/Projeto_Laion/DR_TUBULACAO_003/Geometry/DR_TUBULACAO_003_0/_6E81_148627

                def carregar_materiais_selecionados():   
                    self.materiais_selecionados = []                 
                    for obj in self.selected:
                        dir_obj = '/'.join(str(obj).split('/')[:-1])
                        for material in self.materiais:
                            if dir_obj in material:
                                self.materiais_selecionados.append(material)
                                break    
                    #self.label.text = str(self.materiais_selecionados[0])               

                with ui.HStack():   
                    def set_intensity_opacity(intensity:float, path_material:str):
                        omni.kit.commands.execute('ChangeProperty',
                                prop_path=Sdf.Path(path_material + '/Shader.inputs:opacity_constant'),
                                value=intensity,
                                prev=1.0)

                    def set_opaco_translucido(translucido:bool, path_material:str):  
                        omni.kit.commands.execute('ChangeProperty',
                            prop_path=Sdf.Path(path_material + '/Shader.inputs:enable_opacity'),
                            value=translucido,
                            prev=None)

                    def on_opacity():
                        carregar_obj_selecionados()
                        carregar_materiais_selecionados()

                        for material in self.materiais_selecionados:
                            set_opaco_translucido(True, material)
                            set_intensity_opacity(self.slider_opacity.model.get_value_as_float(), material)
                        
                    def off_opacity():
                        carregar_obj_selecionados()
                        carregar_materiais_selecionados()

                        for material in self.materiais_selecionados:
                            set_opaco_translucido(False, material)
                            set_intensity_opacity(self.slider_opacity.model.get_value_as_float(), material)                     
                        

                    ui.Button("Opaco", clicked_fn=lambda: off_opacity())
                    ui.Button("Translúcido", clicked_fn=lambda: on_opacity())

                ui.Button("Carregar Materiais do USD", clicked_fn=lambda: carregar_materiais_from_usd())

    def on_shutdown(self): 
        print("[setProperty.Opacity] setProperty Opacity shutdown")