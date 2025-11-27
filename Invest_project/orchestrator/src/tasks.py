import subprocess
import json
import os
import requests



def run_download_moex_data(script_path: str, interval: str, from_dt: str, to_dt: str):
    print(f'Downloading moex data from {from_dt} to {to_dt}')
    try:
        result = subprocess.run(
            [
                script_path,
                "--interval", interval,
                "--from", from_dt,
                "--till", to_dt,
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("MOEX data downloaded successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while downloading MOEX data:")
        print(e.stderr)


def run_generate_features(python_executable: str, feature_service_script: str):
    try:
        result = subprocess.run(
            [str(python_executable), str(feature_service_script)],
            check=True,
            capture_output=True,
            text=True
        )
        print("Features generated successfully.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error while generating features:")
        print(e.stderr)
        return None


def run_predict(python_executable: str, predict_service_script: str):
    try:
        result = subprocess.run(
            [str(python_executable), str(predict_service_script)],
            check=True,
            capture_output=True,
            text=True
        )
        print("Predict successfully.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error in prediction:")
        print(e.stderr)
        return None


def prepare_message(input_path: str = "src/resources/preds.json") -> str:

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Файл {input_path} не найден.")

    message = "📈 Прогнозы по акциям на сегодня:\n\n"

    lines = open(input_path, 'r', encoding='utf-8').readlines()

    for line in lines:
        line = line.replace('\n', '').strip()

        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка разбора JSON в строке: {line}. Ошибка: {e}")

        ticker = data.get("ticker", "Неизвестный тикер")
        prediction = data.get("prediction")
        proba = data.get("proba", [])

        classes = {
            0: "падение",
            1: "боковое движение",
            2: "рост"
        }
        trend = classes.get(prediction, "неизвестно")

        if len(proba) >= 3:
            fall_prob, sideways_prob, rise_prob = [round(p * 100, 2) for p in proba]

            message += (
                f"🔹 {ticker}: прогноз — {trend}\n"
                f"   - Рост: {rise_prob}%\n"
                f"   - Падение: {fall_prob}%\n"
                f"   - Боковое движение: {sideways_prob}%\n\n"
            )
        else:
            message += f"🔹 {ticker}: недостаточно данных для отображения вероятностей.\n\n"
    return message


def send_message_to_telegram(message: str, url: str)-> dict:

    headers = {
    "Content-Type": "application/json",
    "Authorization": "kjld12lAnbP_pej"
    }

    payload = {
    "message": message
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Ошибка] Не удалось отправить запрос: {e}")
        return {"error": str(e)}



# def send_message_to_kafka(message, topic, server, user, password, ssl_path):
#     producer = KafkaProducer(
#         bootstrap_servers=[server],
#         security_protocol="SASL_SSL",
#         sasl_mechanism="SCRAM-SHA-512",
#         sasl_plain_username=user,
#         sasl_plain_password=password,
#         ssl_cafile=ssl_path)
#
#     try:
#         producer.send(topic, message)
#         producer.flush()
#         print("Message sent to Kafka successfully.")
#     except Exception as e:
#         print("Error while sending message to Kafka:")
#         print(e)
#     finally:
#         producer.close()


