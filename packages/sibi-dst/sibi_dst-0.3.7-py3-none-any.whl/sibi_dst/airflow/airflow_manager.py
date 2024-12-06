import os
import fsspec
import httpx
from jinja2 import Template
from datetime import datetime, timedelta


class AirflowDAGManager:
    DAG_TEMPLATE = """
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime, timedelta

    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    with DAG(
        '{{ dag_id }}',
        default_args=default_args,
        description="{{ description }}",
        schedule_interval="{{ schedule_interval }}",
        start_date=datetime({{ start_year }}, {{ start_month }}, {{ start_day }}),
        catchup=False,
    ) as dag:
        {% for task in tasks %}
        {{ task }}
        {% endfor %}
    """

    def __init__(self, output_dir, airflow_dags_path, airflow_url, storage_backend="file", storage_config=None,
                 auth=None):
        """
        Initialize the Airflow DAG Manager.

        Args:
            output_dir (str): Local directory for storing generated DAGs.
            airflow_dags_path (str): Remote DAGs path (e.g., local path or S3 bucket).
            airflow_url (str): Base URL of the remote Airflow server (e.g., "http://airflow.example.com").
            storage_backend (str): Storage backend for fsspec (default: "file").
            storage_config (dict): Configuration for the storage backend.
            auth (tuple): Authentication tuple (username, password) for Airflow REST API.
        """
        self.output_dir = output_dir
        self.airflow_dags_path = airflow_dags_path
        self.airflow_url = airflow_url
        self.storage_backend = storage_backend
        self.storage_config = storage_config or {}
        self.auth = auth

        os.makedirs(self.output_dir, exist_ok=True)

    def generate_dag(self, dag_id, description, schedule_interval, tasks):
        """
        Generate an Airflow DAG Python script.

        Args:
            dag_id (str): Unique ID for the DAG.
            description (str): Description of the DAG.
            schedule_interval (str): Cron schedule for the DAG.
            tasks (list of str): Task definitions in PythonOperator format.

        Returns:
            str: Path to the generated DAG file.
        """
        template = Template(self.DAG_TEMPLATE)
        dag_script = template.render(
            dag_id=dag_id,
            description=description,
            schedule_interval=schedule_interval,
            start_year=datetime.now().year,
            start_month=datetime.now().month,
            start_day=datetime.now().day,
            tasks=tasks,
        )

        file_path = os.path.join(self.output_dir, f"{dag_id}.py")
        with open(file_path, "w") as f:
            f.write(dag_script)

        print(f"DAG for {dag_id} created at: {file_path}")
        return file_path

    def upload_dag(self, local_file):
        """
        Upload a DAG file to the remote Airflow server.

        Args:
            local_file (str): Path to the local DAG file.
        """
        try:
            remote_file_path = f"{self.airflow_dags_path}/{os.path.basename(local_file)}"
            fs = fsspec.filesystem(self.storage_backend, **self.storage_config)
            with open(local_file, "rb") as f:
                with fs.open(remote_file_path, "wb") as remote_f:
                    remote_f.write(f.read())
            print(f"Uploaded {local_file} to {remote_file_path}")
        except Exception as e:
            print(f"Error uploading {local_file}: {e}")
            raise

    def upload_all_dags(self, dag_files):
        """
        Upload multiple DAG files to the remote Airflow server.

        Args:
            dag_files (list of str): List of local DAG file paths.
        """
        for local_file in dag_files:
            self.upload_dag(local_file)

    def trigger_dag(self, dag_id, run_id=None, conf=None):
        """
        Trigger a DAG on the remote Airflow server.

        Args:
            dag_id (str): The ID of the DAG to trigger.
            run_id (str, optional): Custom run ID for the DAG run.
            conf (dict, optional): Additional configuration for the DAG run.

        Returns:
            dict: Response from the Airflow server.
        """
        url = f"{self.airflow_url}/api/v1/dags/{dag_id}/dagRuns"
        payload = {"dag_run_id": run_id or f"manual_{datetime.now().isoformat()}", "conf": conf or {}}
        try:
            response = httpx.post(url, json=payload, auth=self.auth)
            response.raise_for_status()
            print(f"DAG {dag_id} triggered successfully.")
            return response.json()
        except Exception as e:
            print(f"Error triggering DAG {dag_id}: {e}")
            raise

    def monitor_dag_run(self, dag_id, run_id):
        """
        Monitor a specific DAG run on the remote Airflow server.

        Args:
            dag_id (str): The ID of the DAG.
            run_id (str): The ID of the DAG run to monitor.

        Returns:
            dict: Status of the DAG run.
        """
        url = f"{self.airflow_url}/api/v1/dags/{dag_id}/dagRuns/{run_id}"
        try:
            response = httpx.get(url, auth=self.auth)
            response.raise_for_status()
            dag_run_status = response.json()
            print(f"DAG Run Status for {dag_id} - {run_id}: {dag_run_status}")
            return dag_run_status
        except Exception as e:
            print(f"Error monitoring DAG run {dag_id} - {run_id}: {e}")
            raise

    def monitor_all_dags(self):
        """
        Fetch and log the status of all DAGs on the remote Airflow server.

        Returns:
            dict: Status of all DAGs.
        """
        url = f"{self.airflow_url}/api/v1/dags"
        try:
            response = httpx.get(url, auth=self.auth)
            response.raise_for_status()
            all_dags = response.json()
            print("All DAGs fetched successfully.")
            return all_dags
        except Exception as e:
            print(f"Error monitoring all DAGs: {e}")
            raise

    def manage_dags(self, dag_definitions):
        """
        Generate, upload, and manage DAGs based on given definitions.

        Args:
            dag_definitions (list of dict): List of DAG definitions.
        """
        # Generate DAGs
        print("Generating DAGs...")
        dag_files = []
        for definition in dag_definitions:
            dag_files.append(
                self.generate_dag(
                    dag_id=definition["dag_id"],
                    description=definition["description"],
                    schedule_interval=definition["schedule_interval"],
                    tasks=definition["tasks"],
                )
            )

        # Upload DAGs
        print("Uploading DAGs...")
        self.upload_all_dags(dag_files)
        print("DAG management completed successfully.")