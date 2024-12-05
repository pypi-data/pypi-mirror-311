import os
import warnings
from langchain.vectorstores import Chroma
from langchain.agents import Tool
from langchain import LLMChain
from langchain_core.prompts import PromptTemplate
import re
from langchain.tools import Tool, tool
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import initialize_agent 
from langchain.agents import AgentType
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from danilo_planner.midirectorio import MiClase
import json

warnings.filterwarnings("ignore", category=DeprecationWarning)

global collecciones
global collecciones_planificador
global colleccion_actual
global planificador_actual

api_hugginface=""
api_key=""
input_memory=[]
collecciones = []
colleccion_actual=[]
collecciones_planificador=[]
planificador_actual=[]

json_file_path = os.path.normpath(f"danilo_planner\\collecciones.json")

def cargar_json(ruta):
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {"colecciones": []}

def guardar_json(ruta, data):
    with open(ruta, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def agregar_coleccion(nombre_coleccion):
    data = cargar_json(json_file_path)
    data["colecciones"].append(nombre_coleccion)
    guardar_json(json_file_path, data)
    print(f"Colección '{nombre_coleccion}' agregada exitosamente.")

#####################################################################
# CORREGIR ESTA COSA SOLO CARGA EL COLECCIONES
def cargar_colecciones_en_vector():
    data = cargar_json(json_file_path)
    datos=data.get("colecciones", [])
    for item in datos:
        collecciones_planificador.append(item)
#####################################################################

def leer_plan(texto_indicacion_leer_planificador):
    """
        parametros: texto con la indicación del usuario para leer el plan
        procesamiento: se lee el plan dado un texto con la indicación
        retorno: El formato adecuado de documentos para crear el repositorio de planificacion
    """
    loader = DirectoryLoader("danilo_planner", glob=f"**\\{colleccion_actual[0]}.txt", loader_cls=TextLoader)
    documents = loader.load()
    return documents

def leer_planinificador(texto_indicacion_leer_planificador):
    """
        parametros: texto con la indicación del usuario para leer el plan
        procesamiento: se lee el plan dado un texto con la indicación
        retorno: El formato adecuado de documentos para crear el repositorio de planificacion
    """
    loader = DirectoryLoader("danilo_planner", glob=f"**\\{planificador_actual[0]}.txt", loader_cls=TextLoader)
    documents = loader.load()
    return documents

def crear_carpeta():
    ruta=MiClase.select_directory()
    nueva_carpeta = os.path.join(ruta, "Planes")
    if not os.path.exists(nueva_carpeta):
        os.makedirs(nueva_carpeta)
        print(f"Carpeta 'Planes' creada en: {nueva_carpeta}")
    else:
        print(f"La carpeta 'Planes' ya existe en: {nueva_carpeta}")


def mostrar_lista_planificadores(collecciones):
    if not collecciones:
        print("No hay planificadores disponibles.")
        return
    
    print("Lista de colecciones de planificadores:")
    for i in range (len(collecciones)):
        print(f"{i+1}. {collecciones[i]}")


@tool
def lista_mejoras_explicitas(lista_mejoras):
    """
        parametros: texto con la lista de mejoras explicitas por parte del usuario
        procesamiento: se actualiza el planificador con las mejoras explicitas
        retorno: actualización exitosa del planificador
    """
    conversacion=lista_mejoras
    docs=leer_planinificador("Leer planificador")
    planificacion_actual = format_docs(docs)
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
    prompt_template = f"""
    La planificación actual es la siguiente:
    {planificacion_actual}
    y la conversación es la siguiente:
    {conversacion}
    extrae de manera estricta las acciones de mejora de la conversación y aplicalas en código PDDL a la planificación actual.
    solo devuelve la planificación en PDDL con las acciones de mejora.
    """
    multi_input_prompt = PromptTemplate(
            input_variables=["planificacion_actual", "conversacion"], 
            template=prompt_template
        )
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
    llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
    result = llm_chain.run({"planificacion_actual": planificacion_actual , "conversacion": conversacion})
    response=actualizar_planificador(result)
    var_control[0]=0
    input_memory.clear()
    auxiliar[0]=0
    return f"Implementación éxitosa: {response}"


@tool
def crear_plan(especificaciones):
    """
        parametros: texto con las especificaciónes del plan a crear
        procesamiento: se crea el plan segun las especificaciones del usuario
        retorno: mensaje de confirmación de la creación del plan y el contenido retornado
    """
    try:
        nombre=colleccion_actual[0]
        persist_directory_plan = os.path.normpath(f"danilo_planner\\{nombre}.txt")
        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
        
        if os.path.exists(persist_directory_plan) and os.path.getsize(persist_directory_plan) > 0:
            with open(persist_directory_plan, 'r', encoding='utf-8') as archivo:
                contenido_existente = archivo.read()
            return f"El planificador ya existe y contiene datos:\n{contenido_existente}"
        else:
            multi_input_template = """
            Eres un experto en lenguaje {programming_language}.
            {query}
            """
            multi_input_prompt = PromptTemplate(
                input_variables=["programming_language", "query"], 
                template=multi_input_template
            )
            llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
                
            programming_language = "PDDL"
            query = especificaciones
                
            total = llm_chain.run({"programming_language": programming_language, "query": query})
                
            patron = r"```(.*?)```"
            resultados = re.findall(patron, total, re.DOTALL)
            contenido_dentro_triples_comillas = '\n'.join(resultados) if resultados else total.strip()
            contenido_sin_pddl = re.sub(r'\blisp\b', '', contenido_dentro_triples_comillas, flags=re.IGNORECASE)
                
            directorio = os.path.dirname(persist_directory_plan)
            if not os.path.exists(directorio):
                os.makedirs(directorio)
                    
            with open(persist_directory_plan, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_sin_pddl)
                
            mi_clase_instance = MiClase()
            ruta=mi_clase_instance.select_directory()
            with open(ruta+f"\\{nombre}.txt", "w", encoding="utf-8") as archivo:
                archivo.write(contenido_sin_pddl)

            return f"El planificador fue creado exitosamente y guardado:\n{contenido_sin_pddl}"
        
    except Exception as e:
            return str(e) 


from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough


def format_docs(docs1):
    loader = DirectoryLoader("danilo_planner", glob=f"**\\{planificador_actual[0]}.txt", loader_cls=TextLoader)
    docs1=loader.load()
    return "\n\n".join(str(page.page_content) for page in docs1)
    
@tool        
def crear_planificador(texto_indicacion_crear_repositorio):
    """
        parametros: texto con las indicación de crear el planificador 
        procesamiento: se crea el planificador segun las indicaciones del usuario
        retorno: mensaje de confirmación de la creación del planificador
    """
    nombre=planificador_actual[0]
    persist_directory = f"danilo_planner\\{nombre}"
    Chroma_DB = Chroma(persist_directory=persist_directory, embedding_function=agent.embeddings).as_retriever()
    query = "planificación"
    docs = Chroma_DB.get_relevant_documents(query)
    
    if docs:
        return "El repositorio existe"
        
    docs = leer_plan("leer plan")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=0)
    splits = text_splitter.split_documents(docs)
    Chroma.from_documents(documents=splits, embedding=agent.embeddings,persist_directory=persist_directory)
    return "planificador creado con éxito"


