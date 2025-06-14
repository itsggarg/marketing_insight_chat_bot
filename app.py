"""
Marketing Insights Generator Application

A Flask-based web application that generates AI-powered marketing insights
from company data using Google's Gemini API.

Features:
- Multi-company support with dynamic configuration
- AI-powered marketing recommendations
- Conversation history management
- Customizable company backgrounds
- Database integration for data retrieval
"""

import os
import pandas as pd
import google.generativeai as genai
import mysql.connector
from flask import Flask, request, jsonify, render_template, redirect, url_for
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Company configuration
# Each company has a unique identifier, display name, database reference, and icon
COMPANY_CONFIG = {
    'company1': {
        'name': 'Company One',
        'db_env': 'MYSQL_DB_COMPANY1',
        'icon': '🛒'
    },
    'company2': {
        'name': 'Company Two',
        'db_env': 'MYSQL_DB_COMPANY2',
        'icon': '👔'
    },
    'company3': {
        'name': 'Company Three',
        'db_env': 'MYSQL_DB_COMPANY3',
        'icon': '🏗️'
    },
    'company4': {
        'name': 'Company Four',
        'db_env': 'MYSQL_DB_COMPANY4',
        'icon': '🥃'
    }
}

# Load configuration from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

# Configure Gemini API if key is available
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Failed to configure Gemini API: {e}")

# Global dictionary to store company managers
company_managers = {}


class CompanyDataManager:
    """
    Manages data and operations for a specific company.
    
    Attributes:
        company_id: Unique identifier for the company
        company_config: Configuration dictionary for the company
        mysql_db: Database name from environment variables
        background_manager: Manages company background information
        conversation_manager: Manages conversation history
        data_manager: Handles data loading and processing
    """
    
    def __init__(self, company_id):
        self.company_id = company_id
        self.company_config = COMPANY_CONFIG.get(company_id, {})
        self.mysql_db = os.getenv(self.company_config.get('db_env', ''))
        self.background_manager = BackgroundManager(self)
        self.conversation_manager = ConversationManager()
        self.data_manager = DataManager(self)
    
    def get_company_name(self):
        """Returns the display name of the company"""
        return self.company_config.get('name', 'Unknown Company')


