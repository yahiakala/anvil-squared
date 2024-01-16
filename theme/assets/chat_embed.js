// anvilChat.js
function createAnvilChat(url) {
    window.addEventListener('DOMContentLoaded', (event) => {
        var chatWidth = Math.min(window.innerWidth * 0.8, 400); // chat bubble takes up to 80% of the viewport width, but no more than 400px
        var chatHeight = Math.min(window.innerHeight * 0.8, 500); // chat bubble takes up to 80% of the viewport height, but no more than 500px

        var styles = `
            #chatbubble {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: ${chatWidth}px;
            height: ${chatHeight}px;
            display: none;
            border: 1px solid #e4e4e7;
            border-radius: 6px;
            padding: 10px;
            box-shadow: inset 0 0 0 15px #fafafa;
            background-color: #fafafa;
            z-index: 1;
            box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
            }
            #openButton, #closeButton {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            background-color: #4285f4;
            border-radius: 50%;
            color: #ffffff;
            font-weight: bold;
            font-size: 20px;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
            }
            #closeButton {
            display: none;
            }
            /* Add some hover effects to the button */
            #openButton:hover, #closeButton:hover {
            transform: scale(1.1);
            }
        `;

        var styleSheet = document.createElement("style");
        styleSheet.type = "text/css";
        styleSheet.innerText = styles;
        document.head.appendChild(styleSheet);

        // Add the chat iframe
        const iframe = document.createElement("iframe");
        iframe.id = "chatbubble";
        iframe.src = url;

        // Add the open button
        const openButton = document.createElement("div");
        openButton.id = "openButton";
        openButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512" fill="white">
            <!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
            <path d="M512 240c0 114.9-114.6 208-256 208c-37.1 0-72.3-6.4-104.1-17.9c-11.9 8.7-31.3 20.6-54.3 30.6C73.6 471.1 44.7 480 16 480c-6.5 0-12.3-3.9-14.8-9.9c-2.5-6-1.1-12.8 3.4-17.4l0 0 0 0 0 0 0 0 .3-.3c.3-.3 .7-.7 1.3-1.4c1.1-1.2 2.8-3.1 4.9-5.7c4.1-5 9.6-12.4 15.2-21.6c10-16.6 19.5-38.4 21.4-62.9C17.7 326.8 0 285.1 0 240C0 125.1 114.6 32 256 32s256 93.1 256 208z"/>
            </svg>
        `;
        openButton.onclick = toggleChat;

        // Add the close button
        const closeButton = document.createElement("div");
        closeButton.id = "closeButton";
        closeButton.innerHTML = `
            <svg id="closeIcon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.3" stroke="white" width="24" height="24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5"></path>
            </svg>
        `;
        closeButton.onclick = toggleChat;

        document.body.appendChild(iframe);
        document.body.appendChild(openButton);
        document.body.appendChild(closeButton);

        function toggleChat() {
            if(iframe.style.display === "none") {
                iframe.style.display = "block";
                openButton.style.display = "none";
                closeButton.style.display = "flex";
            } else {
                iframe.style.display = "none";
                openButton.style.display = "flex";
                closeButton.style.display = "none";
            }
        }
    });
}