from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Validate database URL
if not SQLALCHEMY_DATABASE_URL:
    print("⚠️  SQLALCHEMY_DATABASE_URL environment variable is not set")
    # Create a dummy engine for development/testing
    engine = None
    SessionLocal = None
else:
    print(f"🔗 Database URL: {SQLALCHEMY_DATABASE_URL[:50]}...")
    
    try:
        # Create engine with additional parameters for better connection handling
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_pre_ping=True,  # Enable connection health checks
            pool_recycle=300,    # Recycle connections after 5 minutes
            pool_size=10,        # Set pool size
            max_overflow=20      # Allow up to 20 additional connections
        )
        print("✅ Database engine created successfully")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
    except Exception as e:
        print(f"❌ Error creating database engine: {e}")
        engine = None
        SessionLocal = None

Base = declarative_base()

# Dependency to get DB session
def get_db():
    if SessionLocal is None:
        raise Exception("Database not configured. Please check SQLALCHEMY_DATABASE_URL environment variable.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def init_db():
    if engine is None:
        print("⚠️  Cannot initialize database - engine not available")
        return
    
    try:
        from models import User, Email, Session  # Import models here to avoid circular imports
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise 