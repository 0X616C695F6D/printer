import subprocess

def summarize_text(text: str, word_limit: int) -> str:
    """
    Summarizes the provided text using the locally downloaded Deepseek 7B model via the Ollama CLI.
    The prompt instructs the model to output only the final summary without any chain-of-thought.
    
    Parameters:
        text (str): Full article text to summarize.
        word_limit (int): Maximum number of words allowed in the summary.
    
    Returns:
        str: The final summarized text constrained to the specified word limit.
    """
    prompt = (
        f"You are a newspaper journalist writing a column for a newspaper article."
        "You are tasked only with writing the content, not the subheading, title, etc."
        "Do not include any * in the summary, i.e similar to markdown."
        "Summarize the following article(s) into a most {word_limit} words."
        "And, at least 300 words. Remember, newspaper journalists have to make the"
        " summary interesting, do a good job of analyzing the data, and be truthful."
        "\n\n"
        f"{text}"
    )
    command = ["ollama", "run", "llama3.1:latest", prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Ollama command failed: {result.stderr}")
    
    output = result.stdout.strip()
    # Post-process: extract the text after "Final Summary:" if it exists.
    marker = "Final Summary:"
    if marker in output:
        final_summary = output.split(marker, 1)[1].strip()
    else:
        final_summary = output
    
    # Ensure the summary does not exceed the word limit.
    words = final_summary.split()
    if len(words) > word_limit:
        final_summary = " ".join(words[:word_limit])
    
    return final_summary

