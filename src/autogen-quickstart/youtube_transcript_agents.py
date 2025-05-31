
# This script defines a system of agents to fetch and process YouTube video transcripts. 
# Key functionalities:
# 1. Fetch YouTube Transcript:
#     - Given a YouTube video ID, the `YouTube_Transcript_Agent` fetches the transcript of the video using the `youtube_transcript_api`.
# 2. Agent Definitions:
#     - Grammar Fix Agent (`Summarization_Agent`): Summarizes the fetched transcript into a concise and informative summary.
#     - Style Fix Agent (`Style_Agent`): Applies stylistic improvements to the summaries or excerpts.
#     - Final Review Agent: Combines and reviews the outputs from the Grammar and Style agents to produce a coherent, polished summary.
# 3. Workflow:
#     - A graph flow is constructed where:
#       a. The `YouTube_Transcript_Agent` fetches the transcript.
#       b. The Grammar and Style agents process the transcript in parallel.
#       c. The outputs from the Grammar and Style agents are joined and passed to the Final Review Agent for a comprehensive review.

from youtube_transcript_api import YouTubeTranscriptApi      
from youtube_transcript_api.formatters import TextFormatter
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

import asyncio  # Import asyncio to run the async function

# Define a tool to fetch YouTube transcripts
async def fetch_youtube_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript = "\n".join([f"{item['text']}" for item in transcript])
        return formatted_transcript
    except Exception as e:
        return f"Error fetching transcript for video ID {video_id}: {e}"

# Define the model client
model_client = OpenAIChatCompletionClient(model="gpt-4.1-nano")

# Define the YouTube Transcript Agent
youtube_transcript_agent = AssistantAgent(
    name="YouTube_Transcript_Agent",
    tools=[fetch_youtube_transcript],
    model_client=model_client,
    description="An agent that fetches YouTube video transcripts using video IDs.",
    system_message="You are a helpful assistant. Use the provided tool to fetch YouTube video transcripts.",
)

# Create two editor agents
editor1 = AssistantAgent("editor1", model_client=model_client, system_message="Edit the paragraph for grammar.")

editor2 = AssistantAgent("editor2", model_client=model_client, system_message="Edit the paragraph for style. Be concise. Use bullet items to highlight key points. ")

# Create the final reviewer agent
final_reviewer = AssistantAgent(
    "final_reviewer",
    model_client=model_client,
    system_message="Consolidate the grammar and style edits into a final version.",
)

# Build the workflow graph
builder = DiGraphBuilder()
builder.add_node(youtube_transcript_agent).add_node(editor1).add_node(editor2).add_node(final_reviewer)

# Fan-out from youtube_transcript_agent to editor1 and editor2
builder.add_edge(youtube_transcript_agent, editor1)
builder.add_edge(youtube_transcript_agent, editor2)

# Fan-in both editors into final reviewer
builder.add_edge(editor1, final_reviewer)
builder.add_edge(editor2, final_reviewer)

# Build and validate the graph
graph = builder.build()

# Create the flow
flow = GraphFlow(
    participants=builder.get_participants(),
    graph=graph,
)


# Define an async function to run the workflow
async def main():
    video_ids = ["egSh4TxS5go"]  # Replace with your list of YouTube video IDs

    # Process each video
    for video_id in video_ids:
        print(f"Processing video ID: {video_id}")

        await Console(flow.run_stream(task=f"Fetch the transcript of the YouTube video with ID {video_id} and summarize it."))

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
