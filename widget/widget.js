(function () {
    // LeadMe Chat Widget
    const API_URL = 'https://leadme-backend.onrender.com/api/v1';
    let clientId = 'default_client';
    
    // Generate or retrieve session ID
    let sessionId = localStorage.getItem('leadme_session_id');
    if (!sessionId) {
        sessionId = 'session_' + Math.random().toString(36).substring(2, 11);
        localStorage.setItem('leadme_session_id', sessionId);
    }
    
    let unresolvedQuestion = '';

    // Load Google Fonts
    const fontLink = document.createElement('link');
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap';
    fontLink.rel = 'stylesheet';
    document.head.appendChild(fontLink);

    // Inject Styles
    const style = document.createElement('style');
    style.textContent = `
        #leadme-widget-container {
            font-family: 'Inter', sans-serif;
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            pointer-events: none;
        }

        #leadme-launcher {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
            pointer-events: auto;
            position: relative;
            z-index: 2;
        }

        #leadme-launcher:hover {
            transform: scale(1.1);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.6);
        }

        #leadme-launcher svg {
            width: 28px;
            height: 28px;
            fill: white;
            transition: transform 0.3s ease;
        }

        #leadme-chat-window {
            width: 380px;
            height: 600px;
            max-height: calc(100vh - 100px);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            margin-bottom: 20px;
            opacity: 0;
            transform: translateY(20px) scale(0.95);
            transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
            pointer-events: auto;
            transform-origin: bottom right;
        }
        
        #leadme-chat-window.leadme-open {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        
        #leadme-chat-window.leadme-closed {
            pointer-events: none;
            display: none;
        }

        #leadme-header {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            padding: 20px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }

        #leadme-header-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        #leadme-avatar {
            width: 40px;
            height: 40px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid rgba(255, 255, 255, 0.4);
        }
        
        #leadme-avatar svg {
            width: 20px;
            height: 20px;
            fill: white;
        }

        #leadme-title {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
            line-height: 1.2;
        }
        
        #leadme-subtitle {
            font-size: 12px;
            opacity: 0.8;
            margin: 0;
        }

        #leadme-close-btn {
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s ease;
        }
        
        #leadme-close-btn:hover {
            background: rgba(255, 255, 255, 0.25);
        }

        #leadme-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
            scroll-behavior: smooth;
        }
        
        #leadme-messages::-webkit-scrollbar {
            width: 6px;
        }
        #leadme-messages::-webkit-scrollbar-track {
            background: transparent;
        }
        #leadme-messages::-webkit-scrollbar-thumb {
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
        }

        .leadme-msg {
            max-width: 85%;
            padding: 12px 16px;
            font-size: 14px;
            line-height: 1.5;
            animation: leadme-fade-in 0.3s ease-out forwards;
            word-wrap: break-word;
        }
        
        @keyframes leadme-fade-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .leadme-msg-user {
            background: linear-gradient(135deg, #6366f1, #818cf8);
            color: white;
            border-radius: 20px 20px 4px 20px;
            align-self: flex-end;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
        }

        .leadme-msg-bot {
            background: #f1f5f9;
            color: #1e293b;
            border-radius: 20px 20px 20px 4px;
            align-self: flex-start;
            border: 1px solid rgba(0,0,0,0.05);
        }

        .leadme-typing-indicator {
            display: flex;
            gap: 4px;
            padding: 14px 18px;
            background: #f1f5f9;
            border-radius: 20px 20px 20px 4px;
            align-self: flex-start;
            width: fit-content;
        }
        
        .leadme-dot {
            width: 6px;
            height: 6px;
            background: #94a3b8;
            border-radius: 50%;
            animation: leadme-bounce 1.4s infinite ease-in-out both;
        }
        
        .leadme-dot:nth-child(1) { animation-delay: -0.32s; }
        .leadme-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes leadme-bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        #leadme-input-container {
            padding: 16px;
            background: white;
            border-top: 1px solid rgba(0,0,0,0.05);
            display: flex;
            gap: 12px;
            align-items: center;
        }

        #leadme-input {
            flex: 1;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            border-radius: 24px;
            padding: 14px 20px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        
        #leadme-input:focus {
            border-color: #818cf8;
            background: white;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        #leadme-send-btn {
            background: #6366f1;
            color: white;
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        
        #leadme-send-btn:hover {
            background: #4f46e5;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }
        
        #leadme-send-btn svg {
            width: 20px;
            height: 20px;
            fill: white;
            margin-left: 2px;
        }
        
        .leadme-fallback-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px;
            margin-top: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            animation: leadme-fade-in 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        
        .leadme-fallback-title {
            font-weight: 600;
            font-size: 14px;
            color: #1e293b;
            margin: 0 0 12px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .leadme-fallback-input {
            width: 100%;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            margin-bottom: 12px;
            outline: none;
            box-sizing: border-box;
            transition: border-color 0.2s;
            font-family: 'Inter', sans-serif;
        }
        
        .leadme-fallback-input:focus {
            border-color: #6366f1;
        }
        
        .leadme-fallback-btn {
            width: 100%;
            background: #1e293b;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
            font-family: 'Inter', sans-serif;
        }
        
        .leadme-fallback-btn:hover {
            background: #0f172a;
        }

        @media (max-width: 480px) {
            #leadme-chat-window {
                width: calc(100vw - 32px);
                height: calc(100vh - 100px);
                bottom: 80px;
                right: 16px;
            }
            #leadme-widget-container {
                bottom: 16px;
                right: 16px;
            }
        }
    `;
    document.head.appendChild(style);

    // Create DOM Elements
    const container = document.createElement('div');
    container.id = 'leadme-widget-container';
    
    const chatWindow = document.createElement('div');
    chatWindow.id = 'leadme-chat-window';
    chatWindow.className = 'leadme-closed';
    
    chatWindow.innerHTML = `
        <div id="leadme-header">
            <div id="leadme-header-info">
                <div id="leadme-avatar">
                    <svg viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z" /></svg>
                </div>
                <div>
                    <h3 id="leadme-title">LeadMe Assistant</h3>
                    <p id="leadme-subtitle">We reply instantly</p>
                </div>
            </div>
            <button id="leadme-close-btn">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 1L13 13M1 13L13 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            </button>
        </div>
        <div id="leadme-messages">
            <div class="leadme-msg leadme-msg-bot">Hi there! 👋 How can I help you today?</div>
        </div>
        <div id="leadme-input-container">
            <input type="text" id="leadme-input" placeholder="Type your message..." autocomplete="off"/>
            <button id="leadme-send-btn">
                <svg viewBox="0 0 24 24"><path d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/></svg>
            </button>
        </div>
    `;
    
    const launcher = document.createElement('div');
    launcher.id = 'leadme-launcher';
    launcher.innerHTML = `
        <svg viewBox="0 0 24 24"><path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4C22,2.89 21.1,2 20,2Z" /></svg>
    `;
    
    container.appendChild(chatWindow);
    container.appendChild(launcher);
    document.body.appendChild(container);

    const closeBtn = document.getElementById('leadme-close-btn');
    const messagesEl = document.getElementById('leadme-messages');
    const inputEl = document.getElementById('leadme-input');
    const sendBtn = document.getElementById('leadme-send-btn');
    
    const scriptTag = document.currentScript || document.querySelector('script[src*="widget.js"]');
    if (scriptTag && scriptTag.getAttribute('data-client-id')) {
        clientId = scriptTag.getAttribute('data-client-id');
    }

    let isOpen = false;

    function toggleChat() {
        isOpen = !isOpen;
        if (isOpen) {
            chatWindow.classList.remove('leadme-closed');
            chatWindow.classList.add('leadme-open');
            launcher.innerHTML = `<svg viewBox="0 0 24 24"><path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" /></svg>`;
            setTimeout(() => inputEl.focus(), 300);
        } else {
            chatWindow.classList.remove('leadme-open');
            setTimeout(() => chatWindow.classList.add('leadme-closed'), 400);
            launcher.innerHTML = `<svg viewBox="0 0 24 24"><path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4C22,2.89 21.1,2 20,2Z" /></svg>`;
        }
    }

    launcher.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `leadme-msg leadme-msg-${sender}`;
        msgDiv.innerText = text;
        messagesEl.appendChild(msgDiv);
        scrollToBottom();
    }
    
    function showTyping() {
        const div = document.createElement('div');
        div.className = 'leadme-typing-indicator';
        div.id = 'leadme-typing';
        div.innerHTML = '<div class="leadme-dot"></div><div class="leadme-dot"></div><div class="leadme-dot"></div>';
        messagesEl.appendChild(div);
        scrollToBottom();
    }
    
    function hideTyping() {
        const typing = document.getElementById('leadme-typing');
        if (typing) typing.remove();
    }
    
    function renderFallbackForm() {
        const card = document.createElement('div');
        card.className = 'leadme-fallback-card';
        card.innerHTML = `
            <h4 class="leadme-fallback-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                Connect with an Expert
            </h4>
            <p style="font-size: 13px; color: #64748b; margin-top: 0; margin-bottom: 12px; line-height: 1.4;">I don't have the exact answer for that right now. Leave your email and our team will get back to you shortly!</p>
            <input type="email" class="leadme-fallback-input" placeholder="Your work email" required/>
            <button class="leadme-fallback-btn">Send Message</button>
        `;
        messagesEl.appendChild(card);
        scrollToBottom();
        
        const submitBtn = card.querySelector('.leadme-fallback-btn');
        const emailInput = card.querySelector('.leadme-fallback-input');
        
        submitBtn.addEventListener('click', async () => {
            const email = emailInput.value;
            if (!email || !email.includes('@')) {
                alert('Please enter a valid email.');
                return;
            }
            
            card.innerHTML = '<div style="text-align:center; padding:10px;"><div class="leadme-dot" style="display:inline-block"></div><div class="leadme-dot" style="display:inline-block; margin-left:4px;"></div><div class="leadme-dot" style="display:inline-block; margin-left:4px;"></div></div>';
            
            try {
                const res = await fetch(`${API_URL}/leads/capture`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        client_id: clientId,
                        session_id: sessionId,
                        email: email,
                        unresolved_question: unresolvedQuestion
                    })
                });
                
                if (res.ok) {
                    card.innerHTML = `
                        <div style="text-align:center; color: #10b981;">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:8px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                            <h4 style="margin:0 0 4px 0; font-size:14px; color:#1e293b;">Thank you!</h4>
                            <p style="margin:0; font-size:12px; color:#64748b;">Our team will reach out shortly.</p>
                        </div>
                    `;
                    setTimeout(scrollToBottom, 100);
                } else {
                    throw new Error('Failed to submit');
                }
            } catch (e) {
                card.innerHTML = '<p style="color:#ef4444; font-size:13px; text-align:center; margin:0;">Failed to send. Please try again later.</p>';
                console.error(e);
            }
        });
    }

    function scrollToBottom() {
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    async function sendMessage() {
        const text = inputEl.value.trim();
        if (!text) return;
        
        inputEl.value = '';
        addMessage(text, 'user');
        unresolvedQuestion = text;
        showTyping();
        
        try {
            const res = await fetch(`${API_URL}/chat/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    client_id: clientId,
                    session_id: sessionId,
                    message: text
                })
            });
            
            const data = await res.json();
            hideTyping();
            
            if (data.lead_capture_prompt) {
                if (data.reply) addMessage(data.reply, 'bot');
                renderFallbackForm();
            } else {
                addMessage(data.reply, 'bot');
            }
            
        } catch (error) {
            hideTyping();
            addMessage('Sorry, I am having trouble connecting right now.', 'bot');
            console.error('LeadMe Chat Error:', error);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    inputEl.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

})();
