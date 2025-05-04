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
        
        // Enable/disable send button based on input
        if (this.value.trim() === '') {
            sendButton.disabled = true;
            sendButton.classList.add('disabled');
        } else {
            sendButton.disabled = false;
            sendButton.classList.remove('disabled');
        }
    });
    
    // Initialize send button state
    sendButton.disabled = true;
    
    // Mobile menu toggle with animation
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar--open');
        mainContent.classList.toggle('main-content--sidebar-open');
        
        // Add overlay when sidebar is open on mobile
        if (sidebar.classList.contains('sidebar--open') && window.innerWidth <= 768) {
            const overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.right = '0';
            overlay.style.bottom = '0';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            overlay.style.zIndex = '90';
            overlay.style.opacity = '0';
            overlay.style.transition = 'opacity 0.3s ease';
            document.body.appendChild(overlay);
            
            // Fade in overlay
            setTimeout(() => {
                overlay.style.opacity = '1';
            }, 10);
            
            // Close sidebar when clicking overlay
            overlay.addEventListener('click', function() {
                sidebar.classList.remove('sidebar--open');
                mainContent.classList.remove('main-content--sidebar-open');
                overlay.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 300);
            });
        } else {
            // Remove overlay when sidebar is closed
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 300);
            }
        }
    });
    
    // Theme toggle with smooth transition
    themeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        const icon = themeToggle.querySelector('i');
        const text = themeToggle.querySelector('span');
        
        if (body.classList.contains('dark-mode')) {
            // Animate icon change
            icon.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                icon.className = 'fas fa-sun';
                icon.style.transform = 'rotate(0)';
            }, 150);
            text.textContent = 'Light mode';
            
            // Save preference
            localStorage.setItem('theme', 'dark');
        } else {
            // Animate icon change
            icon.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                icon.className = 'fas fa-moon';
                icon.style.transform = 'rotate(0)';
            }, 150);
            text.textContent = 'Dark mode';
            
            // Save preference
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Load saved theme preference
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        themeToggle.querySelector('i').className = 'fas fa-sun';
        themeToggle.querySelector('span').textContent = 'Light mode';
    }
    
    // New chat button with animation
    document.querySelector('.new-chat-btn').addEventListener('click', function() {
        // Add button press animation
        this.classList.add('pressed');
        setTimeout(() => {
            this.classList.remove('pressed');
        }, 200);
        
        // Clear conversation with fade out effect
        const turns = conversation.querySelectorAll('.conversation-turn');
        turns.forEach((turn, index) => {
            setTimeout(() => {
                turn.style.opacity = '0';
                turn.style.transform = 'translateY(-10px)';
            }, index * 50);
        });
        
        // Clear and add welcome message after animation
        setTimeout(() => {
            conversation.innerHTML = '';
            addWelcomeMessage();
        }, turns.length * 50 + 300);
    });
    
    // Conversation history items with hover effect
    const conversationItems = document.querySelectorAll('.conversation-item');
    conversationItems.forEach((item) => {
        item.addEventListener('click', function() {
            conversationItems.forEach(i => i.classList.remove('conversation-item--active'));
            this.classList.add('conversation-item--active');
            
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.backgroundColor = 'rgba(0, 132, 255, 0.2)';
            ripple.style.width = '100px';
            ripple.style.height = '100px';
            ripple.style.transform = 'translate(-50%, -50%) scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            
            ripple.style.left = event.clientX - this.getBoundingClientRect().left + 'px';
            ripple.style.top = event.clientY - this.getBoundingClientRect().top + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
            
            // On mobile, close the sidebar after selection
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('sidebar--open');
                mainContent.classList.remove('main-content--sidebar-open');
                
                // Remove overlay
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) {
                    overlay.style.opacity = '0';
                    setTimeout(() => {
                        document.body.removeChild(overlay);
                    }, 300);
                }
            }
        });
    });
    
    // Initialize think dropdowns with smooth animations
    function initThinkDropdowns() {
        document.querySelectorAll('.think-dropdown__header').forEach(header => {
            header.addEventListener('click', function() {
                const dropdown = this.closest('.think-dropdown');
                const content = dropdown.querySelector('.think-dropdown__content');
                const chevron = this.querySelector('.fa-chevron-down');
                
                if (dropdown.classList.contains('open')) {
                    // Close dropdown with animation
                    chevron.style.transform = 'rotate(0deg)';
                    content.style.maxHeight = '0';
                    content.style.padding = '0';
                    
                    setTimeout(() => {
                        dropdown.classList.remove('open');
                    }, 300);
                } else {
                    // Open dropdown with animation
                    dropdown.classList.add('open');
                    chevron.style.transform = 'rotate(180deg)';
                    content.style.padding = '12px';
                    content.style.maxHeight = content.scrollHeight + 24 + 'px'; // Add padding to height
                }
            });
        });
    }
    
    function addWelcomeMessage() {
        // Add welcome message with typing animation
        const typingIndicator = typingTemplate.content.cloneNode(true);
        conversation.appendChild(typingIndicator);
        
        // Simulate typing and then show welcome message
        setTimeout(() => {
            // Remove typing indicator
            const typingElement = document.querySelector('.typing-indicator').closest('.conversation-turn');
            if (typingElement) {
                typingElement.style.opacity = '0';
                typingElement.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    typingElement.remove();
                    
                    // Add welcome message
                    const welcomeTurn = aiTurnTemplate.content.cloneNode(true);
                    welcomeTurn.querySelector('.message-content').textContent = "Hello! I'm studLLm Your own Personal Assistant For Your student life. How can I help you today?";
                    
                    // Hide the think dropdown for welcome message
                    welcomeTurn.querySelector('.think-dropdown').style.display = 'none';
                    conversation.appendChild(welcomeTurn);
                }, 300);
            }
        }, 1500);
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
        sendButton.disabled = true;
        
        // Show typing indicator with fade-in animation
        const typingIndicator = typingTemplate.content.cloneNode(true);
        conversation.appendChild(typingIndicator);
        scrollToBottom();
        
        try {
            // Send message to Flask API
            const response = await fetch('/chat', {
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
            
            // Remove typing indicator with fade-out animation
            const typingElement = document.querySelector('.typing-indicator').closest('.conversation-turn');
            if (typingElement) {
                typingElement.style.opacity = '0';
                typingElement.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    typingElement.remove();
                    
                    // Process the response
                    processApiResponse(data);
                }, 300);
            }
        } catch (error) {
            console.error('Error:', error);
            
            // Remove typing indicator
            const typingElement = document.querySelector('.typing-indicator').closest('.conversation-turn');
            if (typingElement) {
                typingElement.style.opacity = '0';
                typingElement.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    typingElement.remove();
                    
                    // Show error message
                    const aiTurnContent = addAITurn("I'm sorry, I couldn't process your request. Please try again later.");
                    
                    // Hide the think dropdown for error message
                    const thinkDropdown = aiTurnContent.closest('.turn-content').querySelector('.think-dropdown');
                    thinkDropdown.style.display = 'none';
                }, 300);
            }
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
    
    // Import the 'marked' library (or define it if it's already included)
    const marked = window.marked; // Assumes marked is available globally
    // If marked is not available globally, you can include it via CDN or a module bundler.
    // For example, if using a CDN:
    // <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
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
        // Smooth scroll to bottom
        conversation.scrollTo({
            top: conversation.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    // Handle window resize for responsive design
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('sidebar--open');
            mainContent.classList.remove('main-content--sidebar-open');
            
            // Remove overlay
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 300);
            }
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
            
            // Remove overlay
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 300);
            }
        }
    });
    
    // Add ripple animation style
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: translate(-50%, -50%) scale(3);
                opacity: 0;
            }
        }
        
        .pressed {
            transform: scale(0.98);
        }
    `;
    document.head.appendChild(style);
});