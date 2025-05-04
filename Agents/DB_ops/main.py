from fastapi import FastAPI, Depends
from pymongo import MongoClient
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from .get_embeddings import hf_mpnet_embed
from typing import Callable, Awaitable, Union, List
import asyncio
import uuid
from chromadb.config import Settings
import chromadb

# MongoDB CRUD class


class MongoCRUD:
    def __init__(self):
        uri = "mongodb+srv://"
        self.client = MongoClient(uri)
        self.db = self.client.get_database("")
        self.users_collection = self.db["users"]
        self.user_state_collection = self.db["user_state"]
        self.chat_history_collection = self.db["chat_history"]

    def get_clients(self, db_name: str = ""):
        """Get MongoDB client"""
        return self.client[db_name]

    # === USER OPERATIONS ===
    def get_user(self, user_id: str) -> dict:
        """Get a user document by ID; create with defaults if not found."""
        user = self.users_collection.find_one({"_id": user_id})
        if not user:
            default_user = {
                "_id": user_id,
                "state": {"initialized": True, "last_updated": datetime.utcnow().isoformat()},
                "state_history": []
            }
            self.users_collection.insert_one(default_user)
            return default_user
        return user

    # === STATE MANAGEMENT ===
    def update_user_state(self, user_id: str, state_data: dict):
        """Upsert user state; initialize history only on insert."""
        timestamp = datetime.utcnow().isoformat()
        state_data["last_updated"] = timestamp
        update_op = {
            "$set": {"state": state_data},
            "$setOnInsert": {
                "_id": user_id,
                "state_history": []
            }
        }
        existing = self.users_collection.find_one(
            {"_id": user_id}, {"state": 1}
        )
        if existing and "state" in existing:
            update_op["$push"] = {
                "state_history": {
                    "previous_state": existing["state"],
                    "updated_at": timestamp
                }
            }

        result = self.users_collection.update_one(
            {"_id": user_id},
            update_op,
            upsert=True
        )
        return result.modified_count or (1 if result.upserted_id else 0)

    def get_user_state(self, user_id: str):
        """Get user state from the user document"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {"state": 1}
        )
        print("User State: ", user)
        return user.get("state", {}) if user else None

    def get_or_create_user_state(self, user_id: str, default_state: dict = None) -> dict:
        """Get the user state; if none exists, create with default and return it."""
        if default_state is None:
            default_state = {"initialized": True}
        self.users_collection.update_one(
            {"_id": user_id},
            {
                "$setOnInsert": {
                    "state": default_state,
                    "state_history": []
                }
            },
            upsert=True
        )

        user_doc = self.users_collection.find_one(
            {"_id": user_id}, {"state": 1})
        return user_doc.get("state", default_state)

    # === THINGS ABOUT USER ===

    def set_user_things(self, user_id: str, things: dict):
        """Set things about user"""
        timestamp = {"$date": datetime.now().isoformat()}

        result = self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "things_about_user": things,
                    "things_about_user.updated_at": timestamp
                }
            },
            upsert=True
        )
        return result.modified_count or (1 if result.upserted_id else 0)

    def get_user_things(self, user_id: str):
        """Get things about user"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {"things_about_user": 1}
        )
        return user.get("things_about_user", {}) if user else {}

    def update_user_things(self, user_id: str, things_to_update: dict):
        """Update specific things about user"""
        timestamp = {"$date": datetime.now().isoformat()}
        prefixed_things = {}
        for key, value in things_to_update.items():
            prefixed_things[f"things_about_user.{key}"] = value
        prefixed_things["things_about_user.updated_at"] = timestamp

        result = self.users_collection.update_one(
            {"_id": user_id},
            {"$set": prefixed_things},
            upsert=True
        )
        return result.modified_count or (1 if result.upserted_id else 0)

    def remove_user_things(self, user_id: str, keys: List[str]):
        """Remove specific things about user"""
        prefixed_keys = {}
        for key in keys:
            prefixed_keys[f"things_about_user.{key}"] = ""

        result = self.users_collection.update_one(
            {"_id": user_id},
            {"$unset": prefixed_keys}
        )
        return result.modified_count

    # === CHAT HISTORY ===
    def create_conversation(self, user_id: str, metadata: dict = None):
        """Create a new conversation for a user"""
        conversation_id = f"conv_{int(datetime.now().timestamp())}"
        timestamp = {"$date": datetime.now().isoformat()}
        if metadata is None:
            metadata = {}
        result = self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    f"chat_history.{conversation_id}": {
                        "messages": [],
                        "metadata": metadata,
                        "created_at": timestamp,
                        "updated_at": timestamp
                    }
                }
            },
            upsert=True
        )
        return conversation_id if (result.modified_count > 0 or result.upserted_id) else None

    def add_message(self, user_id: str, conversation_id: str, message: dict):
        """Add a message to a conversation"""
        if "timestamp" not in message:
            message["timestamp"] = {"$date": datetime.now().isoformat()}
        timestamp = {"$date": datetime.now().isoformat()}
        result = self.users_collection.update_one(
            {"_id": user_id, f"chat_history.{conversation_id}": {"$exists": True}},
            {
                "$push": {
                    f"chat_history.{conversation_id}.messages": message
                },
                "$set": {
                    f"chat_history.{conversation_id}.updated_at": timestamp
                }
            }
        )

        if result.modified_count == 0:
            result = self.users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        f"chat_history.{conversation_id}": {
                            "messages": [message],
                            "metadata": {},
                            "created_at": timestamp,
                            "updated_at": timestamp
                        }
                    }
                },
                upsert=True
            )

        return result.modified_count or (1 if result.upserted_id else 0)

    def get_conversations(self, user_id: str, limit: int = 10):
        """Get a list of conversations for a user"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {"chat_history": 1}
        )

        if not user or "chat_history" not in user:
            return []

        conversations = []
        for conv_id, conv_data in user["chat_history"].items():
            conv_data["conversation_id"] = conv_id
            conversations.append(conv_data)

        conversations.sort(
            key=lambda c: c.get(
                "updated_at", {"$date": "1970-01-01T00:00:00Z"}),
            reverse=True
        )

        return conversations[:limit]

    def get_conversation(self, user_id: str, conversation_id: str):
        """Get a specific conversation"""
        user = self.users_collection.find_one(
            {"_id": user_id},
            {f"chat_history.{conversation_id}": 1}
        )

        if not user or "chat_history" not in user or conversation_id not in user["chat_history"]:
            return None

        conversation = user["chat_history"][conversation_id]
        conversation["conversation_id"] = conversation_id
        return conversation

class AsyncChromaStore:
    def __init__(
        self,
        persist_directory: str = "./chroma_data",
        recency_window: int = 5,
        semantic_limit: int = 5,
    ):
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_directory,
                chroma_db_impl="duckdb+parquet",
            )
        )
        self.collection = self.client.get_or_create_collection("conversations")
        self.embed = hf_mpnet_embed
        self.recency_window = recency_window
        self.semantic_limit = semantic_limit

    async def _embed(self, text: str) -> List[float]:
        result = self.embed(text)
        if hasattr(result, "__await__"):
            return await result
        return result

    async def add_message(
        self, conv_id: str, user_id: str, msg_id: str,
        text: str, turn_index: int, payload: Optional[Dict[str,Any]] = None
    ):
        vec = await self._embed(text)
        meta = {"conv_id": conv_id, "user_id": user_id,
                "text": text, "turn": turn_index}
        if payload: meta.update(payload)
        self.collection.add(
            ids=[str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{conv_id}_{msg_id}"))],
            embeddings=[vec],
            metadatas=[meta],
        )

    async def get_relevant(
        self, conv_id: str, query: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        qv = await self._embed(query)
        # 1) Get last recency_window messages:
        all_meta = self.collection.get(include=["metadatas"])
        conv = [m for m in all_meta["metadatas"] if m["conv_id"] == conv_id]
        recency = sorted(conv, key=lambda m: m["turn"], reverse=True)[:self.recency_window]

        # 2) Semantic search (exclude those same IDs)
        exclude_ids = {
            str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{conv_id}_{r['turn']}"))
            for r in recency
        }
        sem = self.collection.query(
            query_embeddings=[qv],
            n_results=self.semantic_limit,
            where={"conv_id": conv_id},
        )
        # Build result list, skipping duplicates
        semantic = []
        for idx, meta in zip(sem["ids"][0], sem["metadatas"][0]):
            if idx in exclude_ids:
                continue
            semantic.append(meta)
            if len(semantic) >= self.semantic_limit:
                break

        return recency + semantic

    async def delete_message(self, conv_id: str, msg_id: str):
        pid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{conv_id}_{msg_id}"))
        self.collection.delete(ids=[pid])

    async def prune_older(self, conv_id: str, keep_last_n: int = 200):
        all_meta = self.collection.get(include=["metadatas", "ids"])
        conv = [(m["turn"], pid) for m, pid in zip(all_meta["metadatas"], all_meta["ids"])
                if m["conv_id"] == conv_id]
        conv_sorted = sorted(conv, key=lambda x: x[0])
        to_delete = [pid for turn, pid in conv_sorted[:-keep_last_n]]
        if to_delete:
            self.collection.delete(ids=to_delete)

    async def count_messages(self, conv_id: str) -> int:
        all_meta = self.collection.get(include=["metadatas"])
        return sum(1 for m in all_meta["metadatas"] if m["conv_id"] == conv_id)



# async def main():
#     print("Starting Chroma client...")
#     store = AsyncChromaStore()
#     print("Chroma store initialized.")

#     conv_id = "demo"
#     user_id = "user123"

#     # 1. Add some messages (with increasing turn indices)
#     await store.add_message(conv_id, user_id, msg_id="1", text="Hello Chroma!", turn_index=1)
#     await store.add_message(conv_id, user_id, msg_id="2", text="This is a second message.", turn_index=2)
#     await store.add_message(conv_id, user_id, msg_id="3", text="Let’s chat more.", turn_index=3)
#     print("Added 3 messages.")

#     # 2. Hybrid retrieval for “second”
#     results = await store.get_relevant(conv_id, query="second")
#     print("Hybrid retrieval results:")
#     for hit in results:
#         print(f"– turn={hit['turn']}, text={hit['text']}")

#     # 3. Prune older than last 2
#     await store.prune_older(conv_id, keep_last_n=2)
#     count_after_prune = await store.count_messages(conv_id)
#     print(f"Count after pruning to last 2: {count_after_prune}")

#     # 4. Delete message “3”
#     await store.delete_message(conv_id, msg_id="3")
#     count_final = await store.count_messages(conv_id)
#     print(f"Count after deleting msg 3: {count_final}")

# if __name__ == "__main__":
#     asyncio.run(main())