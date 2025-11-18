from QuickScope.entity import ModelPredictionConfig
from QuickScope.logger.custom_logger import logger
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

import asyncio
from threading import Thread

class ModelPrediction:
    def __init__(self,prediction_config:ModelPredictionConfig):
        self.config = prediction_config
        
    def load_model_tokenizer(self):
        model_path = self.config.model_path
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            # dtype="float32",   # CPU-friendly dtype
            device_map="auto"
        )
        logger.info('Loaded Model For Prediction...')
        
        return model,tokenizer
        
    def start_generation(self,model, tokenizer, streamer, message):  
        # Converting the inputs to tokens for prediction  
        text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt").to(model.device)  
        
        # key word arguments that are provided to the model.generate()function  
        # Includes, inputs, max_tokens, streamer, temparature  
        generation_kwargs = dict(inputs, 
                                 streamer=streamer, 
                                 max_new_tokens=self.config.max_new_tokens, 
                                 top_p=self.config.top_p, 
                                 do_sample=self.config.do_sample, 
                                 temperature=self.config.temperature
                                 )  
        
        # Starting the thread with the stream  
        thread = Thread(target=model.generate, kwargs=generation_kwargs)  
        thread.start()

    # retrieve the data from the queue and present it to the front end
    async def response_generator(self,model, tokenizer, streamer, message):  
        # Starting the generation process  
        self.start_generation(model, tokenizer, streamer, message)  
        # Infinite loop  
        while True:  
            # Retreiving the value from the queue  
            value = streamer._queue.get()  
            # Breaks if a stop signal is encountered  
            if value == None:  
                yield "data: [DONE]\n\n" # for EventSource in the frontend
                break
            # yields the value  
            yield f"data: {value}\n\n" # for EventSource in the frontend
            # provides a task_done signal once value yielded  
            streamer._queue.task_done()  
            # guard to make sure we are not extracting anything from   
            # empty queue
            await asyncio.sleep(0.05)
            
    class CustomStreamer(TextStreamer):  
        def __init__(self, queue, tokenizer, skip_prompt, **decode_kwargs) -> None:  
            super().__init__(tokenizer, skip_prompt, **decode_kwargs)  
            # Queue taken as input to the class  
            self._queue = queue  
            self.stop_signal=None  
            self.timeout = 1  

        def on_finalized_text(self, text: str, stream_end: bool = False):  
            # Instead of printing the text, we add the text into the queue  
            self._queue.put(text)  
            if stream_end:  
                # Similarly we add the stop signal also in the queue to   
                # break the stream  
                self._queue.put(self.stop_signal)