from dataclasses import dataclass
from typing import Dict, Optional
import json
import os

from nema.connectivity import ConnectivityManager, CONNECTIVITY_CONFIG

from .data import Data


@dataclass
class DataCollection:
    items: Dict[str, Data]

    def __getattr__(self, item_id: str):
        try:
            return self.items[item_id]
        except KeyError:
            raise AttributeError(
                f"This DataCollection object has no attribute '{item_id}'"
            )

    def sync_data_from_API(self, job_id: Optional[str] = None):
        # Sync data from the API

        # Retrieve commit ID to ensure that all the data uses the same commit ID
        conn_manager = ConnectivityManager()
        latest_commit_id = conn_manager.get_latest_commit()

        input_fldr = f"{CONNECTIVITY_CONFIG.nema_data_folder}/input/{job_id}"

        os.makedirs(input_fldr, exist_ok=True)

        for item in self.items.values():
            item.sync_from_API(
                connectivity_manager=conn_manager,
                input_folder=input_fldr,
                commit_id=latest_commit_id,
            )

    def save_updates_locally(self, job_id: str):
        # Process updates

        # find which items have been used
        filtered_input_data = filter(
            lambda x: x.cache_info.number_of_times_hit > 0,
            self.items.values(),
        )

        # find which items have been updated
        filtered_output_data = filter(lambda x: x.is_updated, self.items.values())

        # output data to folder
        folder = os.path.join(f"{CONNECTIVITY_CONFIG.nema_data_folder}/output", job_id)
        os.makedirs(folder, exist_ok=True)

        data_output_folder = os.path.join(folder, "data-output")
        os.makedirs(data_output_folder, exist_ok=True)

        raw_data = [
            *[("used_data", data.global_id) for data in filtered_input_data],
            *[
                (
                    "updated_data",
                    json.dumps(
                        data.process_output_data(destination_folder=data_output_folder)
                    ),
                )
                for data in filtered_output_data
            ],
        ]

        output_file = os.path.join(folder, "output.json")
        with open(output_file, "w") as f:
            f.write(json.dumps(raw_data))

        # write to terminal the output file location
        print(f"Nema output written to folder: {folder}")

    def close(self):
        for item in self.items.values():
            item.close()
