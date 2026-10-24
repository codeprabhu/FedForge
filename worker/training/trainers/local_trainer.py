import time
import torch # type: ignore
import torch.nn as nn # type: ignore
from typing import cast

from training.results.training_result import TrainingResult
from training.trainers.base_trainer import BaseTrainer
from serialization.model_weights import ModelWeights

class LocalTrainer(BaseTrainer):
    def train(self, dataset, model, config, pretrained_weights = None):
        dataloader, num_samples = dataset.get_dataloader(
            config.partition_id,config.total_partitions, config.batch_size)
        
        model = model.build()
        if pretrained_weights is not None:
            model.load_state_dict(ModelWeights(cast(dict[str,list],pretrained_weights)).to_state_dict())
        criterion = nn.BCEWithLogitsLoss()

        optimizer = torch.optim.Adam(
            model.parameters(), lr = config.learning_rate)

        start_time = time.time()
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for epoch in range (config.epochs):
            for features, labels in dataloader:
                optimizer.zero_grad()
                outputs = model(features)

                outputs = outputs.squeeze(1)
                loss = criterion(outputs, labels)

                loss.backward()
                optimizer.step()
                running_loss += loss.item() * labels.size(0)

                predictions = torch.sigmoid(outputs)
                predictions = (predictions >=0.5).float()

                correct += (predictions== labels).sum().item()
                total += labels.size(0)
            
        training_time = time.time() - start_time
        accuracy = correct/total if total > 0 else 0.0
        average_loss = (running_loss / total) if total > 0 else 0.0
        model_weights = ModelWeights.from_state_dict(model.state_dict())

        return TrainingResult(
                accuracy= accuracy,
                loss = average_loss,
                epochs= config.epochs,
                num_samples= num_samples,
                training_time_seconds= training_time,
                model_weights = model_weights
            )