@tool
def consultar_planificador(prompt):
    """
        parametros: prompt donde el usuario requiere consultar y retornar el contenido del planificador
        procesamiento: herramienta usada para consultar recibiendo el prompt de parte del usuario
        retorno: consulta realizada
    """
    nombre=planificador_actual[0]
    persist_directory = os.path.normpath(f"danilo_planner\\{nombre}")
    Chroma_DB = Chroma(
        persist_directory=persist_directory, 
        embedding_function=agent.embeddings
    )
    
    retriever = Chroma_DB.as_retriever()
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
    template = """
            Responda la pregunta según el contexto proporcionado.
        \n\n
        contexto:\n {context}?\n
        pregunta: \n{question}\n
        Respuesta:
        """
    custom_rag_prompt = PromptTemplate.from_template(template)
    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
    )
    return rag_chain.invoke(prompt) 

var_control=[0]
auxiliar=[0]

def actualizar_planificador(result):
    """
        parametros: texto con la indicación de actualizar el planificador
        procesamiento: actualiza el planificador
        salida: actualización exitosa
    """
    nombre=planificador_actual[0]
    persist_directory = os.path.normpath(f"danilo_planner\\{nombre}")
    persist_directory_plan = os.path.normpath(f"danilo_planner\\{nombre}.txt")
    docs=leer_planinificador("Leer planificador")
    planificacion_actual = format_docs(docs)
    conversacion = result
    if not conversacion:
        return "No hay conversación previa"
    prompt_template = f"""
    Al siguiente documento de planificación en lenguaje PDDL:

        {planificacion_actual}
        
    extrae e incorpora los planes de mejora de la siguiente conversación sin modificar los planes dados inicialmente:

        {conversacion}

    y siendo estricto en no cambiar la lógica inicial del código PDDL retorna solo el código con las incorporaciones.
    """
    
    multi_input_prompt = PromptTemplate(
                input_variables=["planificacion_actual", "conversacion"], 
                template=prompt_template
            )
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
    llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
    
    result = llm_chain.run({"planificacion_actual": planificacion_actual, "conversacion": conversacion})
    patron = r"```(.*?)```"
    resultados = re.findall(patron, result, re.DOTALL)
    contenido_dentro_triples_comillas = '\n'.join(resultados) if resultados else result.strip()
    contenido_sin_pddl = re.sub(r'\bpddl\b', '', contenido_dentro_triples_comillas, flags=re.IGNORECASE)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=0)
    splits = text_splitter.split_documents(docs)
    
    Chroma_DB = Chroma(persist_directory=persist_directory, embedding_function=agent.embeddings)
    ids_to_delete = Chroma_DB.get()["ids"]
    for id in ids_to_delete:
        Chroma_DB.delete([id])
        
    Chroma.from_documents(documents=splits, embedding=agent.embeddings,persist_directory=persist_directory)
    ruta=MiClase.select_directory()
    with open(ruta+f"\\{nombre}.txt", "w", encoding="utf-8") as archivo:
        archivo.write(contenido_sin_pddl)

    with open(persist_directory_plan, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido_sin_pddl)
    
    agent.memory.chat_memory.clear()
            
    return f"El planificador fue actualizado exitosamente."

