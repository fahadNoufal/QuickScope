from QuickScope.logger.custom_logger import logger
from QuickScope.entity import DataTransformationConfig



class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig):
        self.config = data_transformation_config

    def get_message(self,topic,news):

        sys_prompt = self.config.sys_prompt.replace("{topic}",topic)

        message = [
            {"role": "system", "content": sys_prompt },
            {"role": "user", "content": '\n\n'.join(news)}
        ]
        logger.info("Data transformation completed...")
        
        return message
    
    
    
    # For Model Training Dataset Creation
    def get_transformed_dataset(self):
        import pandas as pd

        df = pd.read_csv(self.config.input_data_path)
        
        def get_sys_prompt(topic):
            system_prompt = f'''You are given topic {topic} and top 3 relevant news headlines along with selected user comments
                            from multiple blog posts. Your task is to create a single, well-structured paragraph
                            that summarizes all key information in an informative, concise, and cohesive way.'''
            return system_prompt


        def make_conversation(row):
            return {
                'role':'system','content':get_sys_prompt(row['topic'])
            },{
                'role':'user','content':row['input']
            },{
                'role':'assistant','content':row['output']
            }

        df['conversation'] = df.apply(make_conversation,axis=1)
        df.to_csv(self.config.output_data_path)
        
        return self.config.output_data_path
    