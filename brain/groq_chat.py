from groq import Groq

from config import GROQ_MODEL, GROQ_API_KEY
from brain.identify import Identity
from memory.vector_store import VectorStore


MIN_WORDS_TO_REMEMBER = 4
DUPLICATE_DISTANCE_THRESHOLD = 0.05


class AtlasBrain:

    def __init__(self):

        self.client = Groq(api_key=GROQ_API_KEY)

        self.identity = Identity()

        self.messages = [
            {
                "role": "system",
                "content": self.identity.prompt()
            }
        ]

        self.memory = VectorStore()

    def _is_worth_remembering(self, text: str) -> bool:

        word_count = len(text.split())
        if word_count < MIN_WORDS_TO_REMEMBER:
            return False

        closest = self.memory.find_closest(text)

        if closest is not None:
            _, distance = closest

            if distance < DUPLICATE_DISTANCE_THRESHOLD:
                return False

        return True

    def chat(self, user_message):

        message = user_message.lower()

        # ==========================
        # Identity Questions
        # ==========================

        assistant_name = self.identity.data["name"]
        creator_name = self.identity.data["creator"]

        if "who are you" in message:
            return f"I am {assistant_name}, a cloud-powered AI assistant created by {creator_name}, Sir."

        if "what is your name" in message:
            return f"My name is {assistant_name}, Sir."

        if "who created you" in message:
            return f"I was created by {creator_name}, Sir."

        if "who is your creator" in message:
            return f"My creator is {creator_name}, Sir."

        if "what is your creator's name" in message:
            return f"My creator's name is {creator_name}, Sir."

        if "who made you" in message:
            return f"I was created by {creator_name}, Sir."

        if "what model powers you" in message:
            return f"I am powered by {GROQ_MODEL} running on Groq, Sir."

        # ==========================
        # Retrieve Relevant Memories
        # ==========================

        relevant_memories = []

        if self.memory.has_memories():
            relevant_memories = self.memory.search_memories(user_message)

        self.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # ==========================
        # Inject Memory Context
        # ==========================

        if relevant_memories:

            memory_text = "\n".join(relevant_memories)

            memory_context = {
                "role": "system",
                "content": f"Relevant memories about Sir:\n{memory_text}"
            }

            request_messages = (
                self.messages[:-1]
                + [memory_context]
                + [self.messages[-1]]
            )

        else:
            request_messages = self.messages

        # ==========================
        # Send to Groq
        # ==========================

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=request_messages
        )

        assistant = response.choices[0].message.content.strip()

        # ==========================
        # Keep "Sir" at the end
        # ==========================

        if not assistant.endswith(("Sir.", "Sir!", "Sir?")):
            assistant += ", Sir."

        # ==========================
        # Save Conversation
        # ==========================

        self.messages.append(
            {
                "role": "assistant",
                "content": assistant
            }
        )

        # ==========================
        # Store New Memory
        # ==========================

        if self._is_worth_remembering(user_message):
            self.memory.add_memory(user_message)

        return assistant
