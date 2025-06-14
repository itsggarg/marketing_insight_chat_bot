/**
 * Marketing Insights Bot - Client-side JavaScript
 * Handles user interactions, API calls, and UI updates
 */

// DOM element references
const form = document.getElementById('prompt-form');
const input = document.getElementById('prompt-input');
const chatBox = document.getElementById('chat-box');
const stopButton = document.getElementById('stop-button');
const sendBtn = document.getElementById('send-btn');
const clearHistoryBtn = document.getElementById('clear-history-btn');
const backgroundBtn = document.getElementById('background-btn');

// Background management elements
const backgroundSection = document.getElementById('background-section');
const backgroundDisplay = document.getElementById('background-display');
const backgroundEditor = document.getElementById('background-editor');
const editBackgroundBtn = document.getElementById('edit-background-btn');
const saveBackgroundBtn = document.getElementById('save-background-btn');
const cancelBackgroundBtn = document.getElementById('cancel-background-btn');
const resetBackgroundBtn = document.getElementById('reset-background-btn');
const backgroundStatus = document.getElementById('background-status');
const characterCount = document.getElementById('character-count');

// Application state
let currentTypingController = null;
let isProcessing = false;
let currentBackgroundInfo = null;
let originalBackgroundText = '';

// Get company ID from window object (set by template)
const COMPANY_ID = window.COMPANY_ID || '';

/**
 * Initialize application on page load
 */
window.addEventListener('DOMContentLoaded', async () => {
  await loadBackgroundInfo();
  
  // Show welcome message if chat is empty
  if (chatBox.children.length === 0) {
    const welcomeMessage = "**Welcome!** I am your marketing strategy assistant. " +
                          "I have access to your company data and can provide insights on " +
                          "branding, market expansion, and strategic recommendations.";
    addMessage(marked.parse(welcomeMessage), 'bot');
  }
});

/**
 * Load company background information from server
 */
async function loadBackgroundInfo() {
  try {
    const response = await fetch(`/get_background?company_id=${COMPANY_ID}`);
    if (response.ok) {
      currentBackgroundInfo = await response.json();
      updateBackgroundDisplay();
    }
  } catch (error) {
    console.error('Error loading background:', error);
  }
}

/**
 * Update the background display with current information
 */
function updateBackgroundDisplay() {
  if (!currentBackgroundInfo) return;
  
  backgroundDisplay.textContent = currentBackgroundInfo.current_background;
  backgroundEditor.value = currentBackgroundInfo.current_background;
  
  // Update status indicator
  if (currentBackgroundInfo.is_edited) {
    backgroundStatus.textContent = '✏️ Edited';
    backgroundStatus.style.color = '#17a2b8';
  } else {
    backgroundStatus.textContent = '📄 Original';
    backgroundStatus.style.color = '#28a745';
  }
  
  updateCharacterCount();
}

/**
 * Update character count display for background editor
 */
function updateCharacterCount() {
  const count = backgroundEditor.value.length;
  const maxCount = 2000;
  characterCount.textContent = `${count}/${maxCount} characters`;
  
  // Apply warning/error styling based on count
  if (count > maxCount * 0.9) {
    characterCount.className = 'character-error';
  } else if (count > maxCount * 0.8) {
    characterCount.className = 'character-warning';
  } else {
    characterCount.className = '';
  }
}

/**
 * Add a message to the chat interface
 * @param {string} htmlText - Message content (HTML)
 * @param {string} sender - Message sender ('user', 'bot', or null for system)
 * @param {boolean} isSystem - Whether this is a system message
 */
