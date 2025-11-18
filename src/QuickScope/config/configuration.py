from QuickScope.constants import *
from QuickScope.utils.common import read_yaml,create_directories
from QuickScope.entity import DataIngestionConfig,DataGenerationConfig,DataTransformationConfig,ModelFinetuningConfig,ModelPredictionConfig
from QuickScope.logger.custom_logger import logger
from QuickScope.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH

class ConfigurationManager:
    def __init__(
            self,
            config_file_path = CONFIG_FILE_PATH,
            params_file_path = PARAMS_FILE_PATH
            ):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)

        
    def get_data_generation_config(self) -> DataGenerationConfig:
        config = self.config.data_generation

        data_generation_config = DataGenerationConfig(
            config.root_dir,
            config.sub_reddit,
            config.sort,
            config.time_filter,
            config.limit,
            config.out_dir_path,
        )
        logger.info("Data Generation Config Initialized...")
        return data_generation_config
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            dataset_path = config.dataset_path
        )
        logger.info("Data Ingestion Config Initialized...")
        return data_ingestion_config
    
    def get_data_transformation_config(self)->DataTransformationConfig:
        config = self.config.data_transformation
        data_transformation_config = DataTransformationConfig(
            sys_prompt = config.sys_prompt,
            input_data_path = config.input_data_path,
            output_data_path = config.output_data_path
        )
        logger.info("Data Transformation Config Initialized...")
        return data_transformation_config
    
    def get_model_finetuning_config(self)->ModelFinetuningConfig:
        config = self.config.model_finetuning
        params = self.params.model_finetuning
        model_finetuning_config = ModelFinetuningConfig(
            
            training_dataset=config.training_dataset,
            output_dir= config.output_dir,
            finetuned_model_path= config.finetuned_model_path,
            
            model_name=params.model_name,
            max_seq_length= params.max_seq_length,
            device_map= params.device_map,
            r= params.r,
            lora_alpha= params.lora_alpha,
            lora_dropout= params.lora_dropout,
            bias= params.bias,
            use_gradient_checkpointing= params.use_gradient_checkpointing,
            random_state= params.random_state,
            use_rslora= params.use_rslora,
            loftq_config= params.loftq_config,
            per_device_train_batch_size= params.per_device_train_batch_size,
            gradient_accumulation_steps= params.gradient_accumulation_steps,
            dataset_text_field= params.dataset_text_field,
            warmup_steps= params.warmup_steps,
            num_train_epochs= params.num_train_epochs,
            learning_rate= params.learning_rate,
            logging_steps= params.logging_steps,
            optim= params.optim,
            weight_decay= params.weight_decay,
            lr_scheduler_type= params.lr_scheduler_type,
            seed= params.seed,
            report_to= params.report_to,
        )
        logger.info("Model Finetuning Config Initialized...")
        return model_finetuning_config
    
    def get_model_prediction_config(self):
        config = self.config.prediction
        params = self.params.prediction
        
        model_prediction_config = ModelPredictionConfig(
            model_path = config.model_path,
            tokenizer_path = config.tokenizer_path,
            device_map = params.device_map,
            max_new_tokens = params.max_new_tokens,
            top_p = params.top_p,
            do_sample = params.do_sample,
            temperature = params.temperature
        )
        logger.info("Model Prediction Config Initialized...")
        return model_prediction_config