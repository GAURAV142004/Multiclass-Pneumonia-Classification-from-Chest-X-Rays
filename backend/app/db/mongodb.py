"""
MongoDB Connection and Database Utilities
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB connection manager"""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            
            # Test connection
            await self.client.admin.command('ping')
            
            self.db = self.client[settings.MONGODB_DB_NAME]
            
            logger.info(f"✓ Connected to MongoDB database: {settings.MONGODB_DB_NAME}")
            
            # Create indexes
            await self._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create database indexes"""
        try:
            # Users collection indexes
            await self.db.users.create_index("email", unique=True)
            await self.db.users.create_index("created_at")
            
            # Scan history collection indexes (if used)
            await self.db.scan_history.create_index("user_id")
            await self.db.scan_history.create_index("created_at")
            
            logger.info("Database indexes created")
            
        except Exception as e:
            logger.warning(f"Error creating indexes: {str(e)}")
    
    def get_collection(self, name: str):
        """Get a collection from the database"""
        return self.db[name]


# Global MongoDB instance
mongodb = MongoDB()


async def get_database():
    """Dependency to get database instance"""
    return mongodb.db
