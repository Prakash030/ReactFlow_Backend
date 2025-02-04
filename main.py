from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Pipeline(BaseModel):
    nodes: list
    edges: list

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    try:
        nodes = pipeline.nodes
        edges = pipeline.edges

        G = nx.DiGraph()

        for node in nodes:
            G.add_node(node["id"])
        
        for edge in edges:
            G.add_edge(edge["source"], edge["target"])
        
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        
        is_dag = nx.is_directed_acyclic_graph(G)
        
        return {
            "ok": "true",
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'is_dag': is_dag
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
