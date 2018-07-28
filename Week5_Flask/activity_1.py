from flask import Flask
import pandas as pd
app = Flask(__name__)


@app.route('/demographic_statistics')
def demographic_statistics():
    df = pd.read_csv("Demographic_Statistics_By_Zip_Code.csv")
    json = df.T.to_json()
    return 'Hello, World!'


if __name__ == "__main__":
    app.run()
