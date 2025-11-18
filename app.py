import torch
from contextlib import asynccontextmanager

from src.QuickScope.logger.custom_logger import logger

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from peft import PeftModel

# API connection for live data retrival
from src.QuickScope.pipeline.stage_01_data_generation import DataGenerationPipeline
from src.QuickScope.pipeline.stage_03_data_transformation import DataTransformationPipeline
from src.QuickScope.pipeline.stage_05_model_prediction import PredictionPipeline
# Setting up FastAPI app with CORS middleware .

@asynccontextmanager
async def lifespan(app: FastAPI):
    # setting up the fetching api for live data retrival
    data_gen = DataGenerationPipeline()
    
    base = "unsloth/Llama-3.2-1B-Instruct-bnb-4bit"
    adapter = "artifacts/finetunedModel"  # Path to your local model directory
    tokenizer = AutoTokenizer.from_pretrained(base)
    base_model = AutoModelForCausalLM.from_pretrained(base, device_map="auto")
    model = PeftModel.from_pretrained(base_model, adapter)
    logger.info("Successfully loaded Model and Tokenizer...")
    app.state.model = model
    app.state.tokenizer = tokenizer
    app.state.data_gen = await data_gen.init_connection()
    logger.info('models initialized ------------------------------------')
    print('models initialized ------------------------------------')

    yield

    del app.state.model
    del app.state.tokenizer
    await app.state.data_gen.close()
    torch.cuda.empty_cache()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_transformer = DataTransformationPipeline()
predictor = PredictionPipeline()


@app.get('/api/get_news/')
async def get_news(request:Request,topic:str):
    if topic.strip() =='':
        return {'message':'no topic recieved'}
    model = request.app.state.model
    tokenizer = request.app.state.tokenizer
    data_gen = request.app.state.data_gen
    
    
    # streamer = CustomStreamer(streamer_queue, tokenizer, True)
    
    # news = await dataset.get_news(topic)
    data = await data_gen.main(topic)
    
    transformed_data = data_transformer.main(topic,data)

    streaming_response = predictor.main(model,tokenizer,transformed_data)
    return StreamingResponse(
        streaming_response,
        # response_generator(model,tokenizer,streamer, message), 
        media_type='text/event-stream',
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        })