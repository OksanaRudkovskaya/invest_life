import schedule

from src.tasks import (
    run_download_moex_data,
    run_generate_features,
    run_predict,
    prepare_message,
    send_message_to_telegram,
)
from src.utils import load_config, update_config, get_start_end_dates


config = load_config('config.yml')
TIME_START = config.get("orchestrator", {}).get("time_start")


def orchestrator_job():
    print("Starting orchestrator job...")
    global config

    config = load_config('config.yml')
    variables = load_config("src/resources/variables.yml")

    dwn_script_path = config.get("download_moex_data", {}).get("exe_path")
    dwn_script_interval = config.get("download_moex_data", {}).get("interval")
    dwn_start_date, dwn_end_date = get_start_end_dates(variables, "download_moex_data", "end_date")
    if dwn_start_date is None:
        return

    run_download_moex_data(dwn_script_path, dwn_script_interval, dwn_start_date, dwn_end_date)

    update_config("src/resources/variables.yml", "end_date", dwn_end_date, section="download_moex_data")

    python_executable = config.get("generate_features", {}).get("venv_path", "python")
    feature_service_script = config.get("generate_features", {}).get("script_path", "python")
    run_generate_features(python_executable, feature_service_script)

    python_executable_predict = config.get("predict_service", {}).get("venv_path", "python")
    predict_service_script = config.get("predict_service", {}).get("script_path", "python")
    run_predict(python_executable_predict, predict_service_script)

    message = prepare_message()
    print(message)
    url = config.get("send_message_to_telegram", {}).get("url")
    send_message_to_telegram(message, url)

    print("Finished orchestrator job.")


def main():
    import time

    schedule.every().day.at(TIME_START).do(orchestrator_job)
    # schedule.every(1).minutes.do(orchestrator_job)

    print("Orchestrator service started. Waiting for scheduled tasks...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()