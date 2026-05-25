import os
import logging
from flask import Flask, jsonify, render_template
import redis

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

try:
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    cache.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.warning(f"Redis not available: {e}")
    cache = None

@app.route('/')
def home():
    logger.info("Home page visited")
    
    # Increment visit counter in Redis
    visits = 0
    if cache:
        visits = cache.incr('visit_count')  # incr = increment by 1, returns new value
    
    return render_template('index.html', visits=visits)

@app.route('/health')
def health():
    redis_status = 'connected'
    try:
        if cache:
            cache.ping()
        else:
            redis_status = 'unavailable'
    except Exception:
        redis_status = 'error'
    
    logger.info(f"Health check — Redis: {redis_status}")
    
    return jsonify({
        'status': 'healthy',
        'app': 'devops-flask-app',
        'redis': redis_status
    })

@app.route('/reset')
def reset():
    if cache:
        cache.set('visit_count', 0)
    return jsonify({'message': 'Counter reset to 0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)