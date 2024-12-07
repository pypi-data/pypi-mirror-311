from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata

class NLPAgent:

    def __init__(self) -> None:
        pass

    def get_agent(self,
                  callback_handler = None,
                  persist_path:str = None,
                  file_path:str = None,
                  llm_ver:str = None,
                  temperature:int = None,
                  model:str = None,
                  embed_batch_size:int = None,
                  metadata_name:str = None,
                  metadata_desc:list[str] = None):
        if llm_ver is None or llm_ver.strip() == '':
            llm_ver = "gpt-4"
        if temperature is None:
            temperature = 0
        if model is None or model.strip() == '':
            model = "text-embedding-3-small"
        if embed_batch_size is None:
            embed_batch_size = 100
        if metadata_name is None or metadata_name.strip() == '':
            metadata_name = "xurpas_faq"
        if metadata_desc is None or metadata_desc.strip() == '':
            metadata_desc = ["Provides information about Xurpas."
                        "Use a detailed plain text question as input to the tool."]

        if callback_handler != None:
            print("With callback handler!")
            llm = ChatOpenAI(
                temperature=temperature,
                model_name=llm_ver,
                streaming=True,
                callbacks=callback_handler
            )
        else:
            llm = ChatOpenAI(
                temperature=temperature,
                model=llm_ver,
                verbose=True,
                streaming=True
            )

        embed_model = OpenAIEmbedding(
            model=model, embed_batch_size=embed_batch_size
        )

        Settings.llm = llm
        Settings.embed_model = embed_model

        try:
            storage_context = StorageContext.from_defaults(
                persist_dir=persist_path
            )
            data_index = load_index_from_storage(storage_context)

            index_loaded = True
            print("Index was already created. We just loaded it from the local storage.")
        except:
            index_loaded = False
            print("Index is not present. We need it to create it again.")

        if not index_loaded:
            print("Creating Index..")

            docs = SimpleDirectoryReader(
                file_path
            ).load_data()
            data_index = VectorStoreIndex.from_documents(docs)
            data_index.storage_context.persist(persist_dir=persist_path)

            index_loaded = True

        query_engine = data_index.as_query_engine(similarity_top_k=3)

        query_engine_tools = [
            QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name=metadata_name,
                    description=(
                        metadata_desc
                    ),
                ),
            )
        ]

        converted_tools = [t.to_langchain_tool() for t in query_engine_tools]

        print("No of LlamaIndex Tools:", len(converted_tools))

        system_context = """
    You are an AI chatbot developed by Xurpas, integrated into their website using LangChain and OpenAI. Your primary role is to assist visitors by answering inquiries about the company and the services it offers. The answers should be based on information found in the provided PDF and TXT documents.

    ### Instructions:
    1. Answer questions strictly related to Xurpas, its company information, or its services.
    2. Utilize the information found in the provided PDFs and TXTs to formulate your responses.
    3. If a visitor requests an appointment, consultation, or demo, ask for the following details: name, email, contact details, and preferred appointment date and time.
    4. Politely ignore any messages that do not pertain to Xurpas or its services with a courteous response.
    5. Ensure all responses are professional, concise, and helpful.

    ### Example Interactions:
    **Visitor:** "What are the services offered by Xurpas?"
    **AI:** "Xurpas offers a variety of services including software development, mobile app development, and IT consulting.

    **Visitor:** "Can you tell me about the company's history?"
    **AI:** "Xurpas was founded in 2001 and has since grown to become a leading technology company in the Philippines.

    **Visitor:** "I'd like to schedule an appointment."
    **AI:** "I'd be happy to assist with that. Could you please provide your name, email, contact details, and your preferred appointment date and time?"

    **Visitor:** "I'd like to book a consultation."
    **AI:** "I'd be happy to assist with that. Could you please provide your name, email, contact details, and your preferred appointment date and time?"

    **Visitor:** "I'd like to book a demo."
    **AI:** "I'd be happy to assist with that. Could you please provide your name, email, contact details, and your preferred appointment date and time?"

    **Visitor:** "What's the weather like today?"
    **AI:** "I'm here to assist you with questions related to Xurpas and its services. Is there anything specific you would like to know about our company?"
    """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_context,
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_tool_calling_agent(
            llm=llm,
            tools=converted_tools,
            prompt=prompt
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=converted_tools,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
            max_iterations=10
        )

        return agent_executor