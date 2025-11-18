# from QuickScope.entity import ModelFinetuningConfig
# from QuickScope.logger.custom_logger import logger


# from unsloth.chat_templates import get_chat_template, train_on_responses_only
# from unsloth.chat_templates import train_on_responses_only
# from unsloth import FastLanguageModel
# from trl import SFTTrainer, SFTConfig
# from datasets import Dataset

# import pandas as pd

# class ModelFinetuning:
#     def __init__(self,model_finetuning_config:ModelFinetuningConfig):
#         self.config = model_finetuning_config
        
#     def load_model(self):
#         model,tokenizer=FastLanguageModel.from_pretrained(
#             model_name=self.config.model_name,
#             load_in_4bit=True,
#             max_seq_length=self.config.max_seq_length,
#             dtype=None,
#             device_map=self.config.device_map
#         )
#         return model,tokenizer
        
#     def get_peft_model(self,model):
#         model = FastLanguageModel.get_peft_model(
#             model,
#             r=self.config.r,
#             target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
#                             "gate_proj", "up_proj", "down_proj"],

#             lora_alpha=self.config.lora_alpha,
#             lora_dropout=self.config.lora_dropout,
#             bias=self.config.bias,
#             use_gradient_checkpointing=self.config.use_gradient_checkpointing,
#             random_state = self.config.random_state,
#             use_rslora=self.config.use_rslora,
#             loftq_config=self.config.loftq_config
#         )
#         return model
    
#     def apply_chat_template(self,tokenizer):
        
#         df = pd.read_csv(self.config.training_dataset)
#         def apply_chat_template_custom(chat):
#             text = tokenizer.apply_chat_template(
#                 chat,
#                 tokenize=False,
#                 add_generation_prompt=False
#                 ).replace('<bos>','')
#             return text
#         df['text'] = df['conversation'].apply(apply_chat_template_custom)
        
#         return df
    
#     def train_model(self,model,tokenizer,training_dataset):
#         max_seq_length = 1024
#         trainer = SFTTrainer(
#             model=model,
#             tokenizer=tokenizer,
#             train_dataset=training_dataset,
#             max_seq_length = max_seq_length,
#             eval_dataset=None,
#             args=SFTConfig(
#                 per_device_train_batch_size=self.config.per_device_train_batch_size,
#                 gradient_accumulation_steps=self.config.gradient_accumulation_steps,
#                 dataset_text_field=self.config.dataset_text_field,
#                 warmup_steps=self.config.warmup_steps,
#                 num_train_epochs = self.config.num_train_epochs,
#                 # Set this for 1 full training run.
#                 learning_rate=self.config.learning_rate,
#                 logging_steps=self.config.logging_steps,
#                 optim=self.config.optim,
#                 weight_decay=self.config.weight_decay,
#                 lr_scheduler_type=self.config.lr_scheduler_type,
#                 seed=self.config.seed,
#                 output_dir=self.config.output_dir,
#                 report_to=self.config.report_to,
#             ),
#         )
#         trainer = train_on_responses_only(
#             trainer,
#             instruction_part = "<|start_header_id|>user<|end_header_id|>\n\n",
#             response_part = "<|start_header_id|>assistant<|end_header_id|>\n\n",
#         )
#         train_stats = trainer.train()
#         return trainer
    
#     def save_model(self,trainer,tokenizer):
#         trainer.save_model(self.config.output_dir)
#         tokenizer.save_pretrained(self.config.output_dir)
        
#         return self.config.output_dir