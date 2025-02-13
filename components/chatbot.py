import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


class ChatbotComponent:
    def __init__(self, open_api_key, csv_file=None, data_dict=None):
        self.open_api_key = open_api_key
        self.qa_chain = self._initialize_rag(csv_file, data_dict)
    def _process_data_dict(self, data_dict):
        df = pd.read_csv(data_dict)
        return [Document(page_content=str(row)) for row in df.astype(str).values.tolist()]
    def _initialize_rag(self, csv_file, data_dict):
        # Initialize documents
        documents = []
        if data_dict:
            documents = self._process_data_dict(data_dict)
        elif csv_file:
            df = pd.read_csv(csv_file)
            documents = [Document(page_content=str(row)) for row in df.astype(str).values.tolist()]
        # Split documents
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = text_splitter.split_documents(documents)
        # Create embeddings
        embedding_model = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            api_key=self.open_api_key
        )
        vectorstore = FAISS.from_documents(split_docs, embedding_model)
        retriever = vectorstore.as_retriever()
        # Initialize OpenAI model
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            api_key=self.open_api_key
        )
        return RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )
    def ask_question(self, query):
        return self.qa_chain.run(query)
    def create_layout(self):
        return html.Div([
            html.Button(
                ':speech_balloon: Chat',
                id='chat-button',
                n_clicks=0,
                style={
                    'position': 'fixed',
                    'bottom': '20px',
                    'right': '20px',
                    'background': '#007BFF',
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 15px',
                    'border-radius': '20px',
                    'cursor': 'pointer'
                }
            ),
            html.Div(
                id='chat-container',
                children=[
                    html.Div([
                        html.Img(
                            src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png',
                            style={'width': '50px', 'border-radius': '50%'}
                        ),
                        html.Span(
                            "Heart Disease",
                            style={'font-weight': 'bold', 'margin-left': '10px'}
                        ),
                        html.Span(
                            ":large_green_circle: Online",
                            style={'color': 'green', 'margin-left': '10px'}
                        )
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
                    html.Div(
                        id='chat-history',
                        children=[],
                        style={
                            'border': '1px solid #ccc',
                            'padding': '10px',
                            'height': '300px',
                            'overflowY': 'scroll',
                            'background': '#F9F9F9',
                            'border-radius': '10px'
                        }
                    ),
                    html.Div([
                        dcc.Input(
                            id='user-input',
                            type='text',
                            placeholder='Enter your message...',
                            style={
                                'flex': '1',
                                'padding': '10px',
                                'border': '1px solid #ccc',
                                'border-radius': '5px'
                            }
                        ),
                        html.Button(
                            '➤',
                            id='send-button',
                            n_clicks=0,
                            style={
                                'background': '#007BFF',
                                'color': 'white',
                                'border': 'none',
                                'padding': '10px 15px',
                                'border-radius': '5px',
                                'cursor': 'pointer'
                            }
                        )
                    ], style={'display': 'flex', 'margin-top': '10px'}),
                ],
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'bottom': '70px',
                    'right': '20px',
                    'width': '400px',
                    'padding': '20px',
                    'border': '1px solid #ddd',
                    'border-radius': '10px',
                    'box-shadow': '0px 0px 10px rgba(0,0,0,0.1)',
                    'background': 'white'
                }
            ),
        ], style={'position': 'relative'})
    def register_callbacks(self, app):
        @app.callback(
            Output('chat-container', 'style'),
            Input('chat-button', 'n_clicks'),
            State('chat-container', 'style')
        )
        def toggle_chatbot(n_clicks, current_style):
            if n_clicks % 2 == 1:
                return {**current_style, 'display': 'block'}
            return {**current_style, 'display': 'none'}
        @app.callback(
            Output('chat-history', 'children'),
            Input('send-button', 'n_clicks'),
            State('user-input', 'value'),
            State('chat-history', 'children'),
            prevent_initial_call=True
        )
        def update_chat(n_clicks, user_message, chat_history):
            if not user_message:
                return chat_history if chat_history else []
            chatbot_response = self.ask_question(user_message)
            new_chat = html.Div([
                html.Div(
                    f"You: {user_message}",
                    style={
                        'background': '#007BFF',
                        'color': 'white',
                        'padding': '10px',
                        'border-radius': '10px',
                        'margin': '5px 0'
                    }
                ),
                html.Div(
                    f"Response: {chatbot_response}",
                    style={
                        'background': '#E9ECEF',
                        'padding': '10px',
                        'border-radius': '10px',
                        'margin': '5px 0'
                    }
                )
            ])
            return chat_history + [new_chat] if chat_history else [new_chat]