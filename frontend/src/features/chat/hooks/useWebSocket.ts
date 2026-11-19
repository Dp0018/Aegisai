import { useEffect, useState, useRef } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || API_BASE_URL.replace(/^http/, "ws");

function getWebSocketUrl(threadId: string): string {
    return `${WS_BASE_URL}/agent/ws/${threadId}`;
}

export function useWebSocket(
    threadId: string | null,
    onMessageReceived: (message: any) => void
) {
    const [isConnected, setIsConnected] = useState(false);
    const callbackRef = useRef(onMessageReceived);

    // Keep the callback ref updated with the latest function reference
    useEffect(() => {
        callbackRef.current = onMessageReceived;
    }, [onMessageReceived]);

    useEffect(() => {
        if (!threadId) {
            setIsConnected(false);
            return;
        }

        const wsUrl = getWebSocketUrl(threadId);
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            setIsConnected(true);
        };

        ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                callbackRef.current(message);
            } catch (err) {
                console.error("Error parsing WebSocket message:", err);
            }
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = () => {
            setIsConnected(false);
        };

        return () => {
            ws.close();
        };
    }, [threadId]);

    return { isConnected };
}
