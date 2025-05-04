document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const conversation = document.getElementById('conversation');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;
    
    // Templates
    const userTurnTemplate = document.getElementById('userTurnTemplate');
    const aiTurnTemplate = document.getElementById('aiTurnTemplate');
    const typingTemplate = document.getElementById('typingTemplate');
    const jobListingTemplate = document.getElementById('jobListingTemplate');
    const mapTemplate = document.getElementById('mapTemplate');
    
    // Sample data for demonstrations
    const sampleJobListings = [
        {
            title: 'Frontend Developer',
            company: 'Tech Innovations Inc.',
            location: 'San Francisco, CA',
            salary: '$120,000 - $150,000'
        },
        {
            title: 'UX Designer',
            company: 'Creative Solutions',
            location: 'New York, NY',
            salary: '$90,000 - $120,000'
        },
        {
            title: 'Full Stack Engineer',
            company: 'Global Systems',
            location: 'Remote',
            salary: '$130,000 - $160,000'
        },
        {
            title: 'Product Manager',
            company: 'Future Technologies',
            location: 'Austin, TX',
            salary: '$140,000 - $180,000'
        },
        {
            title: 'DevOps Engineer',
            company: 'Cloud Solutions',
            location: 'Seattle, WA',
            salary: '$125,000 - $155,000'
        }
    ];
    
    // Sample map data (simplified SVG map)
    const sampleMapSVG = `
        <svg width="100%" height="100%" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="800" height="400" fill="#e6e6e6"/>
            <path d="M100,100 L700,100 L700,300 L100,300 Z" fill="#c2c2c2" stroke="#999" stroke-width="2"/>
            <circle cx="200" cy="150" r="10" fill="#0084ff" stroke="#fff" stroke-width="2"/>
            <circle cx="350" cy="200" r="10" fill="#0084ff" stroke="#fff" stroke-width="2"/>
            <circle cx="500" cy="250" r="10" fill="#0084ff" stroke="#fff" stroke-width="2"/>
            <circle cx="650" cy="180" r="10" fill="#0084ff" stroke="#fff" stroke-width="2"/>
            <path d="M200,150 L350,200 L500,250 L650,180" stroke="#0084ff" stroke-width="2" fill="none"/>
            <text x="200" y="130" font-size="12" text-anchor="middle" fill="#333">San Francisco</text>
            <text x="350" y="180" font-size="12" text-anchor="middle" fill="#333">Chicago</text>
            <text x="500" y="230" font-size="12" text-anchor="middle" fill="#333">New York</text>
            <text x="650" y="160" font-size="12" text-anchor="middle" fill="#333">Boston</text>
        </svg>
    `;
    
    // Add welcome message
    addWelcomeMessage();
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Mobile menu toggle
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar--open');
        mainContent.classList.toggle('main-content--sidebar-open');
    });
    
    // Theme toggle
    themeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        const icon = themeToggle.querySelector('i');
        const text = themeToggle.querySelector('span');
        
        if (body.classList.contains('dark-mode')) {
            icon.className = 'fas fa-sun';
            text.textContent = 'Light mode';
        } else {
            icon.className = 'fas fa-moon';
            text.textContent = 'Dark mode';
        }
    });
    
    // New chat button
    document.querySelector('.new-chat-btn').addEventListener('click', function() {
        // Clear conversation and add welcome message
        conversation.innerHTML = '';
        addWelcomeMessage();
    });
    
    // Conversation history items
    const conversationItems = document.querySelectorAll('.conversation-item');
    conversationItems.forEach((item) => {
        item.addEventListener('click', function() {
            conversationItems.forEach(i => i.classList.remove('conversation-item--active'));
            this.classList.add('conversation-item--active');
            
            // On mobile, close the sidebar after selection
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('sidebar--open');
                mainContent.classList.remove('main-content--sidebar-open');
            }
        });
    });
    
    // Initialize think dropdowns
    function initThinkDropdowns() {
        document.querySelectorAll('.think-dropdown__header').forEach(header => {
            header.addEventListener('click', function() {
                const dropdown = this.closest('.think-dropdown');
                const content = dropdown.querySelector('.think-dropdown__content');
                
                if (dropdown.classList.contains('open')) {
                    // Close dropdown
                    content.style.maxHeight = '0';
                    setTimeout(() => {
                        dropdown.classList.remove('open');
                    }, 300);
                } else {
                    // Open dropdown
                    dropdown.classList.add('open');
                    content.style.maxHeight = content.scrollHeight + 'px';
                }
            });
        });
    }
    
    function addWelcomeMessage() {
        // Add welcome message
        const welcomeTurn = aiTurnTemplate.content.cloneNode(true);
        welcomeTurn.querySelector('.message-content').textContent = "Hello! I'm studLLm Your own Perosnal Assistant For Your studner life. How can I help you today?";
        
        // Hide the think dropdown for welcome message
        welcomeTurn.querySelector('.think-dropdown').style.display = 'none';
        conversation.appendChild(welcomeTurn);
    }
    
    // Functions
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addUserTurn(message);
        
        // Clear input
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show typing indicator
        const typingIndicator = typingTemplate.content.cloneNode(true);
        conversation.appendChild(typingIndicator);
        scrollToBottom();
        
        try {
            // Send message to API
            const response = await fetch('http://127.0.0.1:8000/api/v1/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            const typingElement = document.querySelector('.typing-indicator').closest('.conversation-turn');
            if (typingElement) typingElement.remove();
            
            // Process the response
            processApiResponse(data);
        } catch (error) {
            console.error('Error:', error);
            
            // Remove typing indicator
            const typingElement = document.querySelector('.typing-indicator').closest('.conversation-turn');
            if (typingElement) typingElement.remove();
            
            // Show error message
            const aiTurnContent = addAITurn("I'm sorry, I couldn't process your request. Please try again later.");
            
            // Hide the think dropdown for error message
            const thinkDropdown = aiTurnContent.closest('.turn-content').querySelector('.think-dropdown');
            thinkDropdown.style.display = 'none';
        }
    }
    
    function processApiResponse(data) {
        if (!data || !data.message) {
            const aiTurnContent = addAITurn("I'm sorry, I received an invalid response. Please try again.");
            const thinkDropdown = aiTurnContent.closest('.turn-content').querySelector('.think-dropdown');
            thinkDropdown.style.display = 'none';
            return;
        }
        
        // Extract message and thinking content from the new format
        const messageContent = data.message;
        const thinkingContent = data.Thinking || '';
        
        // Add AI response
        const aiTurnContent = addAITurn(messageContent);
        
        // Set think content if available
        if (thinkingContent) {
            const thinkDropdown = aiTurnContent.closest('.turn-content').querySelector('.think-dropdown');
            thinkDropdown.querySelector('.think-dropdown__content').textContent = thinkingContent.replace(/<Thinking>|<\/think>/g, '').trim();
            thinkDropdown.classList.add('has-content');
        } else {
            // Hide think dropdown if no think content
            const thinkDropdown = aiTurnContent.closest('.turn-content').querySelector('.think-dropdown');
            thinkDropdown.style.display = 'none';
        }
        
        // Check for job-related content
        if (messageContent.toLowerCase().includes('job') || 
            messageContent.toLowerCase().includes('career') || 
            messageContent.toLowerCase().includes('position')) {
            addJobListings(aiTurnContent, 3);
        }
        
        // Check for location-related content
        if (messageContent.toLowerCase().includes('map') || 
            messageContent.toLowerCase().includes('location') || 
            messageContent.toLowerCase().includes('where')) {
            addMap(aiTurnContent);
        }
        
        // Initialize think dropdowns
        initThinkDropdowns();
    }
    
    function addUserTurn(text) {
        const turnElement = userTurnTemplate.content.cloneNode(true);
        turnElement.querySelector('.message-content').textContent = text;
        conversation.appendChild(turnElement);
        scrollToBottom();
    }
    
    function addAITurn(text, citations = []) {
        const turnElement = aiTurnTemplate.content.cloneNode(true);
        
        // Convert Markdown to HTML
        turnElement.querySelector('.message-content').innerHTML = marked.parse(text);
    
        // Add citations if any
        if (citations.length > 0) {
            const citationsContainer = turnElement.querySelector('.citations');
            citations.forEach(citation => {
                const citationElement = document.createElement('span');
                citationElement.className = 'citation';
                citationElement.textContent = citation;
                citationsContainer.appendChild(citationElement);
            });
        }
    
        conversation.appendChild(turnElement);
        scrollToBottom();
    
        return turnElement.querySelector('.turn-content');
    }
    
    
    function addJobListings(aiTurnContent, count = 3) {
        const listings = sampleJobListings.slice(0, count);
        
        listings.forEach((job, index) => {
            const jobElement = jobListingTemplate.content.cloneNode(true);
            jobElement.querySelector('.job-listing__title').textContent = job.title;
            jobElement.querySelector('.job-listing__company').textContent = job.company;
            jobElement.querySelector('.job-listing__location').textContent = job.location;
            jobElement.querySelector('.job-listing__salary').textContent = job.salary;
            
            aiTurnContent.appendChild(jobElement);
            
            // Add staggered animation
            setTimeout(() => {
                aiTurnContent.querySelectorAll('.job-listing')[index].style.animationDelay = (0.1 * (index + 1)) + 's';
            }, 10);
        });
        
        scrollToBottom();
    }
    
    function addMap(aiTurnContent, title = 'Location Map') {
        const mapElement = mapTemplate.content.cloneNode(true);
        mapElement.querySelector('.map-container__title').textContent = title;
        mapElement.querySelector('.map-container__map').innerHTML = sampleMapSVG;
        
        aiTurnContent.appendChild(mapElement);
        scrollToBottom();
    }
    
    function scrollToBottom() {
        conversation.scrollTop = conversation.scrollHeight;
    }
    
    // Handle window resize for responsive design
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('sidebar--open');
            mainContent.classList.remove('main-content--sidebar-open');
        }
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && 
            sidebar.classList.contains('sidebar--open') && 
            !sidebar.contains(e.target) && 
            e.target !== menuToggle) {
            sidebar.classList.remove('sidebar--open');
            mainContent.classList.remove('main-content--sidebar-open');
        }
    });
});