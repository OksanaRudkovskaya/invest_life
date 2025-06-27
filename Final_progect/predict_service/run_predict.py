import json

from Final_progect.predict_service.model.predict_service import PredictService
from Final_progect.predict_service.src.predict.models import DataItem, PredictTicker


def main():
    output = r'../orchestrator/src/resources/output.json'
    result_file = r'../orchestrator/src/resources/preds.json'

    data = json.loads(open(output, 'r').read())

    predictor = PredictService()

    results = []
    for row in data.get('data'):
        item = DataItem(ticker=row['ticker'], vectors=row['vectors'])
        preds, probs = predictor.predict_last_row(item)
        if preds is None:
            continue
        results.append(
            PredictTicker(
                ticker=row['ticker'],
                prediction=preds,
                proba=probs
            )
        )

    with open(result_file, 'w') as f:
        for r in results:
            f.write(json.dumps(r.__dict__) + '\n')


if __name__ == '__main__':
    main()