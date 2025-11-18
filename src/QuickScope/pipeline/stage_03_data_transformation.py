from QuickScope.components.data_transformation import DataTransformation
from QuickScope.config.configuration import ConfigurationManager
from QuickScope.logger.custom_logger import logger


class DataTransformationPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_data_transformation_config()
    
    def main(self,topic,news):
        dataTransformar = DataTransformation(self.config)
            
        message = dataTransformar.get_message(topic,news)
        logger.info("Completed DataTransformation Pipeline...")
        return message