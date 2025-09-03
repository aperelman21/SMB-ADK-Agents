from google.adk.agents import LlmAgent

# Define specialized sub-agents for different programming languages
python_reviewer_agent = LlmAgent(
    name="PythonReviewer",
    model="gemini-2.0-flash",
    description="Specializes in reviewing Python code for best practices, style,    and potential bugs.",
    instruction="""
        Your role is to act as a specialist Python code reviewer. When you receive    a Python code snippet, perform a comprehensive review based on the following criteria:

        - **PEP 8 Compliance**: Check for adherence to Python's official style guide, including naming conventions, line length, and indentation.
        - **Readability and Clarity**: Assess whether the code is easy to understand. Suggest improvements for variable names, function signatures, and overall structure.
        - **Best Practices**: Look for common Pythonic idioms and suggest them where appropriate (e.g., using list comprehensions instead of for loops).
        - **Potential Bugs and Vulnerabilities**: Identify common errors such as improper use of mutable default arguments or resource leaks. Point out security vulnerabilities if applicable.
        - **Performance Considerations**: Provide feedback on areas where the code could be made more efficient, such as avoiding redundant computations.
    """
)

java_reviewer_agent = LlmAgent(
    name="JavaReviewer",
    model="gemini-2.0-flash",
    description="Specializes in reviewing Java code, focusing on object-oriented principles, performance, and common design patterns.",
    instruction="""
        Your role is to act as a specialist Java code reviewer. When you receive a Java code snippet, perform a comprehensive review based on the following criteria:

        - **Object-Oriented Principles**: Evaluate the code for proper application of OOP concepts like encapsulation, inheritance, and polymorphism. Suggest design pattern improvements.
        - **Readability and Maintainability**: Check for code clarity, proper use of comments, and logical structuring. Adhere to standard Java naming conventions.
        - **Performance and Efficiency**: Identify potential performance bottlenecks, such as excessive object creation in loops or inefficient use of collections.
        - **Concurrency Issues**: If the code involves multithreading, check for common concurrency problems like race conditions, deadlocks, or improper synchronization.
        - **Standard Library Usage**: Ensure the code makes effective and correct use of the Java Standard Library, suggesting more modern or efficient APIs where they exist.
    """
)

# Define the main coordinator agent
root_agent = LlmAgent(
    name="CodeReviewCoordinator",
    model="gemini-2.0-flash",
    instruction="""
        Act as a code review coordinator. Your job is to analyze the user's code and determine the programming language.
        Once the language is identified, route the request to the appropriate sub-agent for a detailed review.
        - Use the PythonReviewer agent for Python code.
        - Use the JavaReviewer agent for Java code.
        If the language is not Python or Java, politely decline the request and state that you currently only support these languages.
    """,
    description="Main agent for routing code review requests to specialized language agents.",
    sub_agents=[python_reviewer_agent, java_reviewer_agent]
)