function addMessage(htmlText, sender, isSystem = false) {
  const messageDiv = document.createElement('div');
  
  if (isSystem) {
    messageDiv.className = 'system-message';
    messageDiv.innerHTML = htmlText;
  } else {
    messageDiv.className = `chat-message ${sender}`;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    
    if (sender === 'user') {
      bubble.textContent = htmlText;
    } else {
      bubble.innerHTML = htmlText;
    }
    
    messageDiv.appendChild(bubble);
  }
  
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Add an error message to the chat
 * @param {string} errorText - Error message text
 */
function addErrorMessage(errorText) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'error-message';
  messageDiv.textContent = `❌ ${errorText}`;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Animate typing effect for bot responses
 * @param {string} fullMarkdown - Complete markdown text to type
 * @param {HTMLElement} element - Element to update with typed text
 * @param {number} msPerChar - Milliseconds per character
 * @returns {Object} Controller object with cancel method
 */
function typeMarkdownText(fullMarkdown, element, msPerChar = 10) {
  let currentTypedIndex = 0;
  const startTime = Date.now();
  let timeoutId;
  let lastRenderedHTML = '';
  let stopped = false;

  stopButton.style.display = 'inline-block';

  function type() {
    if (stopped) return;

    const elapsedTime = Date.now() - startTime;
    const targetTypedIndex = Math.min(Math.floor(elapsedTime / msPerChar), fullMarkdown.length);

    if (targetTypedIndex > currentTypedIndex) {
      currentTypedIndex = targetTypedIndex;
      const currentTextChunk = fullMarkdown.substring(0, currentTypedIndex);
      const newHTML = marked.parse(currentTextChunk);
      
      // Only update DOM if HTML changed
      if (newHTML !== lastRenderedHTML || currentTypedIndex === fullMarkdown.length) {
        element.innerHTML = newHTML;
        lastRenderedHTML = newHTML;

        // Auto-scroll if near bottom
        const nearBottom = chatBox.scrollHeight - chatBox.scrollTop <= chatBox.clientHeight + 50;
        if (nearBottom) chatBox.scrollTop = chatBox.scrollHeight;
      }
    }

    if (currentTypedIndex < fullMarkdown.length) {
      timeoutId = setTimeout(type, Math.max(5, msPerChar / 2));
    } else {
      finish();
    }
  }

  function cancel() {
    stopped = true;
    clearTimeout(timeoutId);
    stopButton.style.display = 'none';
    currentTypingController = null;
    setProcessingState(false);
  }

  function finish() {
    stopButton.style.display = 'none';
    currentTypingController = null;
    setProcessingState(false);
  }

  type();
  return { cancel };
}

/**
 * Set the processing state of the application
 * @param {boolean} processing - Whether currently processing
 */
function setProcessingState(processing) {
  isProcessing = processing;
  sendBtn.disabled = processing;
  input.disabled = processing;
  
  if (processing) {
    sendBtn.innerHTML = '<span class="spinner"></span>Processing...';
  } else {
    sendBtn.textContent = 'Send';
  }
}

/**
 * Exit background edit mode and restore display
 */
function exitEditMode() {
  backgroundDisplay.style.display = 'block';
  backgroundEditor.style.display = 'none';
  editBackgroundBtn.style.display = 'inline-block';
  saveBackgroundBtn.style.display = 'none';
  cancelBackgroundBtn.style.display = 'none';
}

// Event Listeners

// Toggle background section visibility
backgroundBtn.addEventListener('click', () => {
  backgroundSection.style.display = backgroundSection.style.display === 'none' ? 'block' : 'none';
});

// Enter background edit mode
editBackgroundBtn.addEventListener('click', () => {
  originalBackgroundText = backgroundEditor.value;
  backgroundDisplay.style.display = 'none';
  backgroundEditor.style.display = 'block';
  editBackgroundBtn.style.display = 'none';
  saveBackgroundBtn.style.display = 'inline-block';
  cancelBackgroundBtn.style.display = 'inline-block';
  backgroundEditor.focus();
});

// Save background changes
saveBackgroundBtn.addEventListener('click', async () => {
  const newBackground = backgroundEditor.value.trim();
  
  if (!newBackground) {
    addErrorMessage('Background cannot be empty');
    return;
  }
  
  if (newBackground.length > 2000) {
    addErrorMessage('Background too long. Please keep it under 2000 characters.');
    return;
  }
  
  try {
    const response = await fetch('/update_background', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        background: newBackground,
        company_id: COMPANY_ID
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      currentBackgroundInfo = data.background_info;
      updateBackgroundDisplay();
      exitEditMode();
      addMessage('✅ Background updated successfully', null, true);
    } else {
      addErrorMessage(data.error || 'Failed to update background');
    }
  } catch (error) {
    addErrorMessage('Error updating background: ' + error.message);
  }
});

// Cancel background edit
cancelBackgroundBtn.addEventListener('click', () => {
  backgroundEditor.value = originalBackgroundText;
  updateCharacterCount();
  exitEditMode();
});

// Reset background to original
resetBackgroundBtn.addEventListener('click', async () => {
  if (!confirm('Reset background to original from database?')) return;
  
  try {
    const response = await fetch('/reset_background', { 
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_id: COMPANY_ID })
    });
    const data = await response.json();
    
    if (response.ok) {
      currentBackgroundInfo = data.background_info;
      updateBackgroundDisplay();
      addMessage('🔄 Background reset to original', null, true);
    } else {
      addErrorMessage(data.error || 'Failed to reset background');
    }
  } catch (error) {
    addErrorMessage('Error resetting background: ' + error.message);
  }
});

