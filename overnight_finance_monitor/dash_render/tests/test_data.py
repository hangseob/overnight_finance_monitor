import sys
import os
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 부모 디렉토리를 path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

logger.info(f"Current dir: {current_dir}")
logger.info(f"Adding parent dir to sys.path: {parent_dir}")

try:
    from data_manager import get_sp500_futures_at_time
    logger.info("Successfully imported get_sp500_futures_at_time from data_manager")
except ImportError as e:
    logger.error(f"Failed to import data_manager: {e}")
    sys.exit(1)

def test_fetch_48h_delayed_point():
    logger.info("Starting test: test_fetch_48h_delayed_point")
    target_time = datetime.now() - timedelta(hours=48)
    logger.info(f"Calculated Target Time (T-48h): {target_time}")
    
    try:
        point = get_sp500_futures_at_time(target_time)
        
        if point:
            logger.info(f"SUCCESS: Found data point: {point}")
            return True
        else:
            logger.warning("FAILED: Could not fetch data point for 48h ago.")
            
            # 주말인 경우를 대비해 72시간 전으로 시도
            alt_target = target_time - timedelta(hours=24)
            logger.info(f"Trying alternative target (72h ago): {alt_target}")
            point = get_sp500_futures_at_time(alt_target)
            if point:
                logger.info(f"SUCCESS with alternative: {point}")
                return True
            else:
                logger.error("FAILED even with alternative target.")
    except Exception as e:
        logger.error(f"Exception during test: {e}", exc_info=True)
            
    return False

if __name__ == "__main__":
    logger.info("Running data fetch test script...")
    if test_fetch_48h_delayed_point():
        logger.info("=== FINAL RESULT: TEST PASSED ===")
    else:
        logger.info("=== FINAL RESULT: TEST FAILED ===")
        sys.exit(1)
