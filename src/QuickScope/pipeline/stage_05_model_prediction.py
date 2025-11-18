from QuickScope.components.model_prediction import ModelPrediction
from QuickScope.config.configuration import ConfigurationManager
from QuickScope.logger.custom_logger import logger
from queue import Queue

class PredictionPipeline:
    def __init__(self,):
        pass
    
    def main(self,model,tokenizer,message):
        prediction_config = ConfigurationManager().get_model_prediction_config()
        model_prediction = ModelPrediction(prediction_config)
        streamer_queue = Queue()  
        streamer = model_prediction.CustomStreamer(streamer_queue, tokenizer, True)  
        response_gen = model_prediction.response_generator(model, tokenizer, streamer, message)
        logger.info("Prediction Pipeline Exicuted...")
        return response_gen
        # streamer = CustomStreamer(streamer_queue, tokenizer, True)