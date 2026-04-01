import os
import shutil

class BucketAdapter:
    def __init__(self, storage_dir="artifacts"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def store_artifact(self, execution_id: str, local_filepath: str) -> str:
        """
        Stores the generated artifact to the persistent bucket/disk layer.
        Links the provided execution_id with the filename for metadata mapping.
        """
        if not os.path.exists(local_filepath):
            raise FileNotFoundError(f"Source artifact {local_filepath} does not exist.")
            
        filename = os.path.basename(local_filepath)
        destination_path = os.path.join(self.storage_dir, f"{execution_id}_{filename}")
        shutil.copy2(local_filepath, destination_path)
        return destination_path
