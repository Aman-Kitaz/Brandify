document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const logoPreview = document.getElementById('logoPreview');
    const generatedLogo = document.getElementById('generatedLogo');
    const downloadLogoButton = document.getElementById('downloadLogoButton');

    let conversationId = null;
    let currentStage = 'initial';
    let brandDetails = {};

    // Function to add a message to the chat
    function addMessage(message, sender = 'assistant') {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Start the conversation
    function startConversation() {
        fetch('/start_conversation', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                conversationId = data.conversation_id;
                addMessage(data.message);
            })
            .catch(error => {
                console.error('Error starting conversation:', error);
                addMessage('Failed to start conversation. Please refresh the page.');
            });
    }

    // Process user response
    function processResponse(userResponse) {
        console.log('Processing response:', userResponse);
        console.log('Current stage:', currentStage);

        fetch('/process_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                user_response: userResponse
            })
        })
        .then(response => response.json())
        .then(data => {
            // Always add user's response to chat
            addMessage(userResponse, 'user');
            
            // Handle different stages
            if (data.stage === 'brand_name_input') {
                // Store brand name
                brandDetails['brand_name'] = userResponse;
            }
            else if (data.stage === 'prompt_input') {
                // Store custom prompt
                brandDetails['custom_prompt'] = userResponse;
            }
            
            // Handle different response types
            if (data.suggestions) {
                // Brand name suggestions stage
                let suggestionsText = "Here are brand name suggestions:\n";
                data.suggestions.forEach(suggestion => {
                    suggestionsText += suggestion + "\n";
                });
                addMessage(suggestionsText);
            } 
            else if (data.question) {
                // Multiple choice question stage
                let optionsText = `${data.question}\n`;
                data.options.forEach((option, index) => {
                    optionsText += `${index + 1}. ${option}\n`;
                });
                addMessage(optionsText);
            } 
            else if (data.next_step === 'generate_logo') {
                // Logo generation stage
                addMessage('Preparing to generate your logo...');
                generateLogo();
            } 
            else if (data.message) {
                // Generic message handling
                addMessage(data.message);
            }

            // Update current stage
            currentStage = data.stage || currentStage;
            console.log('Updated stage:', currentStage);
            console.log('Current brand details:', brandDetails);
        })
        .catch(error => {
            console.error('Error processing response:', error);
            addMessage('Sorry, something went wrong. Please try again.');
        });
    }

    // Generate logo
    function generateLogo() {
        console.log('Generating logo with brand details:', brandDetails);
        
        fetch('/generate_logo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                brand_details: brandDetails
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.logo_path) {
                generatedLogo.src = data.logo_path;
                logoPreview.style.display = 'block';
                addMessage('Logo generated successfully!');
                
                if (data.prompt_used) {
                    addMessage(`Logo Generation Prompt: ${data.prompt_used}`);
                }
            } else {
                addMessage('Sorry, logo generation failed.');
                if (data.error) {
                    console.error('Logo generation error:', data.error);
                }
            }
        })
        .catch(error => {
            console.error('Logo generation error:', error);
            addMessage('Sorry, there was an error generating the logo.');
        });
    }

    // Event listener for send button
    sendButton.addEventListener('click', () => {
        const userResponse = userInput.value.trim();
        if (userResponse) {
            processResponse(userResponse);
            userInput.value = '';
        }
    });

    // Event listener for Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const userResponse = userInput.value.trim();
            if (userResponse) {
                processResponse(userResponse);
                userInput.value = '';
            }
        }
    });

    // Download logo button
    downloadLogoButton.addEventListener('click', () => {
        const logoPath = generatedLogo.src;
        const link = document.createElement('a');
        link.href = logoPath;
        link.download = 'brand_logo.png';
        link.click();
    });

    // Start the conversation when page loads
    startConversation();
});