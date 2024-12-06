from .datatypes import EAOntology, EROntology, LLMClient, EAEdge, EREdge, Document
from pydantic import ValidationError
from .KGLogger import loggers
from typing import List, Union
import json
import re
import time
import datetime


# 定义知识图谱构建类
class KnowledgeGraphBuilder:
    def __init__(self, ontology: Union[EAOntology, EROntology], llm_client: LLMClient):
        self.ontology = ontology
        self.llm_client = llm_client
    
    # 定义日志的格式，包括通知，错误和详细三种格式
    def log(self, level, message):
        loggers[level].info(message)

    # 格式化用户的输入文本
    def format_user_input(self, user_text: str) -> str:
        return f"The user input text is: ```\n{user_text}\n```"
    
    # 格式化实体关系三元组提取的系统提示
    def format_EROntology_prompt(self) -> str:
        return (
            "You are an expert at creating Knowledge Graphs. "
            "Consider the following ontology. \n"
            f"{self.ontology.dump()} \n"
            "The user will provide you with an input text delimited by ```. "
            "Extract all the entities and relationships from the user-provided text as per the given ontology. Do not use any previous knowledge about the context."
            "Remember there can be multiple direct (explicit) or implied relationships between the same pair of nodes. "
            "Be consistent with the given ontology. Use ONLY the labels and relationships mentioned in the ontology. "
            "When extracting relationships between entities, strictly follow the relationship names in the relationships list defined in the ontology, and do not add other relationship types and names independently. "
            "Format your output as a json with the following schema. \n"
            "[\n"
            "   {\n"
            '       node_1: Required, an entity object with attributes: {"entity": "as per the ontology, According to the type field of the entities list defined in the ontology", "name": "Name of the entity"},\n'
            '       node_2: Required, an entity object with attributes: {"entity": "as per the ontology, the label of the entity", "name": "Name of the entity"},\n'
            #"       relationship: Describe the relationship between node_1 and node_2 as per the context, in a few sentences.\n"
			"       relationship: Required,  the relationship type between node_1 and node_2 defined in the ontology, and do not add any other comments before or after the relationship type .\n"
            "   },\n"
            "]\n"
            "Do not add any other comment before or after the json. Respond ONLY with a well formed json that can be directly read by a program."
        )
    
    # 格式化实体属性三元组提取的系统提示
    def format_EAOntology_prompt(self) -> str:
        return (
            "You are an expert at creating Knowledge Graphs. "
            "Consider the following ontology. \n"
            f"{self.ontology.dump()} \n"
            "The user will provide you with an input text delimited by ```. "
            "According to the given ontology, entities, attributes possessed by entities, and attribute values corresponding to the attributes are extracted from the text provided by the user. "
            "Be consistent with the given ontology. Only use entities and attributes mentioned in the ontology. "
            "If the same entity and attribute has multiple attribute values, these multiple different attribute values are combined into one string. "
            "Format your output as a json with the following schema. \n"
            "[\n"
            "   {\n"
            '       node_1: Required, an entity object with attributes: {"entity": "According to the type field of the entities list defined in the ontology", "name": "Name of the entity"},\n'
            '       node_2: Required, Extract the corresponding entity attribute value based on the type field in the attributes list: {"attribute": "According to the type field of the attributes list defined in the ontology", "name": "The value of the attribute"},\n'
            "       relationship: Required, the content of the ontology-defined attribute list, that is, the attributes of the node_1 node. Don't add any attribute relationships other than the ontology definition. \n"
            "   },\n"
            "]\n"
            "Do not add any other comment before or after the json. Respond ONLY with a well formed json that can be directly read by a program."
        )
    
   

    # 根据定义的本体模式调用对应的系统提示
    def format_prompt(self) -> str:
        if isinstance(self.ontology, EROntology):
            return self.format_EROntology_prompt()
        elif isinstance(self.ontology, EAOntology):
            return self.format_EAOntology_prompt()
        else:
            raise ValueError("Unsupported or Invalid Ontology Type")

    # 调用LLM生成相应提取知识图谱三元组
    def generate_responses(self, user_text: str) -> str:
        return self.llm_client.generate_response(
            user_message=self.format_user_input(user_text),
            system_message=self.format_prompt(),
        )
    
    # 调用LLM为每个用户输入的文本块生成摘要作为元数据
    def summary(self, user_text: str) -> str:
        try:
            prompt = "Succinctly summarise the text provided by the user. Respond only with the summary and no other comments"
            return self.llm_client.generate_response(user_message=user_text, system_message=prompt)
        except Exception as e:
            return ""
    
    # 将每个文本块映射到一个新的Document对象，Document对象包含文本和一些元数据
    def create_docs(self, user_text: List[str]):
        current_time = str(datetime.datetime.now())
        return map(
            lambda t: Document(
                text=t,
                metadata={
                    "summary": self.summary(t),
                    'generated_at': current_time,
                },
            ),
            user_text,
        )

    # 利用json固有的方法自动解析出json格式
    def response_to_json (self, text: str):
        self.log("INFO", f"Attempting to parse JSON: \n{text}")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.log("ERROR", f"Failed to parse JSON: {e.msg}, Invalid JSON: {text}")
            return None

    # 利用正则表达式手动的解析出json格式
    def parse_manually(self, text: str):
        self.log("INFO", f"Attempting Manual Parsing: \n{text}")
        pattern = r"\}\s*,\s*\{"
        try:
            cleaned_text = text.replace("\n[{]}` ", "")
            obj_strings = re.split(pattern, cleaned_text, flags=re.MULTILINE | re.DOTALL)
            json_objects = ["{" + obj_string + "}" for obj_string in obj_strings if obj_string.strip()]
            return [json.loads(obj) for obj in json_objects]
        except Exception as e:
            self.log("ERROR", f"Error during manual parsing: {str(e)}, Invalid input: {text}")
            return []
        
    # 将生成的json转化为边
    def data_to_edge(self, edge_data):
        try:
            if isinstance(self.ontology, EAOntology):
                return EAEdge(**edge_data)
            elif isinstance(self.ontology, EROntology):
                return EREdge(**edge_data)
            else:
                raise ValueError("Unsupported or Invalid Ontology Type")
        except ValidationError as e:
            self.log("ERROR", f"Edge parsing failed: {e.errors(include_url=False, include_input=False)}, Invalid edge data: {edge_data}")
            return None

    # 过滤掉node_2中value为空的边
    def extract_valid_edges(self, jsondata):
        edges = []
        for edge_data in jsondata:
            if edge_data and edge_data.get('node_2', {}).get('name'):
                if edge := self.data_to_edge(edge_data):
                    edges.append(edge)
        return edges
    
    # 处理文本并生成边
    def text_to_edges(self, user_text: str):
        response_text = self.generate_responses(user_text)
        if not response_text:
            self.log("ERROR", "Empty response from Knowledge Graph Builder")
        self.log("INFO", "Response received, parsing JSON.")
        try:
            jsondata = self.response_to_json(response_text)
        except json.JSONDecodeError:
            jsondata = self.parse_manually(response_text) or []
        return self.extract_valid_edges(jsondata)  

    # 处理文档并生成子图
    def document_to_subgraph(self, doc: Document, sequence: Union[int, None] = None) -> List[Union[EAEdge, EREdge]]:
        self.log("DEBUG", f"Extracting edges from document with ontology:\n{self.ontology.dump()}")
        edges = self.text_to_edges(doc.text)
        for edge in edges:
            if edge:
                edge.metadata = doc.metadata
                edge.sequence = sequence
        self.log("DEBUG", f"Extracted {len(edges)} edges with metadata and sequence.")
        return edges
    
    # 处理延迟
    def pause(self, delay):
        self.log("INFO", f"Waiting for {delay}s before the next request ... ")
        time.sleep(delay)

    # 处理文档列表并生成知识图谱
    def documents_to_graph(self, docs: List[Document], sequence_key: Union[int, None] = None, delay=0) -> List[Union[EAEdge, EREdge]]:
        graph = []
        for index, doc in enumerate(docs):
            sequence = getattr(doc, sequence_key) if sequence_key else index
            self.log("INFO", f"Processing document: {index+1}")
            subgraph = self.document_to_subgraph(doc, sequence)
            graph.extend(subgraph)
            if delay > 0:
                self.pause(delay)
            self.log("DEBUG", f"Extracted graph with {len(graph)} edges from {len(docs)} documents.")
        return graph
    