class BackgroundManager:
    """
    Manages company background information used for context in AI responses.
    
    Features:
    - Loads initial background from database
    - Allows temporary edits to background
    - Can reset to original background
    """
    
    def __init__(self, company_manager):
        self.company_manager = company_manager
        self.original_background = self.load_background_from_database()
        self.current_background = self.original_background
        self.is_edited = False
    
    def load_background_from_database(self):
        """
        Loads company background information from the database.
        
        Returns:
            str: Background text or default message if not found
        """
        try:
            conn = mysql.connector.connect(
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=self.company_manager.mysql_db,
                unix_socket=f"/cloudsql/{INSTANCE_CONNECTION_NAME}",
                connect_timeout=15,
                autocommit=True
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `company-background`")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result and result[0]:
                return result[0]
            else:
                return f"No background information available for {self.company_manager.get_company_name()}"
        
        except Exception as e:
            return f"No background information available for {self.company_manager.get_company_name()}"
    
    def update_background(self, new_background):
        """
        Updates the current background with user-provided text.
        
        Args:
            new_background: New background text
            
        Returns:
            bool: True if update successful, False otherwise
        """
        if new_background and new_background.strip():
            self.current_background = new_background.strip()
            self.is_edited = True
            return True
        return False
    
    def reset_background(self):
        """Resets background to original version from database"""
        self.current_background = self.original_background
        self.is_edited = False
    
    def get_background(self):
        """Returns the current background text"""
        return self.current_background
    
    def get_background_info(self):
        """
        Returns comprehensive background information.
        
        Returns:
            dict: Contains current/original background, edit status, and character count
        """
        return {
            "current_background": self.current_background,
            "original_background": self.original_background,
            "is_edited": self.is_edited,
            "character_count": len(self.current_background)
        }


class ConversationManager:
    """
    Manages conversation history for contextual AI responses.
    
    Features:
    - Maintains conversation history with size limits
    - Provides relevant history based on current question
    - Tracks data context establishment
    """
    
    def __init__(self, max_history=8, max_tokens_per_turn=3000):
        self.history = []
        self.max_history = max_history
        self.max_tokens_per_turn = max_tokens_per_turn
        self.data_context_established = False
    
    def add_turn(self, question, answer):
        """
        Adds a question-answer pair to conversation history.
        
        Args:
            question: User's question
            answer: AI's response
        """
        clean_question = self._clean_question_from_data(question)
        truncated_answer = (answer[:self.max_tokens_per_turn] + "..."
                          if len(answer) > self.max_tokens_per_turn else answer)
        
        self.history.append((clean_question, truncated_answer))
        self.data_context_established = True
        
        # Remove oldest entry if history exceeds limit
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def _clean_question_from_data(self, question):
        """
        Extracts the actual user question from the full prompt.
        
        Args:
            question: Full prompt including context
            
        Returns:
            str: Cleaned user question
        """
        if "Current Question:" in question:
            parts = question.split("Current Question:")
            if len(parts) > 1:
                return parts[-1].strip()
        
        lines = question.split('\n')
        for line in reversed(lines):
            if line.strip() and not line.strip().startswith(('You are', 'Company', 'Data:', 'Background:')):
                return line.strip()
        
        return question[:200] + "..." if len(question) > 200 else question
    
    def get_relevant_history(self, current_question, max_relevant=3):
        """
        Retrieves conversation history relevant to the current question.
        
        Args:
            current_question: Current user question
            max_relevant: Maximum number of relevant entries to return
            
        Returns:
            list: Relevant (question, answer) pairs
        """
        if not self.history:
            return []
        
        # Extract keywords from current question
        keywords = set(word.lower() for word in current_question.split()
                      if len(word) > 3)
        
        # Score each history entry based on keyword matches
        scored_history = []
        for q, a in self.history:
            q_words = set(word.lower() for word in q.split() if len(word) > 3)
            score = len(keywords.intersection(q_words))
            scored_history.append((score, q, a))
        
        # Sort by relevance score
        scored_history.sort(key=lambda x: x[0], reverse=True)
        
        # Return most relevant entries
        relevant_history = []
        for score, q, a in scored_history[:max_relevant]:
            if score > 0 or len(relevant_history) < 1:
                relevant_history.append((q, a))
        
        return relevant_history
    
    def get_data_context_note(self):
        """Returns a note about data context if established"""
        if self.data_context_established:
            return "Note: The same complete dataset was provided in all previous exchanges."
        return ""
    
    def clear_history(self):
        """Clears all conversation history"""
        self.history = []
        self.data_context_established = False


class DataManager:
    """
    Manages data loading and processing for a company.
    
    Features:
    - Database connection testing
    - Data loading from MySQL
    - Error handling and reporting
    """
    
    def __init__(self, company_manager):
        self.company_manager = company_manager
        self.data = "Data unavailable - not yet loaded."
        self.raw_data_df = None
        self.initialization_attempted = False
        self.connection_error = None
    
    def test_database_connection(self):
        """
        Tests database connection and validates configuration.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Check for required environment variables
            if not all([MYSQL_USER, MYSQL_PASSWORD, self.company_manager.mysql_db, INSTANCE_CONNECTION_NAME]):
                missing = []
                if not MYSQL_USER: missing.append("MYSQL_USER")
                if not MYSQL_PASSWORD: missing.append("MYSQL_PASSWORD")
                if not self.company_manager.mysql_db: missing.append(f"MYSQL_DB for {self.company_manager.company_id}")
                if not INSTANCE_CONNECTION_NAME: missing.append("INSTANCE_CONNECTION_NAME")
                error_msg = f"Missing environment variables: {', '.join(missing)}"
                self.connection_error = error_msg
                return False
            
            # Attempt connection
            conn = mysql.connector.connect(
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=self.company_manager.mysql_db,
                unix_socket=f"/cloudsql/{INSTANCE_CONNECTION_NAME}",
                connect_timeout=15,
                autocommit=True
            )
            
            # Test with simple query
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            self.connection_error = None
            return True
        
        except mysql.connector.Error as e:
            error_msg = f"MySQL connection error for {self.company_manager.get_company_name()}: {e}"
            self.connection_error = error_msg
            return False
        except Exception as e:
            error_msg = f"Database connection test failed for {self.company_manager.get_company_name()}: {e}"
            self.connection_error = error_msg
            return False
    
    def get_engine(self):
        """
        Creates SQLAlchemy engine for database operations.
        
        Returns:
            Engine: SQLAlchemy engine instance
        """
        try:
            def get_conn():
                return mysql.connector.connect(
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    database=self.company_manager.mysql_db,
                    unix_socket=f"/cloudsql/{INSTANCE_CONNECTION_NAME}",
                    connect_timeout=15,
                    autocommit=True
                )
            return create_engine("mysql+mysqlconnector://", creator=get_conn)
        except Exception as e:
            raise
    
    def load_data(self):
        """
        Loads data from the database.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            # Test connection first
            if not self.test_database_connection():
                self.initialization_attempted = True
                return False
            
            engine = self.get_engine()
            
            # Check if table exists
            table_check_query = "SHOW TABLES LIKE 'scans'"
            table_exists = pd.read_sql(table_check_query, engine)
            
            if table_exists.empty:
                error_msg = f"Table 'scans' does not exist in database for {self.company_manager.get_company_name()}"
                self.data = error_msg
                self.initialization_attempted = True
                return False
            
            # Load data with row limit for performance
            query = "SELECT * FROM scans LIMIT 5000"
            data_df = pd.read_sql(query, engine)
            
            if data_df.empty:
                self.data = f"No data available in database table 'scans' for {self.company_manager.get_company_name()}."
                self.initialization_attempted = True
                return False
            
            # Convert to CSV format for AI processing
            self.data = data_df.to_csv(index=False)
            self.raw_data_df = data_df
            self.initialization_attempted = True
            self.connection_error = None
            return True
        
        except Exception as e:
            error_msg = f"Error loading data for {self.company_manager.get_company_name()}: {str(e)}"
            self.data = f"Data unavailable due to error: {str(e)[:200]}"
            self.connection_error = str(e)
            self.initialization_attempted = True
            return False
    
    def get_data_info(self):
        """
        Returns information about loaded data.
        
        Returns:
            dict: Data statistics and error information
        """
        if self.raw_data_df is not None:
            return {
                "total_records": len(self.raw_data_df),
                "columns": list(self.raw_data_df.columns),
                "connection_error": self.connection_error
            }
        return {
            "total_records": 0,
            "columns": [],
            "connection_error": self.connection_error
        }


# Helper Functions

def get_company_manager(company_id):
    """
    Retrieves or creates a company manager instance.
    
    Args:
        company_id: Unique company identifier
        
    Returns:
        CompanyDataManager: Manager instance or None if invalid ID
    """
    if company_id not in COMPANY_CONFIG:
        return None
    
    if company_id not in company_managers:
        company_managers[company_id] = CompanyDataManager(company_id)
        # Initialize data on first access
        company_managers[company_id].data_manager.load_data()
    
    return company_managers[company_id]


def create_efficient_prompt(current_data, current_background, user_prompt, conversation_manager):
    """
    Creates an optimized prompt for the AI model.
    
    Args:
        current_data: Company data in CSV format
        current_background: Company background information
        user_prompt: User's question
        conversation_manager: ConversationManager instance
        
    Returns:
        str: Complete prompt for AI model
    """
    relevant_history = conversation_manager.get_relevant_history(user_prompt)
    data_context_note = conversation_manager.get_data_context_note()
    
    # System instructions for AI behavior
    system_prompt = (
        "You are a professional marketing analyst specializing in data-driven strategies. "
        "Provide actionable, specific marketing recommendations based on the provided data. "
        "Focus on India and USA markets. Be concise and practical."
    )
    
    # Limit data size to prevent API errors
    if len(current_data) > 50000:  # Limit to ~50KB
        lines = current_data.split('\n')
        header = lines[0] if lines else ""
        data_sample = '\n'.join(lines[:500])  # First 500 rows
        data_section = f"Dataset Sample (showing first 500 records):\n{header}\n{data_sample}\n\n[Note: Full dataset contains more records but showing sample for analysis]"
    else:
        data_section = f"Complete Dataset:\n{current_data}"
    
    # Build conversation history section
    history_text = ""
    if relevant_history:
        history_text = "\n--- Previous Conversation Context ---\n"
        if data_context_note:
            history_text += f"{data_context_note}\n\n"
        
        for i, (q, a) in enumerate(relevant_history[-3:]):
            history_text += f"Previous Q{i+1}: {q}\nPrevious A{i+1}: {a}\n\n"
    
    # Construct final prompt
    final_prompt = (
        f"{system_prompt}\n\n"
        f"Company Background:\n{current_background}\n\n"
        f"{data_section}\n"
        f"{history_text}"
        f"Provide specific, actionable marketing recommendations."
        f"Current Question: {user_prompt}\n\n"
    )
    
    return final_prompt


def get_insights(prompt):
    """
    Generates insights using Google's Gemini AI model.
    
    Args:
        prompt: Complete prompt for the AI model
        
    Returns:
        str: AI-generated insights or error message
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API key is not configured."
    
    if not prompt or not isinstance(prompt, str):
        return "Error: Invalid prompt provided."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        response = model.generate_content(prompt)
        
        if response.parts and response.text:
            return response.text
        else:
            # Handle blocked responses
            feedback = getattr(response, 'prompt_feedback', None)
            if feedback and hasattr(feedback, 'block_reason'):
                return f"Response blocked: {feedback.block_reason}. Please rephrase your question."
            return "No response generated. Please try rephrasing your question."
    
    except Exception as e:
        # Handle various API errors gracefully
        error_str = str(e).lower()
        if "500" in error_str or "internal error" in error_str:
            return "Gemini API is temporarily unavailable. Please try again in a moment."
        elif "quota" in error_str or "limit" in error_str:
            return "API quota exceeded. Please try again later."
        elif "safety" in error_str:
            return "Response blocked for safety reasons. Please rephrase your question."
        else:
            return f"API error occurred. Please try again. ({str(e)[:50]}...)"


# Flask Routes

@app.route('/')
def index():
    """
    Main route - displays company selector or main interface.
    """
    company_id = request.args.get('id')
    
    # Show company selector if no ID provided
    if not company_id:
        return render_template('company-selector.html')
    
    # Validate company ID
    if company_id not in COMPANY_CONFIG:
        return redirect(url_for('index'))
    
    # Get company information
    company_info = COMPANY_CONFIG[company_id]
    
    return render_template('index.html', 
                         company_id=company_id,
                         company_name=company_info['name'],
                         company_icon=company_info['icon'])


@app.route('/get_background')
def get_background():
    """
    API endpoint to retrieve current background information.
    
    Returns:
        JSON: Background information or error
    """
    try:
        company_id = request.args.get('company_id')
        if not company_id:
            return jsonify({"error": "No company ID provided"}), 400
        
        company_manager = get_company_manager(company_id)
        if not company_manager:
            return jsonify({"error": "Invalid company ID"}), 400
        
        background_info = company_manager.background_manager.get_background_info()
        return jsonify(background_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_background', methods=['POST'])
def update_background():
    """
    API endpoint to update company background.
    
    Returns:
        JSON: Success message with updated info or error
    """
    try:
        company_id = request.json.get('company_id')
        if not company_id:
            return jsonify({"error": "No company ID provided"}), 400
        
        company_manager = get_company_manager(company_id)
        if not company_manager:
            return jsonify({"error": "Invalid company ID"}), 400
        
        new_background = request.json.get('background', '').strip()
        if not new_background:
            return jsonify({"error": "Background text cannot be empty."}), 400
        
        if len(new_background) > 2000:
            return jsonify({"error": "Background text too long. Please keep it under 2000 characters."}), 400
        
        success = company_manager.background_manager.update_background(new_background)
        if success:
            return jsonify({
                "message": "Background updated successfully.",
                "background_info": company_manager.background_manager.get_background_info()
            })
        else:
            return jsonify({"error": "Failed to update background."}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reset_background', methods=['POST'])
def reset_background():
    """
    API endpoint to reset background to original.
    
    Returns:
        JSON: Success message with reset info or error
    """
    try:
        company_id = request.json.get('company_id')
        if not company_id:
            return jsonify({"error": "No company ID provided"}), 400
        
        company_manager = get_company_manager(company_id)
        if not company_manager:
            return jsonify({"error": "Invalid company ID"}), 400
        
        company_manager.background_manager.reset_background()
        return jsonify({
            "message": "Background reset to original.",
            "background_info": company_manager.background_manager.get_background_info()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test')
def test_endpoint():
    """
    Test endpoint for system diagnostics.
    
    Returns:
        JSON: System status and configuration information
    """
    try:
        company_id = request.args.get('company_id')
        
        if company_id:
            # Company-specific test
            company_manager = get_company_manager(company_id)
            if not company_manager:
                return jsonify({"error": "Invalid company ID"}), 400
            
            db_test = company_manager.data_manager.test_database_connection()
            background_info = company_manager.background_manager.get_background_info()
            
            return jsonify({
                "status": "success",
                "company": company_manager.get_company_name(),
                "database_connection": db_test,
                "background_preview": background_info["current_background"][:100] + "..." 
                    if len(background_info["current_background"]) > 100 
                    else background_info["current_background"],
                "background_is_edited": background_info["is_edited"],
                "connection_error": company_manager.data_manager.connection_error,
                "data_info": company_manager.data_manager.get_data_info()
            })
        else:
            # General system test
            return jsonify({
                "status": "success",
                "companies_configured": list(COMPANY_CONFIG.keys()),
                "environment_variables": {
                    "MYSQL_USER": bool(MYSQL_USER),
                    "MYSQL_PASSWORD": bool(MYSQL_PASSWORD),
                    "INSTANCE_CONNECTION_NAME": bool(INSTANCE_CONNECTION_NAME),
                    "GEMINI_API_KEY": bool(GEMINI_API_KEY)
                }
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Main API endpoint for generating marketing insights.
    
    Returns:
        JSON: AI-generated insights and metadata
    """
    try:
        company_id = request.json.get('company_id')
        if not company_id:
            return jsonify({"error": "No company ID provided"}), 400
        
        company_manager = get_company_manager(company_id)
        if not company_manager:
            return jsonify({"error": "Invalid company ID"}), 400
        
        user_prompt = request.json.get('prompt', '').strip()
        custom_background = request.json.get('background', '').strip()
        
        if not user_prompt:
            return jsonify({"error": "No prompt provided."}), 400
        
        if len(user_prompt) > 500:
            return jsonify({"error": "Prompt too long. Please keep it under 500 characters."}), 400
        
        # Update background if provided
        if custom_background:
            company_manager.background_manager.update_background(custom_background)
        
        # Load data if not initialized
        if not company_manager.data_manager.initialization_attempted:
            company_manager.data_manager.load_data()
        
        # Get current background
        current_background = company_manager.background_manager.get_background()
        
        # Create prompt for AI
        full_prompt = create_efficient_prompt(
            company_manager.data_manager.data,
            current_background,
            user_prompt,
            company_manager.conversation_manager
        )
        
        # Generate insights
        insights = get_insights(full_prompt)
        
        # Add to conversation history if successful
        if not insights.startswith("Error:") and not insights.startswith("Response blocked"):
            company_manager.conversation_manager.add_turn(user_prompt, insights)
        
        # Prepare response
        data_info = company_manager.data_manager.get_data_info()
        background_info = company_manager.background_manager.get_background_info()
        
        response_data = {
            "insights": insights,
            "total_records": data_info["total_records"],
            "conversation_length": len(company_manager.conversation_manager.history),
            "background_info": background_info
        }
        
        # Add warning if database connection failed
        if data_info.get("connection_error"):
            response_data["warning"] = f"Database connection issue: {data_info['connection_error']}"
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/clear_history', methods=['POST'])
def clear_conversation():
    """
    API endpoint to clear conversation history.
    
    Returns:
        JSON: Success message or error
    """
    try:
        company_id = request.json.get('company_id')
        if not company_id:
            return jsonify({"error": "No company ID provided"}), 400
        
        company_manager = get_company_manager(company_id)
        if not company_manager:
            return jsonify({"error": "Invalid company ID"}), 400
        
        company_manager.conversation_manager.clear_history()
        return jsonify({"message": "Conversation history cleared."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error Handlers

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({"error": "Internal server error occurred."}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found."}), 404


if __name__ == "__main__":
    # Run the application
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
