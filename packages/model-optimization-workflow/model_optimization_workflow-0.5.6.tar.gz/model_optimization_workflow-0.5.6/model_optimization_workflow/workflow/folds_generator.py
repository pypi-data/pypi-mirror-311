import os
import shutil
from datetime import datetime, timedelta

from market_data_assembler.common.common import prepare_directory


class FoldsGenerator:
    def __init__(self, config, n_folds, run_directory, datasets_path):
        self.n_folds = n_folds
        self.datasets_path = datasets_path
        self.run_directory = run_directory
        self.folds_directory = os.path.join(self.run_directory, 'folds')
        prepare_directory(self.folds_directory)
        self.config = config
        self.day_from = int(self.config['assembler']['day_from'].timestamp() * 1000)
        self.day_to = int((self.config['assembler']['day_to'] + timedelta(days=1)).timestamp() * 1000)

    def generate(self):
        total_time = self.day_to - self.day_from
        fold_time_window = total_time // self.n_folds

        all_files = [f for f in os.listdir(self.datasets_path) if f.endswith('.json')]
        dataset_size = len(all_files)
        folds = []

        for i in range(self.n_folds):
            fold_start = self.day_from + fold_time_window * i
            fold_end = fold_start + fold_time_window
            fold_path = os.path.join(self.folds_directory, f'{i}')
            os.makedirs(fold_path, exist_ok=True)

            dataset_count = 0
            for filename in all_files:
                file_path = os.path.join(self.datasets_path, filename)
                t_from = int(filename.split('_')[1].split('.')[0])

                if fold_start <= t_from < fold_end:
                    fold_file_path = os.path.join(fold_path, filename)
                    shutil.copy(file_path, fold_file_path)
                    dataset_count += 1

            folds.append(dataset_count)

        print(
            f"process-{os.getpid()}, time: {datetime.now()}, total dataset size: {dataset_size}, Number of folds: {self.n_folds}, Datasets sizes in folds: {folds}"
        )

        if any(count == 0 for count in folds):
            raise ValueError(
                f"process-{os.getpid()}, time: {datetime.now()}, One or more folds are empty. Dataset allocation in folds: {folds}")