@tool
def sugerir_o_implementar_planes_de_mejora(texto_indicacion_sugerir_mejora):
        """
        parametros: texto con la indicación de sugerir planes de mejora o implementar planes de mejora 
        procesamiento: se implementan o sugieren planes de mejoras segun la indicación del usuario
        retorno: lista con las mejoras sugeridas o la confirmación de implementación éxitosa, o en caso contrario, un mensaje de rechazo
        """
        if(var_control[0]==0):
            input_memory.clear()
            var_control[0]=1
        if(len(input_memory)==0):
            docs=leer_planinificador("Leer planificador")
            planificacion_actual = format_docs(docs)
            prompt_template = f"""
            La planificación actual es la siguiente:
            {planificacion_actual}
            sugiere planes de mejora sin alterar la lógica actual del planificador y retorna solo los planes listados y sin incluir código PDDl a dichos planes.
            """
            multi_input_prompt = PromptTemplate(
                    input= planificacion_actual,
                    template=prompt_template
                )
            llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
            llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
            result = llm_chain.run({"planificacion_actual": planificacion_actual})
            return result
        else:
            if(auxiliar[0]==1):
                conversacion=input_memory[0]
                docs=leer_planinificador("Leer planificador")
                planificacion_actual = format_docs(docs)
                llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
                prompt_template = f"""
                La planificación actual es la siguiente:
                {planificacion_actual}
                y la conversación es la siguiente:
                {conversacion}
                extrae de manera estricta las acciones de mejora de la conversación y aplicalas en código PDDL a la planificación actual sin alterar la lógica actual del planificador.
                """
                multi_input_prompt = PromptTemplate(
                        input_variables=["planificacion_actual", "conversacion"], 
                        template=prompt_template
                    )
                llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_key)
                llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
                result = llm_chain.run({"planificacion_actual": planificacion_actual , "conversacion": conversacion})
                response=actualizar_planificador(result)
                var_control[0]=0
                input_memory.clear()
                auxiliar[0]=0
                return f"Implementación éxitosa: {response}"
            else:
                var_control[0]=0
                input_memory.clear()
                auxiliar[0]=0
                return "No se aceptaron las mejoras"
        
