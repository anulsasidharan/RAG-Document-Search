"""Graph Builder for LangGraph workflow"""

from langgraph.graph import StateGraph, END
from src.state.rag_state import RAGState
from src.node.reactnode import RAGNodes

class GraphBuilder:
    """Build and Manage the LangGraph Workflow"""
    
    def __init__(self, retriever, llm):
        """Initilize graph builder

        Args:
            retriever : Document retriever instance
            llm : language model instance
        """
        self.nodes = RAGNodes(retriever, llm)
        self.graph = None
        
    def build(self):
        """
        Build the RAG workflow graph
        
        Returns:
            Compiled graph instance
        """
        
        # Create state graph
        builder = StateGraph(RAGState)
        
        # Add Nodes
        builder.add_node("retriever", self.nodes.retrieve_docs)
        builder.add_node("responder", self.nodes.generate_answer)
        
        # Set Entry point
        builder.set_entry_point("retriever")
        
        # Add edges
        builder.add_edge("retriever", "responder")
        builder.add_edge("responder", END)
        
        # compile the graph
        
        self.graph = builder.compile()
        return self.graph
    
    def run(self, question:str) -> dict:
        """
        Run the RAG workflow

        Args:
            question: User Question

        Returns:
            Final state with answer
        """
        if self.graph is None:
            self.build()
            
        initial_state = RAGState(question=question)
        return self.graph.invoke(initial_state)