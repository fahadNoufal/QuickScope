from QuickScope.entity import DataIngestionConfig
from QuickScope.utils.common import create_directories
from QuickScope.logger import custom_logger
from pathlib import Path
import pandas as pd


class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        self.config = data_ingestion_config

    def get_final_data(self) -> Path:
        # Generated Data
        input_df = pd.read_csv(self.config.input_data_path)
        # Output data generated through n8n
        summary_df = pd.read_csv(self.config.summary_data_path)

        input_df['output'] = summary_df['output']
        create_directories(self.config.root_dir)

        custom_logger.info("Data ingestion completed...")
        input_df.to_csv(self.config.out_dir_path)

        return self.config.out_dir_path

