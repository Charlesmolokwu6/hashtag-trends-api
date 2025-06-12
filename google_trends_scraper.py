from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/get_trends', methods=['POST'])
def get_trends():
    data = request.get_json()
    niche = data.get('niche')

    if not niche:
        return jsonify({'error': 'Niche is required'}), 400

    try:
        kw_list = [niche]
        pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d')
        related = pytrends.related_queries()
        top_related = related[niche]['top']

        if top_related is None:
            return jsonify({'trends': []})

        trends = top_related['query'].tolist()[:10]
        return jsonify({'trends': trends})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

