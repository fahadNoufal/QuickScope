# from QuickScope.logger.custom_logger import logger
from src.QuickScope.logger.custom_logger import logger
from src.QuickScope.pipeline.stage_01_data_generation import DataGenerationPipeline
# from src.QuickScope.pipeline.stage_02_data_ingestion import DataIngestionPipeline
from src.QuickScope.pipeline.stage_03_data_transformation import DataTransformationPipeline
# from src.QuickScope.pipeline.stage_04_model_finetuning import ModelFinetuningPipeline

STAGE_NAME = 'DATA GENERATION'
try:
    data_generation_pipeline = DataGenerationPipeline()
    # data_path = data_generation_pipeline.main()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


# STAGE_NAME = 'DATA INGESTION'
# try:
#     data_ingestion_pipeline = DataIngestionPipeline()
#     # data_path = data_ingestion_pipeline.main()
#     logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#     logger.exception(e)
#     raise e

STAGE_NAME = 'DATA TRANSFORMATION'
try:
    data_transformation_pipeline = DataTransformationPipeline()
    # data_path = data_transformation_pipeline.main()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

# STAGE_NAME = 'MODEL FINETUNING'
# try:
#     model_finetuning_pipeline = DataIngestionPipeline()
#     data_path = model_finetuning_pipeline.main()
#     logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#     logger.exception(e)
#     raise e