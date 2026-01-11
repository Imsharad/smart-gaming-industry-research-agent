---
title: "Part 2: The Architecture of an Agentic System"
author: "Sharad Jain, Technical Architect"
date: "2025-09-18"
---

In our last post, I introduced UDA-Hub as an **agentic product** designed to achieve outcomes, not just respond to prompts. Now, let's explore the architecture that makes this "goal-and-execute" model possible. A system this ambitious can't rely on a single, monolithic AI. It requires a team of autonomous agents working in concert, a design pattern known as a multi-agent system.

Multi-agent systems offer significant advantages over single-agent approaches, including improved problem-solving, enhanced scalability, and increased robustness. By distributing tasks among specialized agents, we can build a system that is more flexible, resilient, and capable of handling complex, real-world problems.

## The Core of UDA-Hub: A Four-Agent Team

Our design is centered around a multi-agent system where each agent embodies a key aspect of autonomous reasoning and action. This separation of concerns is fundamental to building a robust and scalable agentic product.

1.  **The Classifier Agent (Perception):** This is the first point of contact, responsible for **perceiving** the user's intent. It uses a fine-tuned language model to analyze the incoming ticket and performs two critical functions: categorizing the issue (e.g., `Billing`, `Technical`) and calculating a confidence score. This initial assessment is crucial for the system's subsequent planning phase.

2.  **The Supervisor Agent (Planning & Reasoning):** This is the strategic mind of the operation, acting as an AI orchestrator. Based on the Classifier's output, the Supervisor **reasons** about the problem and **plans** the next step. If confidence is high, it routes the ticket to the Resolver. If the issue is complex or ambiguous, it might decide to gather more information or escalate directly to a human. It's the core of the agent's autonomous decision-making capability.

3.  **The Resolver Agent (Action & Execution):** This is the primary **actor** in the system. It takes the categorized ticket and executes the plan. The Resolver has access to a suite of tools—APIs for interacting with external systems, database connectors for querying customer and product information, and knowledge retrieval functions for searching documentation. This is where the "execute" part of "goal-and-execute" comes to life.

4.  **The Escalation Agent (Adaptive Behavior):** No autonomous system is perfect. The Escalation Agent is responsible for graceful failure and **adaptation**. When the Supervisor or Resolver determines an issue is beyond the AI's capabilities, this agent takes over. It prepares a comprehensive handoff package for the human support team, including a summary of the problem and the steps the AI has already taken. This creates a "human-in-the-loop" system, which is essential for building user trust, handling complex edge cases, and providing a seamless customer experience. This approach also provides valuable data for future training and system improvement.

## The Foundation: A Dual-Database Architecture

To act effectively, our agents need access to the right information. We achieved this with a dual-database architecture that serves as the agent's view of the world. This design provides a clear separation between internal application data and sensitive customer information, which is crucial for security and data integrity.

*   **Core DB (`udahub.db`):** This is our internal application database. It contains information about our own products, services, and knowledge base articles. This data is owned and managed by the application.
*   **External DB (`cultpass.db`):** This database holds our customers' data—their subscription status, account details, and interaction history. By keeping this separate, we maintain a clean boundary and can enforce stricter access controls on sensitive information.

Our agents, via a secure tool-based interface, can query both databases. This allows the Resolver Agent, for example, to check a customer's subscription status in the `cultpass.db` while simultaneously pulling a relevant help article from the `udahub.db`. This separation also allows for independent scaling of the two databases, ensuring that customer data and application data can grow without impacting each other.

This combination of specialized agents and a well-defined data architecture is what allows UDA-Hub to move beyond simple automation and exhibit true goal-oriented behavior.

In the next part of this series, we'll explore the "brains" of the operation: how we use knowledge retrieval and memory to enable our agents to learn and adapt, making them truly intelligent.