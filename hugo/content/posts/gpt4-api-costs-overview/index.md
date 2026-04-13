---
post_kind: article
title: "GPT-4 vs GPT-3.5 — capabilities and API cost framing"
date: 2023-04-10T10:00:00-04:00
description: Notes on GPT-4 and GPT-3.5-turbo use cases, strengths, and thinking about chatbot API costs at scale.
tags:
    - AI
    - GPT-4
    - GPT-3.5
    - ChatGPT
    - OpenAI
    - NLP
    - API
---

![Article cover image](https://media.licdn.com/dms/image/D5612AQHKus7rY_HvVQ/article-cover_image-shrink_720_1280/0/1681059889367?e=1709769600&v=beta&t=39LUP6caikwBW_QeEC7T-2peoci56x6v9xzNtCPdWxQ "Cover Image for AI Article")

As artificial intelligence continues to advance, more and more companies are incorporating AI-powered chatbots into their customer service systems. These chatbots can handle a wide range of customer inquiries, from simple questions to more complex issues. However, the cost of implementing and maintaining such chatbots is an important factor to consider. In this article, we will calculate the costs of using GPT-4 and GPT-3.5-turbo models with a message cap of 25 messages every 3 hours for one month of usage, considering the same average prompt sizes (50 to 200 tokens).

## OpenAI API

The OpenAI API can be used for a wide range of natural language processing (NLP) tasks. Some of the most common uses of the API include:

- Language Translation: Translate text from one language to another, making it easy to communicate with people who speak different languages.
- Text Generation: Generate new text based on a given prompt or input. This can be used to generate headlines, summaries, and even entire articles.
- Text Summarization: Summarize long documents or articles into shorter, more concise versions. This can save time and make it easier to read and understand important information.
- Chatbot Development: Develop chatbots that can understand and respond to natural language input. This can be used for customer service, virtual assistants, and other applications.
- Question Answering: Answer questions with high accuracy and fluency; this feature is available with all GPT-3 engines.
- Language Understanding: Understand the meaning of text; this can be used to analyze customer feedback, analyze customer sentiment, and more.
- Text Completion: Complete text based on a given prompt; this can be used for autocompleting forms, writing emails, and more.
- Text Classification: Classify text into different categories, such as spam or not spam, positive or negative sentiment, etc.

## Model Comparison

### GPT-4

GPT-4 offers advanced problem-solving capabilities and broader general knowledge, making it more accurate than its predecessors. It excels in areas like creativity, visual input, and longer context, handling over 25,000 words of text for various applications. All those features are in the waiting list.

In terms of performance, GPT-4 scores higher approximate percentiles among test-takers in the Uniform Bar Exam and Biology Olympiad compared to ChatGPT.

Safety and alignment improvements in GPT-4 include training with human feedback, continuous improvement from real-world use, and GPT-4-assisted safety research.

Various organizations have collaborated with OpenAI to build innovative products using GPT-4, including Duolingo, Be My Eyes, Stripe, Morgan Stanley, Khan Academy, and the Government of Iceland.

Despite its impressive capabilities, GPT-4 still has known limitations, such as social biases, hallucinations, and adversarial prompts. OpenAI is committed to addressing these issues and promoting transparency, user education, and AI literacy. GPT-4 is available on ChatGPT Plus and as an API for developers to build applications and services. OpenAI is excited to see how people utilize GPT-4 as they work towards developing empowering technologies.

### GPT-3.5-turbo

The engine that is currently used in the ChatGPT Demo without the ChatGPT plus.

- Draft an email or other piece of writing
- Write Python code
- Answer questions about a set of documents
- Create conversational agents
- Give your software a natural language interface
- Tutor in a range of subjects
- Translate languages
- Simulate characters for video games and much more

Choosing between GPT-4 and GPT-3.5-turbo comes down to quality, latency, and budget: GPT-4 is stronger on difficult reasoning and long context, while GPT-3.5-turbo remains the workhorse for many chat and tooling scenarios. When you model costs, combine expected tokens per turn, traffic, and rate limits—especially if you cap messages per user per hour.
