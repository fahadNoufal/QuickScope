from QuickScope.components.data_generation import DataGeneration
from QuickScope.config.configuration import ConfigurationManager
from QuickScope.logger.custom_logger import logger


class DataGenerationPipeline:
    def __init__(self):
        config = ConfigurationManager()
        data_generation_config = config.get_data_generation_config()
        self.data_generation = DataGeneration(data_generation_config)
        logger.info("Data Generation Pipeline Started... ")
        
    
    async def init_connection(self):
        self.connection = await self.data_generation.init_connection()
        return self
    
    async def main(self,topic):
        data = await self.data_generation.fetch_data(topic)
        logger.info("Data Generation Pipeline Completed... ")
        return data
    
    async def close(self):
        logger.info("Data Generation(connection) Pipeline Closed... ")
        await self.connection.close()
        return True
    
    
async def main():
    dgp = DataGenerationPipeline()
    conn = await dgp.init_connection()
    data = await dgp.main(topic='Sports')
    logger.info(str(data))
    await dgp.close()
    
# import asyncio
# asyncio.run(main())