class PlanificadorAgent:
    def __init__(self):
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=api_hugginface, model_name="sentence-transformers/all-MiniLM-l6-v2"
        )

        self.tools =[
            Tool(
                name='crear_plan',
                func=crear_plan,
                description="se crea el plan segun las especificaciones del usuario"
            ),
            Tool(
                name='crear_planificador',
                func=crear_planificador,
                description="Se crea el planificador segun las indicaciones del usuario"
            ),
            Tool(
                name='consultar_planificador',
                func=consultar_planificador,
                description="herramienta usada para consultar recibiendo el prompt de parte del usuario"
            ),
            Tool(
                name='sugerir_o_implementar_planes_de_mejora',
                func=sugerir_o_implementar_planes_de_mejora,
                description="se implementan o sugieren planes de mejoras segun la indicación del usuario"
            ),Tool(
                name='lista_mejoras_explicitas',
                func=lista_mejoras_explicitas,
                description="se actualiza el planificador con las mejoras explicitas")
            ]
            
        self.memory = ConversationBufferMemory()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Usa la herramienta más apropiada para dar una respuesta satisfactoria al usuario."),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=ChatOpenAI(temperature=0, model="gpt-4o-mini",api_key=api_key),
            prompt=self.prompt,
            memory=self.memory,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            return_intermediate_steps=False,
            handle_parsing_errors=True,
        )
    
    def chat(self, input):
        try:
            response = self.agent.invoke({'input': input})
            if isinstance(response, dict):
                response_text = response.get("content", "")
            else:
                response_text = str(response)

            self.memory.save_context(
                {"input": input},       
                {"output": response_text}    
            )
            return response
        except Exception as e:
            return str(e)

cargar_colecciones_en_vector()
api_hugginface= str(input("Ingrese la api de Hugging Face: "))
api_key= str(input("Ingrese la api de GPT: "))
agent = PlanificadorAgent()
crear_planificador=str(input("Indique si desea crear un nuevo planificador con el siguiente texto: crear nuevo planificador: "))
if crear_planificador.lower() in ["crear nuevo planificador"]:
    especificaciones=str(input("Indique las especificaciones del plan: "))
    crear_carpeta()
    nombre=str(input("Indique el nombre del documento: "))
    colleccion_actual.append(nombre)
    response= agent.chat(especificaciones)
    print(f"Assistant: {response}")
    collecciones.append(nombre)
    nombre_c=str(input("Indique el nombre del planificador: "))
    collecciones_planificador.append(nombre_c)
    agregar_coleccion(nombre_c)
    planificador_actual.append(nombre_c)
    response= agent.chat("crea el planificador")
    print(f"Assistant: {response}")
    print("Bienvenido.")
    while True:
        if var_control[0] == 1:
            user_input = input("Para aceptar las mejoras escriba: implementa las mejoras al planificador: ")
            if user_input.lower() in ["implementa las mejoras al planificador"]:
                auxiliar[0]= 1
            else:
                user_input = input("You: ")
        if var_control[0] == 0:
            user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = agent.chat(user_input)
        input_memory.append(agent.memory.buffer)
        print(f"Assistant: {response}")
else:
    mostrar_lista_planificadores(collecciones_planificador)
    opcion=int(input("Indique el número de la colección de planes que desea consultar: "))
    collecion=collecciones_planificador[opcion-1]
    planificador_actual.append(collecion)
    print("Bienvenido.")
    while True:
        if var_control[0] == 1:
            user_input = input("Para aceptar las mejoras escriba: implementa las mejoras al planificador: ")
            if user_input.lower() in ["implementa las mejoras al planificador"]:
                auxiliar[0]= 1
            else:
                user_input = input("You: ")
        if var_control[0] == 0:
            user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = agent.chat(user_input)
        input_memory.append(agent.memory.buffer)
        print(f"Assistant: {response}")

planificador_actual.clear()