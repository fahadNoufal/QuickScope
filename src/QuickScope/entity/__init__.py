from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir:Path
    summary_data_path:Path
    out_dir_path:Path
    input_data_path:Path

@dataclass(frozen=True)
class DataGenerationConfig:
    root_dir:Path
    sub_reddit:str
    sort:str
    time_filter:str
    limit:int
    out_dir_path:Path

@dataclass(frozen=True)
class DataTransformationConfig:
    sys_prompt:str
    input_data_path:Path
    output_data_path:Path
    
@dataclass(frozen=True)
class ModelFinetuningConfig:
    training_dataset:Path
    output_dir: Path
    finetuned_model_path: Path
    model_name: str
    max_seq_length: int
    device_map: str
    r: int
    lora_alpha: int
    lora_dropout: int
    bias: str
    use_gradient_checkpointing: str
    random_state: int
    use_rslora: bool
    loftq_config: bool
    
    per_device_train_batch_size: int
    gradient_accumulation_steps: int
    dataset_text_field: str
    warmup_steps: int
    num_train_epochs: int
    learning_rate: float
    logging_steps: int
    optim: str
    weight_decay: float
    lr_scheduler_type: str
    seed: int
    report_to: str
    
@dataclass(frozen=True)
class ModelPredictionConfig:
    model_path: Path
    tokenizer_path: Path
    device_map: str
    max_new_tokens: int
    top_p: float
    do_sample: True
    temperature: int