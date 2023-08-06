from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from lollms.personality import AIPersonality, MSG_TYPE
from lollms.binding import LOLLMSConfig, LLMBinding
from lollms.helpers import ASCIIColors
from lollms.console import MainMenu
from lollms.paths import LollmsPaths
from lollms.console import MainMenu
from lollms import BindingBuilder, ModelBuilder, PersonalityBuilder
from lollms import reset_all_installs
from typing import List, Tuple
import importlib
from pathlib import Path
import argparse
import logging
import shutil
import yaml
import copy

class LoLLMsServer:
    def __init__(self):
        self.app = Flask("LoLLMsServer_Server")
        #self.app.config['SECRET_KEY'] = 'lollmssecret'
        CORS(self.app)  # Enable CORS for all routes
        self.socketio = SocketIO(self.app, cors_allowed_origins='*')
        self.clients = {}
        self.current_binding = None
        self.current_model = None
        self.personalities = []
        self.answer = ['']



        self.lollms_paths = LollmsPaths.find_paths(force_local=False)
        self.menu = MainMenu(self)

        # Set log level to warning
        self.app.logger.setLevel(logging.WARNING)
        # Configure a custom logger for Flask-SocketIO
        self.socketio_log = logging.getLogger('socketio')
        self.socketio_log.setLevel(logging.WARNING)
        self.socketio_log.addHandler(logging.StreamHandler())

        self.initialize_routes()
        self.run()


    def load_binding(self):
        if self.config.binding_name is None:
            print(f"No bounding selected")
            print("Please select a valid model or install a new one from a url")
            self.menu.select_binding()
            # cfg.download_model(url)
        else:
            try:
                self.binding_class = BindingBuilder().build_binding(self.lollms_paths.bindings_zoo_path, self.config)
            except Exception as ex:
                print(ex)
                print(f"Couldn't find binding. Please verify your configuration file at {self.config.file_path} or use the next menu to select a valid binding")
                self.menu.select_binding()

    def load_model(self):
        try:
            self.model = ModelBuilder(self.binding_class, self.config).get_model()
        except Exception as ex:
            ASCIIColors.error(f"Couldn't load model.")
            ASCIIColors.error(f"Binding returned this exception : {ex}")
            ASCIIColors.error(f"{self.config.get_model_path_infos()}")
            print("Please select a valid model or install a new one from a url")
            self.menu.select_model()

    def load_personality(self):
        try:
            self.personality = PersonalityBuilder(self.lollms_paths, self.config, self.model).build_personality()
        except Exception as ex:
            ASCIIColors.error(f"Couldn't load personality.")
            ASCIIColors.error(f"Binding returned this exception : {ex}")
            ASCIIColors.error(f"{self.config.get_personality_path_infos()}")
            print("Please select a valid model or install a new one from a url")
            self.menu.select_model()
        self.cond_tk = self.personality.model.tokenize(self.personality.personality_conditioning)
        self.n_cond_tk = len(self.cond_tk)

    def initialize_routes(self):
        @self.socketio.on('connect')
        def handle_connect():
            client_id = request.sid
            self.clients[client_id] = {"namespace": request.namespace, "full_discussion_blocks": []}
            ASCIIColors.success(f'Client connected with session ID: {client_id}')

        @self.socketio.on('disconnect')
        def handle_disconnect():
            client_id = request.sid
            if client_id in self.clients:
                del self.clients[client_id]
            print(f'Client disconnected with session ID: {client_id}')


        @self.socketio.on('list_available_bindings')
        def handle_list_bindings():
            binding_infs = []
            for p in self.bindings_path.iterdir():
                if p.is_dir():
                    with open(p/"binding_card.yaml", "r") as f:
                        card = yaml.safe_load(f)
                    with open(p/"models.yaml", "r") as f:
                        models = yaml.safe_load(f)
                    entry={
                        "name":p.name,
                        "card":card,
                        "models":models
                    }
                    binding_infs.append(entry)

            emit('bindings_list', {'success':True, 'bindings': binding_infs}, room=request.sid)

        @self.socketio.on('list_available_personalities')
        def handle_list_available_personalities():
            personalities_folder = self.personalities_path
            personalities = {}
            for language_folder in personalities_folder.iterdir():
                if language_folder.is_dir():
                    personalities[language_folder.name] = {}
                    for category_folder in  language_folder.iterdir():
                        if category_folder.is_dir():
                            personalities[language_folder.name][category_folder.name] = []
                            for personality_folder in category_folder.iterdir():
                                if personality_folder.is_dir():
                                    try:
                                        personality_info = {"folder":personality_folder.stem}
                                        config_path = personality_folder / 'config.yaml'
                                        with open(config_path) as config_file:
                                            config_data = yaml.load(config_file, Loader=yaml.FullLoader)
                                            personality_info['name'] = config_data.get('name',"No Name")
                                            personality_info['description'] = config_data.get('personality_description',"")
                                            personality_info['author'] = config_data.get('author', 'ParisNeo')
                                            personality_info['version'] = config_data.get('version', '1.0.0')
                                        scripts_path = personality_folder / 'scripts'
                                        personality_info['has_scripts'] = scripts_path.is_dir()
                                        assets_path = personality_folder / 'assets'
                                        gif_logo_path = assets_path / 'logo.gif'
                                        webp_logo_path = assets_path / 'logo.webp'
                                        png_logo_path = assets_path / 'logo.png'
                                        jpg_logo_path = assets_path / 'logo.jpg'
                                        jpeg_logo_path = assets_path / 'logo.jpeg'
                                        bmp_logo_path = assets_path / 'logo.bmp'
                                        
                                        personality_info['has_logo'] = png_logo_path.is_file() or gif_logo_path.is_file()
                                        
                                        if gif_logo_path.exists():
                                            personality_info['avatar'] = str(gif_logo_path).replace("\\","/")
                                        elif webp_logo_path.exists():
                                            personality_info['avatar'] = str(webp_logo_path).replace("\\","/")
                                        elif png_logo_path.exists():
                                            personality_info['avatar'] = str(png_logo_path).replace("\\","/")
                                        elif jpg_logo_path.exists():
                                            personality_info['avatar'] = str(jpg_logo_path).replace("\\","/")
                                        elif jpeg_logo_path.exists():
                                            personality_info['avatar'] = str(jpeg_logo_path).replace("\\","/")
                                        elif bmp_logo_path.exists():
                                            personality_info['avatar'] = str(bmp_logo_path).replace("\\","/")
                                        else:
                                            personality_info['avatar'] = ""
                                        personalities[language_folder.name][category_folder.name].append(personality_info)
                                    except Exception as ex:
                                        print(f"Couldn't load personality from {personality_folder} [{ex}]")
            emit('personalities_list', {'personalities': personalities}, room=request.sid)

        @self.socketio.on('list_available_models')
        def handle_list_available_models():
            """List the available models

            Returns:
                _type_: _description_
            """
            if self.binding_class is None:
               emit('available_models_list', {'success':False, 'error': "No binding selected"}, room=request.sid)
            model_list = self.binding_class.get_available_models()

            models = []
            for model in model_list:
                try:
                    filename = model.get('filename',"")
                    server = model.get('server',"")
                    image_url = model.get("icon", '/images/default_model.png')
                    license = model.get("license", 'unknown')
                    owner = model.get("owner", 'unknown')
                    owner_link = model.get("owner_link", 'https://github.com/ParisNeo')
                    filesize = int(model.get('filesize',0))
                    description = model.get('description',"")
                    model_type = model.get("model_type","")
                    if server.endswith("/"):
                        path = f'{server}{filename}'
                    else:
                        path = f'{server}/{filename}'
                    local_path = self.models_path/f'{self.config["binding_name"]}/{filename}'
                    is_installed = local_path.exists() or model_type.lower()=="api"
                    models.append({
                        'title': filename,
                        'icon': image_url,  # Replace with the path to the model icon
                        'license': license,
                        'owner': owner,
                        'owner_link': owner_link,
                        'description': description,
                        'isInstalled': is_installed,
                        'path': path,
                        'filesize': filesize,
                        'model_type': model_type
                    })
                except Exception as ex:
                    print("#################################")
                    print(ex)
                    print("#################################")
                    print(f"Problem with model : {model}")
            emit('available_models_list', {'success':True, 'available_models': models}, room=request.sid)

        @self.socketio.on('list_available_personalities_languages')
        def handle_list_available_personalities_languages():
            try:
                languages = [l for l in self.personalities_path.iterdir()]
                emit('available_personalities_languages_list', {'success': True, 'available_personalities_languages': languages})
            except Exception as ex:
                emit('available_personalities_languages_list', {'success': False, 'error':str(ex)})

        @self.socketio.on('list_available_personalities_categories')
        def handle_list_available_personalities_categories(data):
            try:
                language = data["language"]
                categories = [l for l in (self.personalities_path/language).iterdir()]
                emit('available_personalities_categories_list', {'success': True, 'available_personalities_categories': categories})
            except Exception as ex:
                emit('available_personalities_categories_list', {'success': False, 'error':str(ex)})

        @self.socketio.on('list_available_personalities_names')
        def handle_list_available_personalities_names(data):
            try:
                language = data["language"]
                category = data["category"]
                personalities = [l for l in (self.personalities_path/language/category).iterdir()]
                emit('list_available_personalities_names_list', {'success': True, 'list_available_personalities_names': personalities})
            except Exception as ex:
                emit('list_available_personalities_names_list', {'success': False, 'error':str(ex)})

        @self.socketio.on('select_binding')
        def handle_select_binding(data):
            self.cp_config = copy.deepcopy(self.config)
            self.cp_config["binding_name"] = data['binding_name']
            try:
                self.binding_class = self.build_binding(self.bindings_path, self.cp_config)
                self.config = self.cp_config
                emit('select_binding', {'success':True, 'binding_name': self.cp_config["binding_name"]}, room=request.sid)
            except Exception as ex:
                print(ex)
                emit('select_binding', {'success':False, 'binding_name': self.cp_config["binding_name"], 'error':f"Couldn't load binding:\n{ex}"}, room=request.sid)

        @self.socketio.on('select_model')
        def handle_select_model(data):
            model_name = data['model_name']
            if self.binding_class is None:
                emit('select_model', {'success':False, 'model_name':  model_name, 'error':f"Please select a binding first"}, room=request.sid)
                return
            self.cp_config = copy.deepcopy(self.config)
            self.cp_config["model_name"] = data['model_name']
            try:
                self.current_model = self.binding_class(self.cp_config)
                emit('select_model', {'success':True, 'model_name':  model_name}, room=request.sid)
            except Exception as ex:
                print(ex)
                emit('select_model', {'success':False, 'model_name':  model_name, 'error':f"Please select a binding first"}, room=request.sid)

        @self.socketio.on('add_personality')
        def handle_add_personality(data):
            personality_path = data['path']
            try:
                personality = AIPersonality(self.lollms_paths, personality_path)
                self.personalities.append(personality)
                self.config["personalities"].append(personality_path)
                emit('personality_added', {'success':True, 'name': personality.name, 'id':len(self.personalities)-1}, room=request.sid)
                self.config.save_config()
            except Exception as e:
                error_message = str(e)
                emit('personality_add_failed', {'success':False, 'error': error_message}, room=request.sid)


        @self.socketio.on('list_active_personalities')
        def handle_list_active_personalities():
            personality_names = [p.name for p in self.personalities]
            emit('active_personalities_list', {'success':True, 'personalities': personality_names}, room=request.sid)

        @self.socketio.on('activate_personality')
        def handle_activate_personality(data):
            personality_id = data['id']
            if personality_id<len(self.personalities):
                self.active_personality=self.personalities[personality_id]
                emit('activate_personality', {'success':True, 'name': self.active_personality, 'id':len(self.personalities)-1}, room=request.sid)
                self.config["active_personality_id"]=personality_id
                self.config.save_config()
            else:
                emit('personality_add_failed', {'success':False, 'error': "Personality ID not valid"}, room=request.sid)

        @self.socketio.on('generate_text')
        def handle_generate_text(data):
            model = self.current_model
            client_id = request.sid
            prompt = data['prompt']
            personality: AIPersonality = self.personalities[data['personality']]
            personality.model = model
            cond_tk = personality.model.tokenize(personality.personality_conditioning)
            n_cond_tk = len(cond_tk)
            # Placeholder code for text generation
            # Replace this with your actual text generation logic
            print(f"Text generation requested by client: {client_id}")

            self.answer[0] = ''
            full_discussion_blocks = self.clients[client_id]["full_discussion_blocks"]

            if prompt != '':
                if personality.processor is not None and personality.processor_cfg["process_model_input"]:
                    preprocessed_prompt = personality.processor.process_model_input(prompt)
                else:
                    preprocessed_prompt = prompt
                
                if personality.processor is not None and personality.processor_cfg["custom_workflow"]:
                    full_discussion_blocks.append(personality.user_message_prefix)
                    full_discussion_blocks.append(preprocessed_prompt)
            
                else:

                    full_discussion_blocks.append(personality.user_message_prefix)
                    full_discussion_blocks.append(preprocessed_prompt)
                    full_discussion_blocks.append(personality.link_text)
                    full_discussion_blocks.append(personality.ai_message_prefix)

            else:
                print(output.strip(),end="",flush=True)

            full_discussion = personality.personality_conditioning + ''.join(full_discussion_blocks)

            def callback(text, message_type: MSG_TYPE):
                if message_type == MSG_TYPE.MSG_TYPE_CHUNK:
                    self.answer[0] = self.answer[0] + text
                    emit('text_chunk', {'chunk': text}, room=client_id)
                return True


            tk = personality.model.tokenize(full_discussion)
            n_tokens = len(tk)
            fd = personality.model.detokenize(tk[-min(self.config.ctx_size-n_cond_tk,n_tokens):])
            
            if personality.processor is not None and personality.processor_cfg["custom_workflow"]:
                print("processing...", end="", flush=True)
                generated_text = personality.processor.run_workflow(prompt, previous_discussion_text=personality.personality_conditioning+fd, callback=callback)
                print(generated_text)
            else:
                print("generating...", end="", flush=True)
                generated_text = personality.model.generate(personality.personality_conditioning+fd, n_predict=personality.model_n_predicts, callback=callback)

            if personality.processor is not None and personality.processor_cfg["process_model_output"]: 
                generated_text = personality.processor.process_model_output(generated_text)

            full_discussion_blocks.append(generated_text.strip())
            print(f"{ASCIIColors.color_green}ok{ASCIIColors.color_reset}", end="", flush=True)

            # Emit the generated text to the client
            emit('text_generated', {'text': generated_text}, room=client_id)

    def build_binding(self, bindings_path: Path, cfg: LOLLMSConfig)->LLMBinding:
        binding_path = Path(bindings_path) / cfg["binding_name"]
        # first find out if there is a requirements.txt file
        install_file_name = "install.py"
        install_script_path = binding_path / install_file_name
        if install_script_path.exists():
            module_name = install_file_name[:-3]  # Remove the ".py" extension
            module_spec = importlib.util.spec_from_file_location(module_name, str(install_script_path))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            if hasattr(module, "Install"):
                module.Install(self.config)
        # define the full absolute path to the module
        absolute_path = binding_path.resolve()
        # infer the module name from the file path
        module_name = binding_path.stem
        # use importlib to load the module from the file path
        loader = importlib.machinery.SourceFileLoader(module_name, str(absolute_path / "__init__.py"))
        binding_module = loader.load_module()
        binding_class = getattr(binding_module, binding_module.binding_name)
        return binding_class


    def run(self, host="localhost", port="9600"):
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', '-hst', default=host, help='Host name')
        parser.add_argument('--port', '-prt', default=port, help='Port number')

        parser.add_argument('--config', '-cfg', default=None, help='Path to the configuration file')
        parser.add_argument('--bindings_path', '-bp', default=str(self.lollms_paths.bindings_zoo_path),
                            help='The path to the Bindings folder')
        parser.add_argument('--personalities_path', '-pp',
                            default=str(self.lollms_paths.personalities_zoo_path),
                            help='The path to the personalities folder')
        parser.add_argument('--models_path', '-mp', default=str(self.lollms_paths.personal_models_path),
                            help='The path to the models folder')

        parser.add_argument('--binding_name', '-b', default="llama_cpp_official",
                            help='Binding to be used by default')
        parser.add_argument('--model_name', '-m', default=None,
                            help='Model name')
        parser.add_argument('--personality_full_name', '-p', default="personality",
                            help='Personality path relative to the personalities folder (language/category/name)')
        
        parser.add_argument('--reset_personal_path', action='store_true', help='Reset the personal path')
        parser.add_argument('--reset_config', action='store_true', help='Reset the configurations')
        parser.add_argument('--reset_installs', action='store_true', help='Reset all installation status')


        args = parser.parse_args()

        if args.reset_installs:
            reset_all_installs()

        if args.reset_personal_path:
            LollmsPaths.reset_configs()

        if args.reset_config:
            cfg_path = LollmsPaths.find_paths().personal_configuration_path / "local_config.yaml"
            try:
                cfg_path.unlink()
                ASCIIColors.success("LOLLMS configuration reset successfully")
            except:
                ASCIIColors.success("Couldn't reset LOLLMS configuration")

        # Configuration loading part
        self.config = LOLLMSConfig.autoload(self.lollms_paths, args.config)


        if args.binding_name:
            self.config.binding_name = args.binding_name

        if args.model_name:
            self.config.model_name = args.model_name

        # Recover bindings path
        self.personalities_path = Path(args.personalities_path)
        self.bindings_path = Path(args.bindings_path)
        self.models_path = Path(args.models_path)
        if self.config.binding_name is None:
            self.menu.select_binding()
        else:
            self.binding_class = self.build_binding(self.bindings_path, self.config)
        if self.config.model_name is None:
            self.menu.select_model()
        else:
            try:
                self.current_model = self.binding_class(self.config)
            except Exception as ex:
                print(f"{ASCIIColors.color_red}Couldn't load model Please select a valid model{ASCIIColors.color_reset}")
                print(f"{ASCIIColors.color_red}{ex}{ASCIIColors.color_reset}")
                self.menu.select_model()

        for p in self.config.personalities:
            personality = AIPersonality(self.lollms_paths, self.config.lollms_paths.personalities_zoo_path/p, self.current_model)
            self.personalities.append(personality)

        self.active_personality = self.personalities[self.config.active_personality_id]

        self.menu.show_logo()
        print(f"{ASCIIColors.color_red}Current personality : {ASCIIColors.color_reset}{self.active_personality}")
        print("running...")

        self.socketio.run(self.app, host=args.host, port=args.port)

def main():
    LoLLMsServer()


if __name__ == '__main__':
    main()