from agents import BlueprintGeneratorAgent

# Initialize provider and agent
agent = BlueprintGeneratorAgent()

response = agent.generate_blueprint(
    statement = "Lovász local lemma, only this lemma, no other applications",
    pdf_files = ["../experiments/lovasz.pdf"],
    reference_urls = ["https://en.wikipedia.org/wiki/Lov%C3%A1sz_local_lemma"],
    refine_times = 2
)

history = agent.get_history()

for message in history:
    print(f"{message.role}: {message.content}")
    print("-" * 100)