// Update character count on input
backgroundEditor.addEventListener('input', updateCharacterCount);

// Stop typing animation
stopButton.addEventListener('click', () => {
  if (currentTypingController) {
    currentTypingController.cancel();
  }
});

// Handle form submission
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const prompt = input.value.trim();
  if (!prompt || isProcessing) return;

  setProcessingState(true);
  addMessage(prompt, 'user');
  input.value = '';
  input.style.height = 'auto';

  // Add loading message
  const botMessageDiv = document.createElement('div');
  botMessageDiv.className = 'chat-message bot';
  const botBubble = document.createElement('div');
  botBubble.className = 'bubble loading-dots';
  botMessageDiv.appendChild(botBubble);
  chatBox.appendChild(botMessageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    // Prepare request body
    const requestBody = { 
      prompt,
      company_id: COMPANY_ID
    };
    
    // Include edited background if applicable
    if (currentBackgroundInfo && currentBackgroundInfo.is_edited) {
      requestBody.background = currentBackgroundInfo.current_background;
    }
    
    // Send request to server
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      let errorMsg = `HTTP error! Status: ${response.status}`;
      try {
        const errData = await response.json();
        errorMsg = errData.error || errData.message || errorMsg;
      } catch {
        errorMsg = response.statusText || errorMsg;
      }
      throw new Error(errorMsg);
    }

    const data = await response.json();

    // Remove loading animation
    botBubble.classList.remove('loading-dots');
    botBubble.innerHTML = '';

    if (data.insights) {
      // Cancel any existing typing animation
      if (currentTypingController) currentTypingController.cancel();
      
      // Start typing animation for response
      currentTypingController = typeMarkdownText(data.insights, botBubble, 10);
      
      // Update background info if provided
      if (data.background_info) {
        currentBackgroundInfo = data.background_info;
        updateBackgroundDisplay();
      }
    } else if (data.error) {
      botBubble.textContent = `❌ ${data.error}`;
      setProcessingState(false);
    } else {
      botBubble.textContent = "Unexpected response format.";
      setProcessingState(false);
    }
  } catch (err) {
    console.error("Fetch error:", err);
    botBubble.classList.remove('loading-dots');
    botBubble.textContent = `❌ Error: ${err.message}`;
    stopButton.style.display = 'none';
    setProcessingState(false);
  }
});

// Clear conversation history
clearHistoryBtn.addEventListener('click', async () => {
  if (isProcessing) return;
  
  try {
    const response = await fetch('/clear_history', { 
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_id: COMPANY_ID })
    });
    const data = await response.json();
    
    if (response.ok) {
      addMessage(`🗑️ ${data.message}`, null, true);
    } else {
      addErrorMessage('Failed to clear history');
    }
  } catch (error) {
    addErrorMessage('Error clearing history: ' + error.message);
  }
});

// Auto-resize textarea based on content
input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = (input.scrollHeight) + 'px';
});
