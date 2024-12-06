import json
import os
import redis.asyncio as redis
from typing import Optional, Dict
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LicenseManager:
    def __init__(self, redis_client: redis.Redis):
        """Redis クライアントの初期化"""
        self.redis_client = redis_client

    async def check_connection(self) -> dict:
        """Redisへの接続テスト"""
        try:
            is_connected = await self.redis_client.ping()
            if is_connected:
                logger.info("Redis connection successful")
                return {"status": "success", "message": "Redis connection successful"}
            else:
                raise ValueError("Redis ping failed")
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed: {str(e)}")
            raise ValueError(f"Redis connection failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during Redis connection check: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")

    async def validate_api_key(self, api_key: str) -> Optional[dict]:
        """APIキーの検証"""
        try:
            key = f"USER_PLAN:{api_key}"
            logger.debug(f"Validating API key: {key}")
            
            user_info_json = await self.redis_client.get(key)
            if not user_info_json:
                logger.warning(f"API key {api_key} not found in Redis.")
                raise ValueError("Invalid API key.")
            
            logger.info(f"API key {api_key} successfully validated.")
            return json.loads(user_info_json)

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error during API key validation: {str(e)}")
            raise ValueError(f"Redis connection error: {str(e)}")
        except redis.TimeoutError as e:
            logger.error(f"Redis operation timed out during API key validation: {str(e)}")
            raise ValueError(f"Redis operation timed out: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON for API key {api_key}: {str(e)}")
            raise ValueError(f"Invalid data format for API key: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during API key validation: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")

    async def add_license(self, api_key: str, user_info: dict):
        """ライセンスの追加"""
        try:
            key = f"USER_PLAN:{api_key}"
            logger.debug(f"Adding new license with key: {key}")
            
            if await self.redis_client.get(key):
                logger.warning(f"API key {api_key} already exists in Redis.")
                raise ValueError("API key already exists.")
            
            await self.redis_client.set(key, json.dumps(user_info))
            logger.info(f"License added successfully for API key {api_key}.")

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error during license addition: {str(e)}")
            raise ValueError(f"Redis connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during license addition: {str(e)}")
            raise ValueError(f"Failed to add license: {str(e)}")

    async def remove_license(self, api_key: str):
        """ライセンスの削除"""
        try:
            key = f"USER_PLAN:{api_key}"
            logger.debug(f"Removing license with key: {key}")
            
            if not await self.redis_client.exists(key):
                logger.warning(f"API key {api_key} does not exist in Redis.")
                raise ValueError("API key does not exist.")
            
            await self.redis_client.delete(key)
            logger.info(f"License removed successfully for API key {api_key}.")

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error during license removal: {str(e)}")
            raise ValueError(f"Redis connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during license removal: {str(e)}")
            raise ValueError(f"Failed to remove license: {str(e)}")


async def validate_license_key(api_key: str, license_manager: LicenseManager) -> dict:
    """
    APIキーの検証を行い、ユーザー情報を返す関数。

    Args:
        api_key (str): 検証するAPIキー。
        license_manager (LicenseManager): LicenseManagerのインスタンス。

    Returns:
        dict: ユーザー情報。

    Raises:
        ValueError: APIキーが無効な場合やその他のエラー。
    """
    logger.debug(f"Starting validation for API key: {api_key}")
    user_info = await license_manager.validate_api_key(api_key)
    if not user_info:
        logger.warning(f"Validation failed for API key: {api_key}")
        raise ValueError("Invalid API key.")
    
    logger.info(f"Validation successful for API key: {api_key}")
    return user_info
